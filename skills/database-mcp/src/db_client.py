"""
Database Client
Abstracts PostgreSQL and SQL Server connections and operations.
"""

import hashlib
import json
import logging
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Sequence
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class DatabaseEngine(Enum):
    """Supported database engines."""
    POSTGRESQL = "postgresql"
    SQLSERVER = "sqlserver"


@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    engine: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"
    user: Optional[str] = None
    password: Optional[str] = None
    schema: str = "public"
    integrated_security: bool = False
    profile: Optional[str] = None

    def __post_init__(self):
        """Validate and normalize configuration."""
        if self.engine.lower() not in ["postgresql", "sqlserver"]:
            raise ValueError(f"Unsupported engine: {self.engine}")

        # Set default ports
        if self.engine.lower() == "sqlserver" and self.port == 5432:
            self.port = 1433

        self.engine = self.engine.lower()
        if self.engine == "sqlserver" and "\\\\" in self.host:
            self.host = self.host.replace("\\\\", "\\")
        logger.info(f"Database config initialized: {self.engine}://{self.host}:{self.port}/{self.database}")


class _SqlCmdConnection:
    """Minimal DB-API compatible connection wrapper backed by sqlcmd."""

    def __init__(self, client: "DatabaseClient"):
        self._client = client
        self._closed = False

    def cursor(self) -> "_SqlCmdCursor":
        if self._closed:
            raise RuntimeError("sqlcmd connection is closed")
        return _SqlCmdCursor(self._client)

    def close(self) -> None:
        self._closed = True


class _SqlCmdCursor:
    """Minimal DB-API compatible cursor wrapper backed by sqlcmd."""

    def __init__(self, client: "DatabaseClient"):
        self._client = client
        self._closed = False
        self._index = 0
        self._rows: List[tuple] = []
        self.description: List[tuple] = []

    def execute(self, query: str, params: Optional[Sequence[Any]] = None) -> "_SqlCmdCursor":
        if self._closed:
            raise RuntimeError("sqlcmd cursor is closed")

        normalized_query = query.strip().upper()
        if "OBJECT_DEFINITION(OBJECT_ID(?))" in normalized_query:
            object_name = str(params[0]) if params else ""
            definition = self._client._sqlcmd_get_routine_definition(object_name)
            self.description = [("OBJECT_DEFINITION", None, None, None, None, None, None)]
            self._rows = [(definition,)] if definition else []
            self._index = 0
            return self

        result_rows = self._client._sqlcmd_fetch_rows(query, params)
        column_names = list(result_rows[0].keys()) if result_rows else []
        self.description = [(name, None, None, None, None, None, None) for name in column_names]
        self._rows = [
            tuple(row.get(column_name) for column_name in column_names)
            for row in result_rows
        ]
        self._index = 0
        return self

    def fetchall(self) -> List[tuple]:
        remaining = self._rows[self._index:]
        self._index = len(self._rows)
        return remaining

    def fetchmany(self, size: int) -> List[tuple]:
        upper_bound = min(self._index + size, len(self._rows))
        batch = self._rows[self._index:upper_bound]
        self._index = upper_bound
        return batch

    def fetchone(self) -> Optional[tuple]:
        if self._index >= len(self._rows):
            return None
        row = self._rows[self._index]
        self._index += 1
        return row

    def close(self) -> None:
        self._closed = True


class DatabaseClient:
    """
    Universal database client for PostgreSQL and SQL Server.
    Provides schema exploration, querying, and analysis capabilities.
    """

    def __init__(self, config: DatabaseConfig):
        """Initialize database client."""
        self.config = config
        self.connection = None
        self.engine = DatabaseEngine(config.engine)
        self.sqlcmd_fallback = False
        self._sqlcmd_path = shutil.which("sqlcmd")
        logger.info(f"DatabaseClient created for {self.engine.value}")

    def _validate_identifier(self, value: str, identifier_type: str) -> str:
        """Validate schema, table and column identifiers."""
        if not value or not re.match(r"^[A-Za-z_][A-Za-z0-9_$]*$", value):
            raise ValueError(f"Invalid {identifier_type}: {value}")
        return value

    def _quote_identifier(self, value: str) -> str:
        """Quote identifiers according to the active database engine."""
        validated = self._validate_identifier(value, "identifier")
        if self.engine == DatabaseEngine.POSTGRESQL:
            return f'"{validated}"'
        return f'[{validated}]'

    def _qualified_table_name(self, schema: str, table_name: str) -> str:
        """Build a fully-qualified and safe table name."""
        return f"{self._quote_identifier(schema)}.{self._quote_identifier(table_name)}"

    def _normalize_limit(self, limit: int) -> int:
        """Normalize query limits to a positive integer."""
        normalized = int(limit)
        if normalized <= 0:
            raise ValueError("Limit must be greater than zero")
        return normalized

    def _pick(self, row: Dict[str, Any], *keys: str) -> Any:
        """Pick the first available key from a row dictionary."""
        for key in keys:
            if key in row:
                return row[key]
        return None

    def connect(self) -> None:
        """Establish database connection."""
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                import psycopg2
                self.connection = psycopg2.connect(
                    host=self.config.host,
                    port=self.config.port,
                    database=self.config.database,
                    user=self.config.user,
                    password=self.config.password
                )
            elif self.engine == DatabaseEngine.SQLSERVER:
                self._connect_sqlserver()

            logger.info(f"Connected to {self.engine.value} database: {self.config.database}")

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def _connect_sqlserver(self) -> None:
        """Connect to SQL Server using ODBC first and sqlcmd as fallback."""
        import pyodbc

        connection_errors = []
        for connection_string in self._build_sqlserver_connection_strings():
            try:
                self.connection = pyodbc.connect(connection_string)
                self.sqlcmd_fallback = False
                logger.info("Connected to SQL Server using pyodbc")
                return
            except Exception as exc:
                connection_errors.append(exc)
                logger.warning(f"pyodbc connection attempt failed: {exc}")

        self._enable_sqlcmd_fallback(connection_errors[-1] if connection_errors else None)

    def _build_sqlserver_connection_strings(self) -> List[str]:
        """Build SQL Server connection string candidates."""
        server_targets = []
        if "\\" in self.config.host:
            server_targets.append(self.config.host)
        else:
            server_targets.append(f"{self.config.host},{self.config.port}")
            server_targets.append(self.config.host)

        base_parts = [
            "Driver={ODBC Driver 17 for SQL Server};",
            f"Database={self.config.database};",
            "Encrypt=no;",
            "TrustServerCertificate=yes;",
        ]

        credentials = []
        if self.config.integrated_security:
            credentials.append("Trusted_Connection=yes;")
        else:
            if not self.config.user:
                raise ValueError("SQL Server requires 'user' when integrated_security is false")
            credentials.append(f"UID={self.config.user};")
            credentials.append(f"PWD={self.config.password or ''};")

        return [
            "".join([f"Server={server_target};", *base_parts, *credentials])
            for server_target in server_targets
        ]

    def _enable_sqlcmd_fallback(self, last_error: Optional[Exception]) -> None:
        """Fallback to sqlcmd when ODBC cannot connect to a SQL Server instance."""
        if not self._sqlcmd_path:
            if last_error:
                raise last_error
            raise RuntimeError("sqlcmd is not available for SQL Server fallback")

        self._probe_sqlcmd_connection()
        self.connection = _SqlCmdConnection(self)
        self.sqlcmd_fallback = True
        logger.warning(
            "Using sqlcmd fallback for SQL Server connection to %s/%s",
            self.config.host,
            self.config.database,
        )

    def _probe_sqlcmd_connection(self) -> None:
        """Validate sqlcmd connectivity against the configured database."""
        self._run_sqlcmd("SELECT 1 AS connection_ok")

    def _run_sqlcmd(self, query: str) -> str:
        """Execute a SQL command through sqlcmd and return stdout."""
        if not self._sqlcmd_path:
            raise RuntimeError("sqlcmd is not available in PATH")

        command = [
            self._sqlcmd_path,
            "-S",
            self.config.host,
            "-d",
            self.config.database,
            "-Q",
            f"SET NOCOUNT ON; {query}",
            "-b",
            "-y",
            "0",
            "-Y",
            "0",
            "-w",
            "65535",
        ]

        if self.config.integrated_security:
            command.append("-E")
        else:
            if not self.config.user:
                raise ValueError("SQL Server requires 'user' when integrated_security is false")
            command.extend(["-U", self.config.user, "-P", self.config.password or ""])

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            stderr = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"sqlcmd execution failed: {stderr}")

        return result.stdout.strip()

    def _sql_literal(self, value: Any) -> str:
        """Convert python values into safe SQL literals."""
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "1" if value else "0"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S.%f')}'"

        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"

    def _apply_sql_parameters(self, query: str, params: Optional[Sequence[Any]]) -> str:
        """Expand DB-API placeholders for the sqlcmd fallback runner."""
        if not params:
            return query

        expanded = query
        for value in params:
            expanded = expanded.replace("?", self._sql_literal(value), 1)
        return expanded

    def _sqlcmd_fetch_rows(self, query: str, params: Optional[Sequence[Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT statement through sqlcmd and return rows as dictionaries."""
        expanded_query = self._apply_sql_parameters(query, params).strip().rstrip(";")
        if "FOR XML" in expanded_query.upper():
            xml_query = expanded_query
        else:
            xml_query = f"{expanded_query} FOR XML RAW('row'), ROOT('rows'), ELEMENTS XSINIL"

        xml_output = self._run_sqlcmd(xml_query)
        if not xml_output:
            return []

        return self._parse_xml_rows(xml_output)

    def _parse_xml_rows(self, xml_output: str) -> List[Dict[str, Any]]:
        """Parse SQL Server XML rowsets into dictionaries."""
        root = ET.fromstring(xml_output)
        rows: List[Dict[str, Any]] = []
        nil_attribute = "{http://www.w3.org/2001/XMLSchema-instance}nil"

        for row_element in root:
            if row_element.tag.split("}", 1)[-1] != "row":
                continue

            row: Dict[str, Any] = {}
            for column_element in row_element:
                column_name = column_element.tag.split("}", 1)[-1]
                is_nil = column_element.attrib.get(nil_attribute) == "true"
                row[column_name] = None if is_nil else (column_element.text or "")
            rows.append(row)

        return rows

    def _sqlcmd_get_routine_definition(self, object_name: str) -> str:
        """Read SQL object definitions directly from sys.sql_modules via sqlcmd."""
        if "." in object_name:
            schema, routine_name = object_name.split(".", 1)
        else:
            schema, routine_name = self.config.schema, object_name

        rows = self._sqlcmd_fetch_rows(
            """
            SELECT m.definition AS definition
            FROM sys.sql_modules m
            INNER JOIN sys.objects o ON m.object_id = o.object_id
            INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
            WHERE s.name = ? AND o.name = ?
            """,
            (schema, routine_name),
        )

        if not rows:
            return "Routine not found or is encrypted"

        return rows[0].get("definition", "") or "Routine not found or is encrypted"

    def disconnect(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from database")

    def execute_query(self, query: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts."""
        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchmany(limit)
            return [dict(zip(columns, row)) for row in rows]
        finally:
            cursor.close()

    def get_tables(self, schema: str = "public") -> List[str]:
        """Get list of tables in schema."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = %s AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                """, (schema,))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """, (schema,))

            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_views(self, schema: str = "public") -> List[str]:
        """Get list of views in schema."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = %s AND table_type = 'VIEW'
                    ORDER BY table_name
                """, (schema,))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'VIEW'
                    ORDER BY TABLE_NAME
                """, (schema,))

            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_columns(self, table_name: str, schema: str = "public") -> List[Dict[str, Any]]:
        """Get column information for a table."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT
                        column_name,
                        data_type,
                        is_nullable,
                        column_default,
                        ordinal_position
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position
                """, (schema, table_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        COLUMN_NAME,
                        DATA_TYPE,
                        IS_NULLABLE,
                        COLUMN_DEFAULT,
                        ORDINAL_POSITION
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
                    ORDER BY ORDINAL_POSITION
                """, (schema, table_name))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_primary_key(self, table_name: str, schema: str = "public") -> Optional[List[str]]:
        """Get primary key columns for a table."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT a.attname
                    FROM pg_index i
                    JOIN pg_attribute a ON a.attrelid = i.indrelid
                        AND a.attnum = ANY(i.indkey)
                    WHERE i.indisprimary
                        AND i.indrelid = (
                            SELECT c.oid
                            FROM pg_class c
                            JOIN pg_namespace n ON n.oid = c.relnamespace
                            WHERE n.nspname = %s AND c.relname = %s
                        )
                    ORDER BY a.attnum
                """, (schema, table_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                    WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
                        AND CONSTRAINT_NAME LIKE 'PK%'
                """, (schema, table_name))

            pk_columns = [row[0] for row in cursor.fetchall()]
            return pk_columns if pk_columns else None
        finally:
            cursor.close()

    def get_foreign_keys(self, table_name: str, schema: str = "public") -> List[Dict[str, Any]]:
        """Get foreign key relationships for a table."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT
                        constraint_name,
                        column_name,
                        foreign_table_schema,
                        foreign_table_name,
                        foreign_column_name
                    FROM information_schema.referential_constraints rc
                    JOIN information_schema.key_column_usage kcu
                        ON rc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu
                        ON rc.unique_constraint_name = ccu.constraint_name
                    WHERE kcu.table_schema = %s AND kcu.table_name = %s
                """, (schema, table_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        kcu.CONSTRAINT_NAME,
                        kcu.COLUMN_NAME,
                        ccu.TABLE_SCHEMA AS REFERENCED_TABLE_SCHEMA,
                        ccu.TABLE_NAME AS REFERENCED_TABLE_NAME,
                        ccu.COLUMN_NAME AS REFERENCED_COLUMN_NAME
                    FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
                    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                        ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                    JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu
                        ON rc.UNIQUE_CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
                    WHERE kcu.TABLE_SCHEMA = ? AND kcu.TABLE_NAME = ?
                """, (schema, table_name))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_all_foreign_keys(self, schema: str = "public") -> List[Dict[str, Any]]:
        """Get all foreign key relationships in schema."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT
                        kcu.table_name,
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu
                        ON tc.constraint_name = ccu.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_schema = %s
                """, (schema,))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        kcu.TABLE_NAME,
                        kcu.COLUMN_NAME,
                        ccu.TABLE_NAME AS foreign_table_name,
                        ccu.COLUMN_NAME AS foreign_column_name
                    FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
                    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                        ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                    JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu
                        ON rc.UNIQUE_CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
                    WHERE kcu.TABLE_SCHEMA = ?
                """, (schema,))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_procedures(self, schema: str = "public") -> List[str]:
        """Get list of stored procedures."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT routine_name
                    FROM information_schema.routines
                    WHERE routine_schema = %s AND routine_type = 'PROCEDURE'
                    ORDER BY routine_name
                """, (schema,))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT ROUTINE_NAME
                    FROM INFORMATION_SCHEMA.ROUTINES
                    WHERE ROUTINE_SCHEMA = ? AND ROUTINE_TYPE = 'PROCEDURE'
                    ORDER BY ROUTINE_NAME
                """, (schema,))

            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_functions(self, schema: str = "public") -> List[str]:
        """Get list of functions."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT routine_name
                    FROM information_schema.routines
                    WHERE routine_schema = %s AND routine_type = 'FUNCTION'
                    ORDER BY routine_name
                """, (schema,))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT ROUTINE_NAME
                    FROM INFORMATION_SCHEMA.ROUTINES
                    WHERE ROUTINE_SCHEMA = ? AND ROUTINE_TYPE = 'FUNCTION'
                    ORDER BY ROUTINE_NAME
                """, (schema,))

            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_triggers(self, schema: str = "public") -> List[str]:
        """Get list of triggers."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT trigger_name
                    FROM information_schema.triggers
                    WHERE trigger_schema = %s
                    ORDER BY trigger_name
                """, (schema,))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT name
                    FROM sys.triggers
                    WHERE is_ms_shipped = 0
                      AND parent_class_desc = 'OBJECT_OR_COLUMN'
                      AND OBJECT_SCHEMA_NAME(parent_id) = ?
                    ORDER BY name
                """, (schema,))

            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_routine_definition(self, routine_name: str, schema: str = "public", routine_type: str = "procedure") -> str:
        """Get source code of a stored procedure or function."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT pg_get_functiondef(p.oid)
                    FROM pg_proc p
                    JOIN pg_namespace n ON n.oid = p.pronamespace
                    WHERE n.nspname = %s AND p.proname = %s
                """, (schema, routine_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT OBJECT_DEFINITION(OBJECT_ID(?))
                """, (f"{schema}.{routine_name}",))

            result = cursor.fetchone()
            return result[0] if result else "Routine not found or is encrypted"
        finally:
            cursor.close()

    def get_indexes(self, table_name: str, schema: str = "public") -> List[Dict[str, Any]]:
        """Get indexes for a table."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT
                        indexname,
                        indexdef
                    FROM pg_indexes
                    WHERE schemaname = %s AND tablename = %s
                """, (schema, table_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        i.name,
                        i.type_desc,
                        STUFF((
                            SELECT ', ' + c2.name
                            FROM sys.index_columns ic2
                            JOIN sys.columns c2
                                ON ic2.object_id = c2.object_id
                               AND ic2.column_id = c2.column_id
                            WHERE ic2.object_id = i.object_id
                              AND ic2.index_id = i.index_id
                            ORDER BY ic2.key_ordinal, ic2.index_column_id
                            FOR XML PATH(''), TYPE
                        ).value('.', 'nvarchar(max)'), 1, 2, '') AS columns
                    FROM sys.indexes i
                    JOIN sys.tables t ON i.object_id = t.object_id
                    WHERE t.schema_id = SCHEMA_ID(?) AND t.name = ?
                      AND i.is_hypothetical = 0
                      AND i.name IS NOT NULL
                """, (schema, table_name))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_row_count(self, table_name: str, schema: str = "public") -> int:
        """Get approximate row count for a table."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT n_live_tup FROM pg_stat_user_tables
                    WHERE schemaname = %s AND relname = %s
                """, (schema, table_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT SUM(p.rows)
                    FROM sys.tables t
                    JOIN sys.partitions p ON t.object_id = p.object_id
                    WHERE t.name = ?
                      AND SCHEMA_NAME(t.schema_id) = ?
                      AND p.index_id IN (0, 1)
                """, (table_name, schema))

            result = cursor.fetchone()
            return int(result[0]) if result and result[0] else 0
        finally:
            cursor.close()

    def get_table_stats(self, table_name: str, schema: str = "public") -> Dict[str, Any]:
        """Get statistics for a table."""
        stats = {
            "table": table_name,
            "schema": schema,
            "row_count": self.get_row_count(table_name, schema),
            "columns": len(self.get_columns(table_name, schema))
        }

        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT pg_size_pretty(pg_total_relation_size(%s))
                """, (f"{schema}.{table_name}",))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        SUM(p.rows) as row_count,
                        SUM(au.total_pages * 8) as size_kb
                    FROM sys.tables t
                    JOIN sys.partitions p ON t.object_id = p.object_id
                    JOIN sys.allocation_units au ON p.partition_id = au.container_id
                                        WHERE t.name = ?
                                            AND SCHEMA_NAME(t.schema_id) = ?
                                """, (table_name, schema))

            result = cursor.fetchone()
            if result:
                if self.engine == DatabaseEngine.POSTGRESQL:
                    stats["size"] = result[0]
                else:
                    stats["size_kb"] = result[1]

        finally:
            cursor.close()

        return stats

    def search_columns(self, pattern: str, schema: str = "public") -> List[Dict[str, Any]]:
        """Search for columns by name pattern."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT
                        table_name,
                        column_name,
                        data_type
                    FROM information_schema.columns
                    WHERE table_schema = %s AND column_name ILIKE %s
                    ORDER BY table_name, column_name
                """, (schema, f"%{pattern}%"))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        TABLE_NAME,
                        COLUMN_NAME,
                        DATA_TYPE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = ? AND COLUMN_NAME LIKE ?
                    ORDER BY TABLE_NAME, COLUMN_NAME
                """, (schema, f"%{pattern}%"))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_distinct_values(self, table_name: str, column_name: str, schema: str = "public", limit: int = 100) -> List[Any]:
        """Get distinct values from a column."""
        cursor = self.connection.cursor()
        try:
            normalized_limit = self._normalize_limit(limit)
            qualified_table = self._qualified_table_name(schema, table_name)
            quoted_column = self._quote_identifier(column_name)

            if self.engine == DatabaseEngine.POSTGRESQL:
                query = f"SELECT DISTINCT {quoted_column} AS value FROM {qualified_table} ORDER BY {quoted_column} LIMIT %s"
                cursor.execute(query, (normalized_limit,))
            else:
                query = f"SELECT DISTINCT TOP {normalized_limit} {quoted_column} AS value FROM {qualified_table} ORDER BY {quoted_column}"
                cursor.execute(query)

            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def build_discovery_index(self, schema: Optional[str] = None) -> Dict[str, Any]:
        """Build a discovery index representing the current database inventory."""
        schema_name = schema or self.config.schema
        tables = self.get_tables(schema_name)
        views = self.get_views(schema_name)
        procedures = self.get_procedures(schema_name)
        functions = self.get_functions(schema_name)
        triggers = self.get_triggers(schema_name)

        table_inventory = []
        for table_name in tables:
            columns = self.get_columns(table_name, schema_name)
            primary_key = self.get_primary_key(table_name, schema_name) or []
            foreign_keys = self.get_foreign_keys(table_name, schema_name)
            table_inventory.append({
                "name": table_name,
                "column_count": len(columns),
                "primary_key": primary_key,
                "foreign_key_count": len(foreign_keys),
                "columns": [
                    {
                        "name": self._pick(column, "column_name", "COLUMN_NAME"),
                        "type": self._pick(column, "data_type", "DATA_TYPE"),
                        "nullable": self._pick(column, "is_nullable", "IS_NULLABLE"),
                    }
                    for column in columns
                ]
            })

        normalized_inventory = {
            "database": {
                "engine": self.config.engine,
                "host": self.config.host,
                "port": self.config.port,
                "name": self.config.database,
                "schema_principal": schema_name,
            },
            "artifacts": {
                "directory": "documentacao/banco_dados",
                "discovery_database": "documentacao/banco_dados/discovery-database.yml",
            },
            "inventory": {
                "tables": table_inventory,
                "views": views,
                "procedures": procedures,
                "functions": functions,
                "triggers": triggers,
            }
        }

        schema_hash = hashlib.sha256(
            json.dumps(normalized_inventory, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()

        return {
            "discovery": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "schema_hash": schema_hash,
                "auto_updated": True,
            },
            **normalized_inventory,
        }

    def analyze_table_relationships(self, table_name: str, schema: str = "public", depth: int = 2) -> Dict[str, Any]:
        """Analyze relationships between tables."""
        relationships = {
            "table": table_name,
            "outgoing_keys": self.get_foreign_keys(table_name, schema),
            "incoming_keys": self._get_incoming_foreign_keys(table_name, schema)
        }

        if depth > 1:
            relationships["related_tables"] = self._get_related_tables(table_name, schema, depth - 1)

        return relationships

    def _get_incoming_foreign_keys(self, table_name: str, schema: str = "public") -> List[Dict[str, Any]]:
        """Get foreign keys that reference this table."""
        cursor = self.connection.cursor()
        try:
            if self.engine == DatabaseEngine.POSTGRESQL:
                cursor.execute(f"""
                    SELECT
                        kcu.table_name,
                        kcu.column_name,
                        ccu.table_name AS reference_table
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu
                        ON tc.constraint_name = ccu.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND ccu.table_schema = %s
                        AND ccu.table_name = %s
                """, (schema, table_name))
            else:  # SQL Server
                cursor.execute(f"""
                    SELECT
                        kcu.TABLE_NAME,
                        kcu.COLUMN_NAME,
                        ccu.TABLE_NAME AS REFERENCE_TABLE
                    FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
                    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                        ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                    JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu
                        ON rc.UNIQUE_CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
                    WHERE ccu.TABLE_NAME = ?
                      AND ccu.TABLE_SCHEMA = ?
                """, (table_name, schema))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def _get_related_tables(self, table_name: str, schema: str = "public", depth: int = 1) -> List[str]:
        """Get list of directly related tables."""
        related = set()

        # Outgoing FKs
        for fk in self.get_foreign_keys(table_name, schema):
            related.add(fk.get("foreign_table_name", ""))

        # Incoming FKs
        for fk in self._get_incoming_foreign_keys(table_name, schema):
            related.add(self._pick(fk, "table_name", "TABLE_NAME") or "")

        related.discard("")
        return sorted(related)

    def build_er_diagram_mermaid(self, schema: Optional[str] = None) -> str:
        """Build an Entity-Relationship diagram in Mermaid format."""
        schema_name = schema or self.config.schema
        tables = self.get_tables(schema_name)
        all_fks = self.get_all_foreign_keys(schema_name)

        # Start Mermaid ER diagram
        mermaid_lines = ["erDiagram"]

        # Build table definitions with columns
        table_data = {}
        for table_name in sorted(tables):
            columns = self.get_columns(table_name, schema_name)
            pk_columns = self.get_primary_key(table_name, schema_name) or []

            table_data[table_name] = {
                "columns": columns,
                "pk_columns": pk_columns
            }

        # Add relationships (foreign keys) first
        added_relationships = set()
        for fk in all_fks:
            source_table = fk.get("table_name", "")
            target_table = fk.get("foreign_table_name", "")

            if source_table and target_table and source_table in tables and target_table in tables:
                # Create unique relationship identifier (one relationship per table pair)
                rel_key = tuple(sorted([source_table, target_table]))

                if rel_key not in added_relationships:
                    # Many-to-One relationship: many source rows reference one target row
                    # Format: TARGET ||--o{ SOURCE : ""
                    relationship_line = f"    {target_table} ||--o" + "{ " + f"{source_table} : \"\""
                    mermaid_lines.append(relationship_line)
                    added_relationships.add(rel_key)

        # Add table definitions with columns
        for table_name in sorted(tables):
            columns = table_data[table_name]["columns"]
            pk_columns = table_data[table_name]["pk_columns"]

            if columns:
                mermaid_lines.append(f"    {table_name} {{")

                for col in columns:
                    col_name = self._pick(col, "column_name", "COLUMN_NAME")
                    col_type = self._pick(col, "data_type", "DATA_TYPE")

                    # Normalize type for display
                    clean_type = str(col_type).split("(")[0].lower()

                    # Check if it's a PK or FK
                    is_pk = col_name in pk_columns

                    # Check if it's part of a foreign key
                    is_fk = False
                    for fk in all_fks:
                        if (fk.get("table_name") == table_name and
                            fk.get("column_name") == col_name):
                            is_fk = True
                            break

                    # Build attribute line with markers
                    markers = ""
                    if is_pk:
                        markers += " PK"
                    if is_fk:
                        markers += " FK"

                    mermaid_lines.append(f"        {clean_type} {col_name}{markers}")

                mermaid_lines.append("    }")

        return "\n".join(mermaid_lines)
