#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime

def get_versioned_path(base_path: str) -> str:
    dir_name = os.path.dirname(base_path) or '.'
    base_name, ext = os.path.splitext(os.path.basename(base_path))

    if not os.path.exists(base_path):
        return base_path

    version = 1
    while True:
        versioned = os.path.join(dir_name, f"{base_name}_v{version}{ext}")
        if not os.path.exists(versioned):
            return versioned
        version += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_rdm.py <data.json> [output.md]")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        chamado = data.get('numero_chamado', 'unknown')
        output_path = f"rdm_{chamado}.md"
        output_path = get_versioned_path(output_path)

    # Load template from the skill's same directory
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'references', 'template_rdm.md')

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        sys.exit(1)

    # Basic information replacement
    template = template.replace('{{DATA_CRIACAO}}', data.get('data_criacao', datetime.now().strftime('%d/%m/%Y')))
    template = template.replace('{{NUMERO_CHAMADO}}', data.get('numero_chamado', ''))
    template = template.replace('{{ASSUNTO}}', data.get('assunto', ''))
    template = template.replace('{{ELABORACAO}}', data.get('elaboracao', ''))
    template = template.replace('{{VERSAO}}', data.get('versao', '1.0'))
    template = template.replace('{{SERVICO}}', data.get('servico', ''))
    template = template.replace('{{SOLICITANTE}}', data.get('solicitante', ''))
    template = template.replace('{{ORGAO}}', data.get('orgao', ''))
    template = template.replace('{{RESUMO}}', data.get('resumo', 'Not filled in.'))
    template = template.replace('{{SOLUCAO}}', data.get('solucao', 'Not filled in.'))
    template = template.replace('{{TREINAMENTO}}', data.get('treinamento', 'Not applicable.'))

    # Default text for Scope Not Included, if none is provided
    default_scope_text = "*The following items are not included in this estimate:*\n*Procurement of equipment or software licenses;*\n*Infrastructure or specific training materials;*\n*Post-deployment support, which will be provided through a maintenance contract.*"
    template = template.replace('{{ESCOPO_NAO_INCLUIDO}}', data.get('escopo_nao_incluido', default_scope_text))

    # Process functionality table and details
    funcionalidades = data.get('funcionalidades', [])
    if not funcionalidades:
        tabela_func = "| | |\n"
        detalhes_func = ""
    else:
        tabela_func = ""
        detalhes_func = ""
        for idx, func in enumerate(funcionalidades, 1):
            nome = func.get('nome', f'Functionality {idx}')
            descricao = func.get('descricao', '')
            tabela_func += f"| {idx} | {nome} |\n"
            detalhes_func += f"**{nome}**\n{descricao}\n\n"

    template = template.replace('{{TABELA_FUNCIONALIDADES}}', tabela_func.strip())
    template = template.replace('{{DETALHES_FUNCIONALIDADES}}', detalhes_func.strip())

    # Process risks table
    riscos = data.get('riscos', [])
    if not riscos:
        # Mandatory blank table
        tabela_riscos = "| | | |\n| | | |\n| | | |\n"
    else:
        tabela_riscos = ""
        for risco in riscos:
            tabela_riscos += f"| {risco.get('descricao', '')} | {risco.get('impacto', '')} | {risco.get('resposta', '')} |\n"

    template = template.replace('{{TABELA_RISCOS}}', tabela_riscos.strip())

    # Save generated file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"RDM generated successfully at: {output_path}")

if __name__ == '__main__':
    main()
