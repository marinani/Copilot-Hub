#!/usr/bin/env python3
"""
Database MCP Server
Model Context Protocol server for interacting with PostgreSQL and SQL Server databases.
Enables exploration, querying, schema discovery and data analysis through VS Code Chat.
"""

import json
import inspect
import sys
import re
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs):
        """Fallback no-op when python-dotenv is not installed."""
        return False

from db_client import DatabaseClient, DatabaseConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


class DatabaseMCPServer:
    """
    MCP Server implementation for database interactions.
    Supports PostgreSQL and SQL Server.
    """

    SCHEMA_INDEX_TOOLS = {
        "explore_schema",
        "list_tables",
        "describe_table",
        "list_routines",
        "get_routine_code",
        "list_indexes",
        "list_foreign_keys",
        "get_row_count",
        "get_table_statistics",
        "search_column",
        "get_enum_values",
        "analyze_relationships"
    }

    PROFILE_MANAGEMENT_TOOLS = {
        "list_profiles",
        "configure_profile"
    }

    def __init__(self, config: Optional[dict] = None, config_path: Optional[str] = None):
        """Initialize MCP server with configuration."""
        self.project_root = self._find_project_root()
        self.skill_root = Path(__file__).resolve().parents[1]
        self.output_dir = self.project_root / "documentacao" / "banco_dados"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if config_path:
            provided_path = Path(config_path)
            self.config_path = provided_path if provided_path.is_absolute() else (self.project_root / provided_path)
        else:
            self.config_path = None
        self.config = config.copy() if config else None
        self.active_profile_name: Optional[str] = None
        self.db_client: Optional[DatabaseClient] = None
        self.tools = self._register_tools()
        logger.info("Database MCP Server initialized")

    def _find_project_root(self) -> Path:
        """Find the project root based on the .github folder location."""
        current_file = Path(__file__).resolve()
        for parent in current_file.parents:
            if parent.name == ".github":
                return parent.parent

        if len(current_file.parents) >= 4:
            return current_file.parents[3]

        return current_file.parent

    def _parse_yaml_scalar(self, value: str) -> Any:
        """Parse a basic YAML scalar value."""
        lowered = value.lower()
        if lowered in {"null", "~"}:
            return None
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1].replace('\\"', '"').replace('\\n', '\n')
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        if re.match(r"^-?\d+$", value):
            return int(value)
        if re.match(r"^-?\d+\.\d+$", value):
            return float(value)
        if value == "{}":
            return {}
        if value == "[]":
            return []
        return value

    def _parse_yaml(self, text: str) -> dict:
        """Parse a restricted YAML subset (nested mappings and simple scalars)."""
        root: Dict[str, Any] = {}
        stack: List[Tuple[int, Dict[str, Any]]] = [(-1, root)]

        for raw_line in text.splitlines():
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue

            indent = len(raw_line) - len(raw_line.lstrip(" "))
            line = raw_line.strip()
            if ":" not in line:
                raise ValueError(f"Linha YAML inválida: {raw_line}")

            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()

            while stack and indent <= stack[-1][0]:
                stack.pop()

            current = stack[-1][1]
            if value == "":
                current[key] = {}
                stack.append((indent, current[key]))
            else:
                current[key] = self._parse_yaml_scalar(value)

        return root

    def _resolve_workspace_config_path(self) -> Path:
        """Resolve the workspace config.yaml path, preferring .vscode over .github."""
        if self.config_path:
            return self.config_path

        vscode_path = self.project_root / ".vscode" / "config.yaml"
        github_path = self.project_root / ".github" / "config.yaml"

        if vscode_path.exists():
            return vscode_path
        if github_path.exists():
            return github_path

        return github_path

    def _load_workspace_config(self) -> Tuple[Path, Dict[str, Any]]:
        """Load workspace configuration from .github/config.yaml or .vscode/config.yaml."""
        load_dotenv(self.project_root / ".env")

        config_path = self._resolve_workspace_config_path()

        try:
            content = config_path.read_text(encoding='utf-8-sig')
        except FileNotFoundError:
            return config_path, {}

        if not content.strip():
            return config_path, {}

        return config_path, self._parse_yaml(content)

    def _write_workspace_config(self, config_path: Path, config_data: dict) -> None:
        """Persist workspace configuration to YAML."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(self._to_yaml(config_data) + "\n", encoding='utf-8')

    def _normalize_profile_config(self, profile_name: str, profile_data: dict) -> dict:
        """Normalize a datasource profile into DatabaseConfig-compatible keys."""
        engine = profile_data.get("type") or profile_data.get("engine")
        host = profile_data.get("server") or profile_data.get("host")
        database = profile_data.get("database") or profile_data.get("name")
        user = profile_data.get("user") or profile_data.get("username")
        password = profile_data.get("password", "")
        port = profile_data.get("port")
        schema = profile_data.get("schema") or ("dbo" if engine == "sqlserver" else "public")
        integrated_security = bool(profile_data.get("integrated_security", False))

        required_fields = {
            "type": engine,
            "server": host,
            "database": database,
        }

        if not integrated_security:
            required_fields["user"] = user

        missing_fields = [
            field_name
            for field_name, field_value in required_fields.items()
            if field_value in (None, "")
        ]

        if missing_fields:
            raise ValueError(
                f"O profile '{profile_name}' está incompleto. Campos obrigatórios ausentes: {', '.join(missing_fields)}"
            )

        normalized_engine = str(engine).lower()
        normalized_port = int(port) if port not in (None, "") else (1433 if normalized_engine == "sqlserver" else 5432)

        return {
            "engine": normalized_engine,
            "host": host,
            "port": normalized_port,
            "database": database,
            "user": user,
            "password": password,
            "schema": schema,
            "integrated_security": integrated_security,
            "profile": profile_name,
        }

    def _connection_prompt_payload(self, config_path: Path, message: str, available_profiles: Optional[List[str]] = None) -> dict:
        """Build a handoff-friendly payload requesting datasource information."""
        payload = {
            "status": "requires_input",
            "message": message,
            "config_path": str(config_path),
            "handoff": {
                "action": "collect_datasource_profile",
                "terminate_if_not_provided": True,
                "required_fields": [
                    "profile",
                    "type",
                    "server",
                    "port",
                    "database",
                    "user",
                    "password",
                    "schema"
                ]
            }
        }

        if available_profiles is not None:
            payload["available_profiles"] = available_profiles
            payload["handoff"]["options"] = [
                {
                    "value": "use_existing_profile",
                    "label": "Usar profile existente"
                },
                {
                    "value": "create_new_profile",
                    "label": "Cadastrar novo profile"
                }
            ]

        return payload

    def _ensure_profile_ready(self, tool_input: dict) -> Optional[dict]:
        """Ensure there is a valid datasource profile selected for the request."""
        if self.config is not None and self.active_profile_name == self.config.get("profile"):
            return None

        config_path, workspace_config = self._load_workspace_config()
        datasource = workspace_config.get("datasource") or {}
        profiles = datasource.get("profiles") or {}

        if not isinstance(profiles, dict) or not profiles:
            return self._connection_prompt_payload(
                config_path,
                "Nenhum profile de datasource foi configurado em config.yaml. Informe os dados da conexão via handoff; se não informar, a tarefa deve ser encerrada imediatamente."
            )

        requested_profile = tool_input.get("profile")
        default_profile = datasource.get("default_profile")

        if requested_profile in (None, ""):
            if default_profile:
                requested_profile = default_profile
            elif len(profiles) == 1:
                requested_profile = next(iter(profiles.keys()))
            else:
                return self._connection_prompt_payload(
                    config_path,
                    "Há mais de um profile configurado e nenhum foi informado. Escolha um profile existente ou cadastre um novo via handoff.",
                    sorted(profiles.keys())
                )

        if requested_profile not in profiles:
            return self._connection_prompt_payload(
                config_path,
                f"O profile '{requested_profile}' não existe. Escolha um profile existente ou cadastre um novo.",
                sorted(profiles.keys())
            )

        normalized_config = self._normalize_profile_config(requested_profile, profiles[requested_profile])

        if self.active_profile_name != requested_profile or self.config != normalized_config:
            if self.db_client:
                self.db_client.disconnect()
                self.db_client = None

            self.config = normalized_config
            self.active_profile_name = requested_profile

        return None

    def _default_schema(self, schema: Optional[str] = None) -> str:
        """Resolve schema with fallback to the configured default."""
        active_config = self.config or {}
        return schema or active_config.get("schema", "public")

    def _schema_from_input(self, tool_input: dict) -> str:
        """Extract schema from tool input using the configured fallback."""
        return self._default_schema(tool_input.get("schema"))

    def _serialize_yaml_scalar(self, value: Any) -> str:
        """Serialize simple scalar values to YAML."""
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)

        text = str(value).replace("\n", "\\n")
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'

    def _to_yaml(self, value: Any, indent: int = 0) -> str:
        """Serialize Python structures to YAML without external dependencies."""
        prefix = "  " * indent

        if isinstance(value, dict):
            if not value:
                return f"{prefix}{{}}"

            lines = []
            for key, item in value.items():
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.append(self._to_yaml(item, indent + 1))
                else:
                    lines.append(f"{prefix}{key}: {self._serialize_yaml_scalar(item)}")
            return "\n".join(lines)

        if isinstance(value, list):
            if not value:
                return f"{prefix}[]"

            lines = []
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{prefix}-")
                    lines.append(self._to_yaml(item, indent + 1))
                elif isinstance(item, list):
                    lines.append(f"{prefix}-")
                    lines.append(self._to_yaml(item, indent + 1))
                else:
                    lines.append(f"{prefix}- {self._serialize_yaml_scalar(item)}")
            return "\n".join(lines)

        return f"{prefix}{self._serialize_yaml_scalar(value)}"

    def _generate_er_diagram(self, schema: str) -> dict:
        """Generate ER diagram in Mermaid format."""
        er_content = self.active_client.build_er_diagram_mermaid(schema)

        # Wrap in markdown with code block
        markdown_content = f"""# Diagrama ER - {self.config.get('database', 'database')}

> Gerado automaticamente pelo Database MCP Server

## Estrutura de Dados

```mermaid
{er_content}
```

---
Generated at: {datetime.now(timezone.utc).isoformat()}
"""

        output_path = self.output_dir / "DADOS-01-ER.md"
        previous_content = output_path.read_text(encoding='utf-8') if output_path.exists() else None
        updated = previous_content != markdown_content

        if updated:
            output_path.write_text(markdown_content, encoding='utf-8')
            logger.info("Updated DADOS-01-ER.md at %s", output_path)

        return {
            "path": str(output_path),
            "updated": updated,
            "schema": schema,
            "output_directory": str(self.output_dir)
        }

    def _refresh_discovery_project(self, schema: str) -> dict:
        """Regenerate the discovery-database.yml index when the schema changes."""
        index_data = self.active_client.build_discovery_index(schema)
        output_path = self.output_dir / "discovery-database.yml"
        yaml_content = self._to_yaml(index_data) + "\n"

        previous_content = output_path.read_text(encoding='utf-8') if output_path.exists() else None
        updated = previous_content != yaml_content

        if updated:
            output_path.write_text(yaml_content, encoding='utf-8')
            logger.info("Updated discovery-database.yml at %s", output_path)

        # Also generate ER diagram
        er_result = self._generate_er_diagram(schema)

        return {
            "path": str(output_path),
            "updated": updated,
            "schema": schema,
            "output_directory": str(self.output_dir),
            "schema_hash": index_data.get("discovery", {}).get("schema_hash"),
            "er_diagram": er_result
        }

    def _register_tools(self) -> dict:
        """Register all available tools."""
        return {
            "explore_schema": {
                "description": "Explore database schema - list tables, views, and structure",
                "handler": self.tool_explore_schema
            },
            "list_tables": {
                "description": "List all tables in the specified schema",
                "handler": self.tool_list_tables
            },
            "describe_table": {
                "description": "Get detailed information about a table (columns, types, constraints)",
                "handler": self.tool_describe_table
            },
            "list_routines": {
                "description": "List stored procedures, functions, and triggers",
                "handler": self.tool_list_routines
            },
            "get_routine_code": {
                "description": "Get the source code of a stored procedure or function",
                "handler": self.tool_get_routine_code
            },
            "list_indexes": {
                "description": "List indexes for a table",
                "handler": self.tool_list_indexes
            },
            "list_foreign_keys": {
                "description": "List foreign key relationships",
                "handler": self.tool_list_foreign_keys
            },
            "query_data": {
                "description": "Execute a SELECT query and return results (limited to 1000 rows)",
                "handler": self.tool_query_data
            },
            "get_row_count": {
                "description": "Get row count for a table",
                "handler": self.tool_get_row_count
            },
            "get_table_statistics": {
                "description": "Get statistics for a table (size, row count, last update)",
                "handler": self.tool_get_table_statistics
            },
            "search_column": {
                "description": "Search for columns by name pattern across all tables",
                "handler": self.tool_search_column
            },
            "get_enum_values": {
                "description": "Get distinct values from a column (useful for status/enum fields)",
                "handler": self.tool_get_enum_values
            },
            "analyze_relationships": {
                "description": "Analyze relationships between tables",
                "handler": self.tool_analyze_relationships
            },
            "list_profiles": {
                "description": "List configured datasource profiles from config.yaml",
                "handler": self.tool_list_profiles
            },
            "configure_profile": {
                "description": "Create or update a datasource profile in config.yaml",
                "handler": self.tool_configure_profile
            }
        }

    @property
    def active_client(self) -> DatabaseClient:
        """Ensure database client is connected."""
        if self.config is None:
            raise ValueError("Nenhum profile ativo foi carregado para a conexão com o banco de dados.")

        if self.db_client is None:
            db_config = DatabaseConfig(**self.config)
            self.db_client = DatabaseClient(db_config)
            self.db_client.connect()
        return self.db_client

    def process_request(self, request: dict) -> dict:
        """
        Process incoming MCP request.
        Expected format:
        {
            "tool": "tool_name",
            "input": {...parameters...}
        }

        Contract notes:
        - profile resolution is enforced for every database tool except profile management tools;
        - structural tools automatically refresh discovery artifacts after successful execution.
        """
        try:
            tool_name = request.get("tool")
            tool_input = request.get("input", {})

            if tool_name not in self.tools:
                return {
                    "status": "error",
                    "error": f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
                }

            if tool_name not in self.PROFILE_MANAGEMENT_TOOLS:
                profile_state = self._ensure_profile_ready(tool_input)
                if profile_state is not None:
                    return profile_state

            logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
            handler = self.tools[tool_name]["handler"]
            handler_signature = inspect.signature(handler)
            accepted_parameters = {
                name
                for name, parameter in handler_signature.parameters.items()
                if parameter.kind in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
            }
            filtered_input = {
                key: value
                for key, value in tool_input.items()
                if key in accepted_parameters
            }
            result = handler(**filtered_input)

            metadata = {
                "artifacts_directory": str(self.output_dir)
            }

            if self.active_profile_name:
                metadata["profile"] = self.active_profile_name

            if tool_name in self.SCHEMA_INDEX_TOOLS:
                metadata["discovery_database"] = self._refresh_discovery_project(self._schema_from_input(tool_input))

            response = {
                "status": "success",
                "tool": tool_name,
                "result": result
            }

            if metadata:
                response["metadata"] = metadata

            return response

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }

    # Tool implementations
    def tool_explore_schema(self, schema: Optional[str] = None) -> dict:
        """Explore database schema structure."""
        client = self.active_client
        schema = self._default_schema(schema)
        tables = client.get_tables(schema)
        views = client.get_views(schema)

        # Generate discovery index and ER diagram
        discovery_result = self._refresh_discovery_project(schema)

        return {
            "schema": schema,
            "tables": len(tables),
            "views": len(views),
            "tables_list": tables,
            "views_list": views,
            "documentation": discovery_result
        }

    def tool_list_tables(self, schema: Optional[str] = None) -> dict:
        """List all tables in schema."""
        client = self.active_client
        schema = self._default_schema(schema)
        tables = client.get_tables(schema)
        return {
            "schema": schema,
            "count": len(tables),
            "tables": tables
        }

    def tool_describe_table(self, table_name: str, schema: Optional[str] = None) -> dict:
        """Get detailed table information."""
        client = self.active_client
        schema = self._default_schema(schema)
        columns = client.get_columns(table_name, schema)
        pk = client.get_primary_key(table_name, schema)
        fks = client.get_foreign_keys(table_name, schema)

        return {
            "table": table_name,
            "schema": schema,
            "columns": columns,
            "primary_key": pk,
            "foreign_keys": fks,
            "column_count": len(columns)
        }

    def tool_list_routines(self, schema: Optional[str] = None, routine_type: str = "all") -> dict:
        """List stored procedures, functions, triggers."""
        client = self.active_client
        schema = self._default_schema(schema)

        result = {}
        if routine_type in ["all", "procedure"]:
            result["procedures"] = client.get_procedures(schema)
        if routine_type in ["all", "function"]:
            result["functions"] = client.get_functions(schema)
        if routine_type in ["all", "trigger"]:
            result["triggers"] = client.get_triggers(schema)

        return {
            "schema": schema,
            "routine_type": routine_type,
            "count": sum(len(v) if isinstance(v, list) else 0 for v in result.values()),
            "routines": result
        }

    def tool_get_routine_code(self, routine_name: str, schema: Optional[str] = None, routine_type: str = "procedure") -> dict:
        """Get source code of stored procedure or function."""
        client = self.active_client
        schema = self._default_schema(schema)
        code = client.get_routine_definition(routine_name, schema, routine_type)

        return {
            "routine": routine_name,
            "schema": schema,
            "type": routine_type,
            "code": code
        }

    def tool_list_indexes(self, table_name: str, schema: Optional[str] = None) -> dict:
        """List indexes for a table."""
        client = self.active_client
        schema = self._default_schema(schema)
        indexes = client.get_indexes(table_name, schema)

        return {
            "table": table_name,
            "schema": schema,
            "count": len(indexes),
            "indexes": indexes
        }

    def tool_list_foreign_keys(self, table_name: Optional[str] = None, schema: Optional[str] = None) -> dict:
        """List foreign key relationships."""
        client = self.active_client
        schema = self._default_schema(schema)

        if table_name:
            fks = client.get_foreign_keys(table_name, schema)
            return {
                "table": table_name,
                "schema": schema,
                "relations": fks
            }
        else:
            all_fks = client.get_all_foreign_keys(schema)
            return {
                "schema": schema,
                "total_relations": len(all_fks),
                "relations": all_fks
            }

    def tool_query_data(self, query: str, limit: int = 1000) -> dict:
        """Execute a SELECT query (read-only)."""
        if not query.strip().upper().startswith("SELECT"):
            return {
                "status": "error",
                "error": "Only SELECT queries are allowed. Write operations are not permitted."
            }

        client = self.active_client
        results = client.execute_query(query, limit)

        return {
            "query": query,
            "row_count": len(results),
            "limited_to": limit if len(results) >= limit else None,
            "rows": results
        }

    def tool_get_row_count(self, table_name: str, schema: Optional[str] = None) -> dict:
        """Get row count for a table."""
        client = self.active_client
        schema = self._default_schema(schema)
        count = client.get_row_count(table_name, schema)

        return {
            "table": table_name,
            "schema": schema,
            "row_count": count
        }

    def tool_get_table_statistics(self, table_name: str, schema: Optional[str] = None) -> dict:
        """Get table statistics."""
        client = self.active_client
        schema = self._default_schema(schema)
        stats = client.get_table_stats(table_name, schema)

        return {
            "table": table_name,
            "schema": schema,
            "statistics": stats
        }

    def tool_search_column(self, column_pattern: str, schema: Optional[str] = None) -> dict:
        """Search for columns by name pattern."""
        client = self.active_client
        schema = self._default_schema(schema)
        results = client.search_columns(column_pattern, schema)

        return {
            "pattern": column_pattern,
            "schema": schema,
            "matches": len(results),
            "results": results
        }

    def tool_get_enum_values(self, table_name: str, column_name: str, schema: Optional[str] = None, limit: int = 100) -> dict:
        """Get distinct values from a column."""
        client = self.active_client
        schema = self._default_schema(schema)
        values = client.get_distinct_values(table_name, column_name, schema, limit)

        return {
            "table": table_name,
            "column": column_name,
            "schema": schema,
            "distinct_count": len(values),
            "values": values
        }

    def tool_analyze_relationships(self, table_name: str, schema: Optional[str] = None, depth: int = 2) -> dict:
        """Analyze relationships between tables."""
        client = self.active_client
        schema = self._default_schema(schema)
        relationships = client.analyze_table_relationships(table_name, schema, depth)

        return {
            "table": table_name,
            "schema": schema,
            "analysis_depth": depth,
            "relationships": relationships
        }

    def tool_list_profiles(self) -> dict:
        """List datasource profiles configured in config.yaml."""
        config_path, workspace_config = self._load_workspace_config()
        datasource = workspace_config.get("datasource") or {}
        profiles = datasource.get("profiles") or {}

        return {
            "config_path": str(config_path),
            "default_profile": datasource.get("default_profile"),
            "count": len(profiles),
            "profiles": [
                {
                    "profile": profile_name,
                    "type": profile_data.get("type") or profile_data.get("engine"),
                    "server": profile_data.get("server") or profile_data.get("host"),
                    "port": profile_data.get("port"),
                    "database": profile_data.get("database") or profile_data.get("name"),
                    "schema": profile_data.get("schema"),
                }
                for profile_name, profile_data in profiles.items()
            ]
        }

    def tool_configure_profile(
        self,
        profile: str,
        type: str,
        server: str,
        database: str,
        user: str,
        password: str,
        port: Optional[int] = None,
        schema: Optional[str] = None,
        set_as_default: bool = False
    ) -> dict:
        """Create or update a datasource profile in config.yaml."""
        config_path, workspace_config = self._load_workspace_config()
        datasource = workspace_config.setdefault("datasource", {})
        profiles = datasource.setdefault("profiles", {})

        normalized_type = str(type).lower()
        resolved_port = int(port) if port is not None else (1433 if normalized_type == "sqlserver" else 5432)
        resolved_schema = schema or ("dbo" if normalized_type == "sqlserver" else "public")

        profiles[profile] = {
            "type": normalized_type,
            "server": server,
            "port": resolved_port,
            "database": database,
            "user": user,
            "password": password,
            "schema": resolved_schema,
        }

        if set_as_default or not datasource.get("default_profile"):
            datasource["default_profile"] = profile

        self._write_workspace_config(config_path, workspace_config)

        return {
            "message": f"Profile '{profile}' salvo com sucesso em config.yaml.",
            "config_path": str(config_path),
            "profile": profile,
            "default_profile": datasource.get("default_profile")
        }

    def start_server(self):
        """Start the MCP server - read requests from stdin, write responses to stdout."""
        logger.info("Starting Database MCP Server - reading from stdin")

        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break

                try:
                    request = json.loads(line)
                    response = self.process_request(request)
                    print(json.dumps(response))
                    sys.stdout.flush()
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    print(json.dumps({
                        "status": "error",
                        "error": f"Invalid JSON: {e}"
                    }))
                    sys.stdout.flush()

        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
        finally:
            if self.db_client:
                self.db_client.disconnect()
            logger.info("Server shutdown complete")

    def get_tools_info(self) -> dict:
        """Return information about all available tools."""
        return {
            "tools": {
                name: {
                    "description": info["description"]
                }
                for name, info in self.tools.items()
            }
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Database MCP Server")
    parser.add_argument("--config", type=str, default=None, help="Path to config.yaml (opcional)")
    parser.add_argument("--list-tools", action="store_true", help="List available tools and exit")

    args = parser.parse_args()

    server = DatabaseMCPServer(config_path=args.config)

    if args.list_tools:
        print(json.dumps(server.get_tools_info(), indent=2))
        return

    server.start_server()


if __name__ == "__main__":
    main()
