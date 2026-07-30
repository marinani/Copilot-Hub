"""
CLI utilitário para operação local da skill database-mcp.

Permite:
- explorar schema;
- descrever tabelas;
- listar rotinas;
- obter corpo de procedure/function/trigger;
- executar SELECT read-only com limite.
"""

import argparse
import json
from pathlib import Path

from mcp_server import DatabaseMCPServer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Database MCP CLI")
    parser.add_argument("tool", help="Ferramenta a executar")
    parser.add_argument("--profile", help="Profile configurado no config.yaml")
    parser.add_argument("--schema", help="Schema alvo")
    parser.add_argument("--table", help="Nome da tabela")
    parser.add_argument("--routine", help="Nome da routine")
    parser.add_argument("--query", help="Consulta SELECT read-only")
    parser.add_argument("--limit", type=int, default=100, help="Limite de linhas")
    parser.add_argument("--config", help="Caminho opcional para config.yaml")
    return parser


def build_input(args: argparse.Namespace) -> dict:
    payload = {}
    if args.profile:
        payload["profile"] = args.profile
    if args.schema:
        payload["schema"] = args.schema
    if args.table:
        payload["table_name"] = args.table
    if args.routine:
        payload["routine_name"] = args.routine
    if args.query:
        payload["query"] = args.query
    if args.limit:
        payload["limit"] = args.limit
    return payload


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    server = DatabaseMCPServer(config_path=args.config)
    tool_input = build_input(args)
    result = server.process_request({
        "tool": args.tool,
        "input": tool_input,
    })
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
