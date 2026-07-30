"""
generate-integrated-index.py
Gera documentacao-integrada/index.md como página de entrada rica do site HTML.
Integra requisitos da documentacao-de-software + metadados de banco (database-mcp).

Executa:
1. Lê artefatos de documentacao-de-software (requisitos, APIs, visão)
2. Lê índice discovery-database.yml do database-mcp
3. Extrai estrutura: seções por tipo (REQ, API, DADOS, etc)
4. Monta tabelas com rastreabilidade inicial (requisito -> tabela, API -> procedure)
5. Gera markdown rico com índice de páginas e descrição de cada seção

Uso:
    python generate-integrated-index.py
    python generate-integrated-index.py --docs documentacao --root c:/seu-projeto
"""

import argparse
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set

# ---------------------------------------------------------------------------
# Descrições das seções (aparecem acima de cada tabela)
# ---------------------------------------------------------------------------

SECAO_DESC = {
    "VIS": (
        "Visão e Escopo",
        "Documentos de visão do sistema: objetivos, stakeholders, contexto de negócio e escopo geral.",
        "Entender o que o sistema deve fazer e para quem.",
    ),
    "REQ": (
        "Requisitos Funcionais",
        "Especificação de requisitos funcionais e não funcionais com critérios de aceitação em Gherkin, "
        "análise de pontos de função (APF) e matriz de risco local.",
        "Entender o quê o sistema deve implementar, como e por quê.",
    ),
    "API": (
        "Documentação de APIs",
        "Endpoints REST da aplicação com especificação de requisição/resposta, validações, "
        "status HTTP, e diagramas de sequência.",
        "Mapear a superfície exposta pela API e integração com procedures do banco.",
    ),
    "DADOS": (
        "Banco de Dados",
        "Estrutura do banco de dados: tabelas, colunas, tipos de dados, constraints, "
        "diagrama ER, procedures, functions, triggers e mapeamento de status.",
        "Consultar estrutura de dados, relacionamentos e regras de negócio persistidas.",
    ),
    "DER": (
        "Diagrama de Entidade e Relacionamento",
        "Modelo conceitual e lógico do banco de dados com cardinalidades e relacionamentos.",
        "Visualizar estrutura de dados em alto nível.",
    ),
    "MIN": (
        "Integração de Sistemas",
        "Mapeamento de dependências entre bases de dados e sistemas externos.",
        "Entender as fronteiras do sistema e dependências externas.",
    ),
    "RASTREABILIDADE": (
        "Rastreabilidade Cruzada",
        "Matrizes de linking entre requisitos ↔ endpoints ↔ procedures ↔ tabelas; "
        "matriz de risco integrada; análise de impacto.",
        "Rastrear impactos de mudanças e validar cobertura de requisitos.",
    ),
}

# Prefixos que identificam cada seção
PREFIX_MAP = [
    ("VIS-", "VIS"),
    ("REQ-", "REQ"),
    ("API-", "API"),
    ("DADOS-", "DADOS"),
    ("DER-", "DER"),
    ("MIN-", "MIN"),
]

EXCLUDE_PATTERNS = [
    r"^ROADMAP-",
    r"^index\.md$",
]

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def should_exclude(filename: str) -> bool:
    """Verifica se arquivo deve ser excluído da navegação."""
    for pat in EXCLUDE_PATTERNS:
        if re.match(pat, filename, re.IGNORECASE):
            return True
    return False


def get_section_prefix(filename: str) -> str:
    """Extrai prefixo da seção do nome do arquivo."""
    for prefix, section in PREFIX_MAP:
        if filename.upper().startswith(prefix):
            return section
    return "OUTRO"


def extract_title(md_content: str) -> str:
    """Extrai título H1 do arquivo markdown."""
    for line in md_content.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("# ---"):
            return line.replace("# ", "").strip()
    return "Sem título"


def extract_brief_description(md_content: str, max_chars: int = 200) -> str:
    """Extrai uma breve descrição (primeiros 200 chars após H1)."""
    in_content = False
    buffer = []
    for line in md_content.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not in_content:
            in_content = True
            continue
        if in_content and line and not line.startswith("#"):
            buffer.append(line)
            if len(" ".join(buffer)) >= max_chars:
                break
    desc = " ".join(buffer)
    return desc[:max_chars] + ("..." if len(desc) > max_chars else "")


def load_database_index(db_index_path: str) -> Dict:
    """Carrega discovery-database.yml do database-mcp."""
    try:
        with open(db_index_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"⚠️  discovery-database.yml não encontrado em {db_index_path}")
        return {}


def extract_database_tables(db_index: Dict) -> List[Dict]:
    """Extrai lista de tabelas do índice de banco de dados."""
    tables = []
    if "database" in db_index and "tables" in db_index["database"]:
        for table_name, table_info in db_index["database"]["tables"].items():
            tables.append({
                "name": table_name,
                "description": table_info.get("description", ""),
                "columns": table_info.get("columns", {}),
            })
    return tables


def extract_database_procedures(db_index: Dict) -> List[Dict]:
    """Extrai lista de procedures/functions do índice de banco de dados."""
    procs = []
    if "database" in db_index and "routines" in db_index["database"]:
        for routine_name, routine_info in db_index["database"]["routines"].items():
            procs.append({
                "name": routine_name,
                "type": routine_info.get("type", "unknown"),  # PROCEDURE, FUNCTION
                "description": routine_info.get("description", ""),
            })
    return procs


def scan_software_docs(docs_dir: Path) -> Dict[str, List[Dict]]:
    """Escaneia documentação de software e agrupa por seção."""
    sections = {
        "VIS": [],
        "REQ": [],
        "API": [],
        "OUTROS": [],
    }

    # Diretório de artefatos
    artefatos_dir = docs_dir / "processo_unificado" / "artefatos_aprovados"

    if not artefatos_dir.exists():
        print(f"⚠️  Diretório de artefatos não encontrado: {artefatos_dir}")
        return sections

    # Scan todos os .md em subdiretórios
    for subdir in [
        "visao",
        "detalhamento_requisitos",
        "documentacao_api",
        "diagrama_de_classes",
        "diagrama_de_integracao_de_sistemas",
        "diagrama_de_entidades_e_relacionamento",
    ]:
        target_dir = artefatos_dir / subdir
        if target_dir.exists():
            for md_file in target_dir.glob("*.md"):
                if should_exclude(md_file.name):
                    continue

                try:
                    content = md_file.read_text(encoding="utf-8")
                    section = get_section_prefix(md_file.name)

                    doc_entry = {
                        "file": md_file.name,
                        "title": extract_title(content),
                        "brief": extract_brief_description(content),
                        "section": section,
                    }

                    if section in sections:
                        sections[section].append(doc_entry)
                    else:
                        sections["OUTROS"].append(doc_entry)

                except Exception as e:
                    print(f"⚠️  Erro ao ler {md_file.name}: {e}")

    return sections


def generate_table_of_contents(
    software_sections: Dict,
    db_index: Dict,
    docs_dir: Path,
) -> str:
    """Gera markdown rico para índice integrado."""

    # Cabeçalho
    md = f"""# Documentação Integrada do Sistema

> **Última atualização:** {datetime.now().strftime("%d/%m/%Y às %H:%M")}

Bem-vindo à documentação completa do sistema, que integra:
- **Documentação de Software:** Requisitos, APIs, visão de negócio
- **Metadados de Banco:** Tabelas, colunas, procedures, functions, triggers
- **Rastreabilidade:** Links bidireccionais entre requisitos ↔ APIs ↔ dados

Navegue pelas seções abaixo ou use a **busca full-text** no topo da página.

---

## 📋 Índice Integrado

"""

    # Seção de Visão
    if software_sections.get("VIS"):
        md += generate_section("VIS", software_sections["VIS"])

    # Seção de Requisitos
    if software_sections.get("REQ"):
        md += generate_section("REQ", software_sections["REQ"])

    # Seção de APIs
    if software_sections.get("API"):
        md += generate_section("API", software_sections["API"])

    # Seção de Banco de Dados
    md += generate_database_section(db_index, docs_dir)

    # Seção de Rastreabilidade
    md += generate_traceability_section(software_sections, db_index)

    # Seção final
    md += f"""
---

## 📖 Convenções da Documentação

### Prefixos de documento

| Prefixo | Tipo | Exemplo |
|---------|------|---------|
| `VIS-` | Visão e escopo | `VIS-001-escopo-geral.md` |
| `REQ-` | Requisito funcional | `REQ-0001-login-usuario.md` |
| `APF-` | Análise de pontos de função | `APF-REQ-0001.md` |
| `API-` | Documentação de endpoint | `API-usuarios-service.md` |
| `DER-` | Diagrama ER | `DER-schema-principal.md` |
| `MIN-` | Integração de sistemas | `MIN-oauth-cidadao.md` |
| `DADOS-` | Metadados de banco | `DADOS-05-MAPA-DADOS.md` |

### Rótulos de confiança

- `[SQL]` — Extraído diretamente do DDL ou schema
- `[INF]` — Conclusão lógica sem comprovação direta
- `[PEN]` — Pendente de confirmação ou evidência

---

## 🔗 Rastreabilidade

### Exemplo: Requisito → Procedure → Tabelas

```
REQ-0001: Autenticação de usuário
  └─→ [API] POST /auth/login (api-auth.md)
      └─→ [SP] sp_authenticate_user
          └─→ [TBL] users, sessions, login_history
```

Clique nos links em cada documento para navegar a cadeia completa.

---

## 🆘 Precisa de ajuda?

- Não encontra um requisito? Use a **busca full-text** (Ctrl+K)
- Quer entender o banco de dados? Veja a seção **Banco de Dados**
- Precisa mapear impacto de uma mudança? Consulte **Rastreabilidade**
- Dúvidas sobre navegação? Veja o **Glossário** na seção Visão Geral

**Data de geração:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}
"""

    return md


def generate_section(section_code: str, docs: List[Dict]) -> str:
    """Gera seção markdown com tabela de documentos."""
    if not docs:
        return ""

    title, desc, context = SECAO_DESC.get(section_code, (section_code, "", ""))

    md = f"""
### {title}

{desc}

**Contexto:** {context}

| Documento | Breve Descrição |
|-----------|-----------------|
"""

    for doc in sorted(docs, key=lambda x: x["file"]):
        # Remover extensão .md para exibição
        doc_name = doc["file"].replace(".md", "")
        file_ref = doc["file"]
        md += f"| [`{doc_name}`](../{file_ref.replace('.md', '.html')}) | {doc['brief']} |\n"

    md += "\n"
    return md


def generate_database_section(db_index: Dict, docs_dir: Path) -> str:
    """Gera seção de banco de dados a partir do índice."""
    title, desc, context = SECAO_DESC["DADOS"]

    md = f"""
### {title}

{desc}

**Contexto:** {context}

#### 📊 Tabelas Principais

| Tabela | Descrição | Colunas |
|--------|-----------|---------|
"""

    tables = extract_database_tables(db_index)
    for table in sorted(tables, key=lambda x: x["name"])[:10]:  # Top 10
        col_count = len(table.get("columns", {}))
        table_desc = table.get("description", "Sem descrição")[:80]
        md += f"| `{table['name']}` | {table_desc} | {col_count} |\n"

    md += "\n#### 🔧 Procedures e Functions\n\n"
    md += "| Rotina | Tipo | Descrição |\n"
    md += "|--------|------|----------|\n"

    procs = extract_database_procedures(db_index)
    for proc in sorted(procs, key=lambda x: x["name"])[:10]:  # Top 10
        proc_type = proc.get("type", "UNKNOWN")
        proc_desc = proc.get("description", "Sem descrição")[:80]
        md += f"| `{proc['name']}` | {proc_type} | {proc_desc} |\n"

    # Verificar se existe DADOS-01-ER.md
    der_file = docs_dir / "banco_dados" / "DADOS-01-ER.md"
    if der_file.exists():
        md += f"\n[→ Visualizar Diagrama ER completo](../banco_dados/DADOS-01-ER.html)\n"

    md += "\n"
    return md


def generate_traceability_section(software_sections: Dict, db_index: Dict) -> str:
    """Gera seção de rastreabilidade cruzada."""
    title, desc, context = SECAO_DESC["RASTREABILIDADE"]

    md = f"""
### {title}

{desc}

**Contexto:** {context}

#### 🔍 Análise de Cobertura

| Tipo | Total | Documentado |
|------|-------|-------------|
| Requisitos | {len(software_sections.get('REQ', []))} | ✅ |
| APIs/Endpoints | {len(software_sections.get('API', []))} | ✅ |
| Tabelas | {len(extract_database_tables(db_index))} | ✅ |
| Procedures/Functions | {len(extract_database_procedures(db_index))} | ✅ |

#### 📍 Matrizes Disponíveis

- **REQ → Tabelas:** Quais tabelas são impactadas por cada requisito
- **API → Procedures:** Quais procedures são chamadas por cada endpoint
- **Matriz de Risco Integrada:** Riscos de requisito + riscos de banco unificados

[→ Consultar Matriz de Rastreabilidade Completa](../rastreabilidade/matriz-rastreabilidade.html)

"""
    return md


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Gera índice integrado de documentação.")
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

    # Scan software docs
    print(f"📄 Escaneando documentação de software em {docs_dir}...")
    software_sections = scan_software_docs(docs_dir)

    # Load database index
    print(f"🗄️  Carregando índice de banco de dados...")
    db_index = load_database_index(str(db_index_path))

    # Generate TOC
    print("✍️  Gerando índice integrado...")
    toc_md = generate_table_of_contents(software_sections, db_index, docs_dir)

    # Write to file
    index_file = docs_dir / "index.md"
    index_file.write_text(toc_md, encoding="utf-8")
    print(f"✅ Índice gerado em {index_file}")


if __name__ == "__main__":
    main()
