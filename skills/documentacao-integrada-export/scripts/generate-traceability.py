"""
generate-traceability.py
Gera matriz de rastreabilidade cruzada entre requisitos, APIs, procedures e tabelas.

Executa:
1. Lê requisitos em documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/
2. Lê documentação de API em documentacao/processo_unificado/artefatos_aprovados/documentacao_api/
3. Lê índice de banco de dados (discovery-database.yml)
4. Usa heurística textual para detectar referências (table_name, sp_nome, etc)
5. Gera matriz markdown com links cruzados

Heurística:
- Requisito → Tabela: busca por `table_name` ou `{table_name}` (case-insensitive)
- Requisito → Procedure: busca por `sp_*`, `proc_*`, `fn_*` (case-insensitive)
- API → Procedure: busca em documentação de endpoint
- Matriz de risco integrada: combina riscos do requisito + riscos das tabelas/procedures

Uso:
    python generate-traceability.py
    python generate-traceability.py --docs documentacao --root c:/seu-projeto
"""

import argparse
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# ---------------------------------------------------------------------------
# Padrões de detecção de referências
# ---------------------------------------------------------------------------

PATTERN_TABLE = re.compile(r'\b([a-z_][a-z0-9_]*)\b', re.IGNORECASE)
PATTERN_PROCEDURE = re.compile(r'\b(sp_|proc_|fn_)([a-z_][a-z0-9_]*)\b', re.IGNORECASE)
PATTERN_ENDPOINT = re.compile(r'(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-{}]+)', re.IGNORECASE)

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def load_database_index(db_index_path: str) -> Dict:
    """Carrega discovery-database.yml do database-mcp."""
    try:
        with open(db_index_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def extract_tables_from_index(db_index: Dict) -> Set[str]:
    """Extrai nomes de todas as tabelas do índice."""
    tables = set()
    if "database" in db_index and "tables" in db_index["database"]:
        tables.update(db_index["database"]["tables"].keys())
    return tables


def extract_procedures_from_index(db_index: Dict) -> Set[str]:
    """Extrai nomes de todas as procedures/functions do índice."""
    procs = set()
    if "database" in db_index and "routines" in db_index["database"]:
        procs.update(db_index["database"]["routines"].keys())
    return procs


def find_referenced_tables(text: str, all_tables: Set[str]) -> Set[str]:
    """Encontra referências a tabelas no texto."""
    found = set()
    text_lower = text.lower()

    # Busca por padrões comuns
    for table in all_tables:
        # Buscar: `table_name`, {table_name}, table_name (com limites)
        patterns = [
            rf'\`{re.escape(table)}\`',
            rf'{{\s*{re.escape(table)}\s*}}',
            rf'\b{re.escape(table)}\b',
        ]
        for pat in patterns:
            if re.search(pat, text_lower, re.IGNORECASE):
                found.add(table)
                break

    return found


def find_referenced_procedures(text: str, all_procs: Set[str]) -> Set[str]:
    """Encontra referências a procedures/functions no texto."""
    found = set()
    text_lower = text.lower()

    for proc in all_procs:
        # Buscar: `sp_name`, {sp_name}, sp_name (com limites)
        patterns = [
            rf'\`{re.escape(proc)}\`',
            rf'{{\s*{re.escape(proc)}\s*}}',
            rf'\b{re.escape(proc)}\b',
        ]
        for pat in patterns:
            if re.search(pat, text_lower, re.IGNORECASE):
                found.add(proc)
                break

    return found


def scan_requirements(docs_dir: Path, db_index: Dict) -> Dict[str, Dict]:
    """Escaneia requisitos e extrai referências."""
    req_dir = docs_dir / "processo_unificado" / "artefatos_aprovados" / "detalhamento_requisitos"

    all_tables = extract_tables_from_index(db_index)
    all_procs = extract_procedures_from_index(db_index)

    requirements = {}

    if not req_dir.exists():
        print(f"⚠️  Diretório de requisitos não encontrado: {req_dir}")
        return requirements

    for req_file in req_dir.glob("req-*.md"):
        try:
            content = req_file.read_text(encoding="utf-8")

            req_id = req_file.stem  # ex: req-0001-login

            # Extrair título
            title = "Sem título"
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break

            # Encontrar referências
            tables = find_referenced_tables(content, all_tables)
            procedures = find_referenced_procedures(content, all_procs)

            requirements[req_id] = {
                "title": title,
                "file": req_file.name,
                "tables": tables,
                "procedures": procedures,
            }

        except Exception as e:
            print(f"⚠️  Erro ao processar {req_file.name}: {e}")

    return requirements


def scan_apis(docs_dir: Path, db_index: Dict) -> Dict[str, Dict]:
    """Escaneia APIs e extrai referências."""
    api_dir = docs_dir / "processo_unificado" / "artefatos_aprovados" / "documentacao_api"

    all_tables = extract_tables_from_index(db_index)
    all_procs = extract_procedures_from_index(db_index)

    apis = {}

    if not api_dir.exists():
        return apis

    for api_file in api_dir.glob("*.md"):
        try:
            content = api_file.read_text(encoding="utf-8")

            api_key = api_file.stem

            # Extrair título
            title = "API"
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break

            # Extrair endpoints
            endpoints = re.findall(PATTERN_ENDPOINT, content)

            # Encontrar referências
            tables = find_referenced_tables(content, all_tables)
            procedures = find_referenced_procedures(content, all_procs)

            apis[api_key] = {
                "title": title,
                "file": api_file.name,
                "endpoints": endpoints,
                "tables": tables,
                "procedures": procedures,
            }

        except Exception as e:
            print(f"⚠️  Erro ao processar {api_file.name}: {e}")

    return apis


def generate_requirement_to_table_matrix(
    requirements: Dict[str, Dict],
    db_index: Dict,
) -> str:
    """Gera matriz de rastreabilidade: Requisito → Tabelas."""

    md = """# Matriz: Requisitos → Tabelas

Rastreia quais tabelas do banco de dados são impactadas por cada requisito.

| Requisito | Tabelas Impactadas | Tipo | Status |
|-----------|-------------------|------|--------|
"""

    for req_id, req_info in sorted(requirements.items()):
        if req_info["tables"]:
            table_list = ", ".join([f"`{t}`" for t in sorted(req_info["tables"])])
            md += f"| [{req_info['title']}]({req_info['file'].replace('.md', '.html')}) | {table_list} | Leitura/Escrita | ✅ |\n"
        else:
            md += f"| [{req_info['title']}]({req_info['file'].replace('.md', '.html')}) | (nenhuma) | — | ⚠️ |\n"

    md += "\n**Legenda:**\n"
    md += "- ✅ Tabelas identificadas e documentadas\n"
    md += "- ⚠️ Requisito sem referência explícita a tabelas (verificar se é correto)\n"
    md += "- 🔴 Tabela referenciada não existe no banco\n"

    return md


def generate_api_to_procedure_matrix(
    apis: Dict[str, Dict],
) -> str:
    """Gera matriz de rastreabilidade: APIs → Procedures."""

    md = """# Matriz: APIs → Procedures

Rastreia quais procedures/functions são chamadas por cada endpoint.

| Endpoint | Método | Procedures | Status |
|----------|--------|-----------|--------|
"""

    for api_key, api_info in sorted(apis.items()):
        if api_info["endpoints"]:
            for method, path in api_info["endpoints"]:
                procs_list = ", ".join([f"`{p}`" for p in sorted(api_info["procedures"])]) if api_info["procedures"] else "(nenhuma)"
                status = "✅" if api_info["procedures"] else "⚠️"
                md += f"| `{path}` | {method} | {procs_list} | {status} |\n"
        else:
            md += f"| {api_info['title']} | — | (não especificado) | ⚠️ |\n"

    md += "\n"
    return md


def generate_procedure_to_table_matrix(
    db_index: Dict,
) -> str:
    """Gera matriz: Procedures → Tabelas (a partir do índice)."""

    md = """# Matriz: Procedures → Tabelas

Rastreia quais tabelas são acessadas por cada procedure/function.

| Procedure | Tipo | Tabelas Referenciadas | Status |
|-----------|------|----------------------|--------|
"""

    if "database" in db_index and "routines" in db_index["database"]:
        for proc_name, proc_info in sorted(db_index["database"]["routines"].items()):
            tables = proc_info.get("referenced_tables", [])
            table_list = ", ".join([f"`{t}`" for t in sorted(tables)]) if tables else "(automático)"
            proc_type = proc_info.get("type", "PROCEDURE")
            status = "📋" if tables else "ⓘ"
            md += f"| `{proc_name}` | {proc_type} | {table_list} | {status} |\n"

    md += "\n**Legenda:**\n"
    md += "- 📋 Procedure com referências de tabelas extraídas\n"
    md += "- ⓘ Procedure sem metadados de tabelas (pode ser read-only ou resultado de análise)\n"

    return md


def generate_integrated_risk_matrix(
    requirements: Dict[str, Dict],
    db_index: Dict,
    docs_dir: Path,
) -> str:
    """Gera matriz de risco integrada: Requisito + Banco."""

    md = """# Matriz de Risco Integrada

Consolida riscos de requisito, banco de dados, procedures e tabelas impactadas.

## Visão Consolidada

| Requisito | Risco do Requisito | Tabelas Impactadas | Risco de Banco | Risco Integrado |
|-----------|-------------------|-------------------|----------------|-----------------|
"""

    for req_id, req_info in sorted(requirements.items()):
        # Buscar matriz de risco local no arquivo req-*.md
        req_file = docs_dir / "processo_unificado" / "artefatos_aprovados" / "detalhamento_requisitos" / req_info["file"]
        req_risk = "Médio"  # default

        try:
            content = req_file.read_text(encoding="utf-8")
            # Buscar seção "Matriz de Risco" ou similar
            if "risco" in content.lower():
                req_risk = "Alto" if "crítico" in content.lower() else "Médio"
        except:
            pass

        tables_list = ", ".join(sorted(req_info["tables"])) if req_info["tables"] else "—"
        bank_risk = "Baixo"  # simplificado

        # Risk consolidation
        if req_risk == "Alto" or bank_risk == "Alto":
            integrated = "🔴 Alto"
        elif req_risk == "Médio" or bank_risk == "Médio":
            integrated = "🟡 Médio"
        else:
            integrated = "🟢 Baixo"

        md += f"| {req_id} | {req_risk} | `{tables_list}` | {bank_risk} | {integrated} |\n"

    md += "\n"
    return md


def generate_impact_analysis(
    requirements: Dict[str, Dict],
) -> str:
    """Gera análise de impacto por tabela."""

    # Invertendo: agrupa tabelas por requisito
    table_map = defaultdict(list)
    for req_id, req_info in requirements.items():
        for table in req_info["tables"]:
            table_map[table].append(req_id)

    md = """# Análise de Impacto por Tabela

Mostra quais requisitos dependem de cada tabela.

| Tabela | Requisitos que Dependem | Conta |
|--------|------------------------|-------|
"""

    for table in sorted(table_map.keys()):
        req_list = ", ".join(sorted(table_map[table]))
        md += f"| `{table}` | {req_list} | {len(table_map[table])} |\n"

    md += "\n"
    return md


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Gera matriz de rastreabilidade cruzada.")
    parser.add_argument(
        "--docs",
        default="documentacao",
        help="Diretório de documentação (default: documentacao)",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Raiz do projeto (default: .)",
    )

    args = parser.parse_args()

    root_path = Path(args.root)
    docs_dir = root_path / args.docs
    db_index_path = docs_dir / "banco_dados" / "discovery-database.yml"

    # Validações
    if not docs_dir.exists():
        print(f"❌ Pasta documentacao não encontrada: {docs_dir}")
        sys.exit(1)

    # Load database index
    print("🗄️  Carregando índice de banco de dados...")
    db_index = load_database_index(str(db_index_path))

    # Scan requirements
    print("📋 Escaneando requisitos...")
    requirements = scan_requirements(docs_dir, db_index)

    # Scan APIs
    print("🔌 Escaneando APIs...")
    apis = scan_apis(docs_dir, db_index)

    # Generate matrices
    print("✍️  Gerando matrizes de rastreabilidade...")

    output_dir = docs_dir / "rastreabilidade"
    output_dir.mkdir(exist_ok=True)

    # 1. Req -> Table
    matrix_req_table = generate_requirement_to_table_matrix(requirements, db_index)
    (output_dir / "01-requisitos-tabelas.md").write_text(
        f"# Rastreabilidade: Requisitos ↔ Tabelas\n\n{matrix_req_table}\n",
        encoding="utf-8"
    )
    print("✅ 01-requisitos-tabelas.md")

    # 2. API -> Procedure
    matrix_api_proc = generate_api_to_procedure_matrix(apis)
    (output_dir / "02-apis-procedures.md").write_text(
        f"# Rastreabilidade: APIs ↔ Procedures\n\n{matrix_api_proc}\n",
        encoding="utf-8"
    )
    print("✅ 02-apis-procedures.md")

    # 3. Procedure -> Table
    matrix_proc_table = generate_procedure_to_table_matrix(db_index)
    (output_dir / "03-procedures-tabelas.md").write_text(
        f"# Rastreabilidade: Procedures ↔ Tabelas\n\n{matrix_proc_table}\n",
        encoding="utf-8"
    )
    print("✅ 03-procedures-tabelas.md")

    # 4. Integrated Risk
    matrix_risk = generate_integrated_risk_matrix(requirements, db_index, docs_dir)
    (output_dir / "04-matriz-risco-integrada.md").write_text(
        f"# Matriz de Risco Integrada\n\n{matrix_risk}\n",
        encoding="utf-8"
    )
    print("✅ 04-matriz-risco-integrada.md")

    # 5. Impact Analysis
    impact = generate_impact_analysis(requirements)
    (output_dir / "05-analise-impacto.md").write_text(
        f"# Análise de Impacto\n\n{impact}\n",
        encoding="utf-8"
    )
    print("✅ 05-analise-impacto.md")

    print(f"\n✅ Todas as matrizes geradas em {output_dir}")


if __name__ == "__main__":
    main()
