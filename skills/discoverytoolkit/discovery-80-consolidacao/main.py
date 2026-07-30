"""
Skill: discovery-80-consolidacao
Objetivo: Consolidar e cruzar informações de fluxos, telas, endpoints e tabelas do Discovery Toolkit.
Saídas: consolidado.json e consolidado.md

Estratégia:
- Fluxos: lê arquivos FLUXO-FXXX-*.md individuais (extraindo CF-XXX do cabeçalho)
- Telas:  lê arquivos TELA-XXX-*.md individuais
- Tabelas: padrão `nome_tabela` em backticks (somente nomes em snake_case com underscores)
- Endpoints: padrão /api/caminho nos arquivos de tela
"""
import os
import re
import json
from collections import defaultdict
from datetime import datetime

ROOT_DISCOVERY = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
DISCOVERY_DIR = os.path.join(ROOT_DISCOVERY, 'discovery')

# Regex para identificar padrões de fluxo, tela, endpoint e tabela
# Formato tabela:       | **ID** | F001 / CF-001 |
# Formato frontmatter1: CF referência: CF-018
# Formato frontmatter2: CF: CF-030
RE_CF_ID = re.compile(r'\|\s*\*\*ID\*\*\s*\|\s*F\d+\s*/\s*(CF-\d{3})\s*\|')
RE_CF_ID_YAML = re.compile(r'^CF refer[eê]ncia:\s*(CF-\d{3})', re.MULTILINE)
RE_CF_ID_YAML2 = re.compile(r'^CF:\s*(CF-\d{3})', re.MULTILINE)
RE_CF_REF = re.compile(r'\bCF-\d{3}\b')
RE_TELA_NUM = re.compile(r'\bTELA-(\d{3})\b')
RE_ENDPOINT = re.compile(r'/api/[\w/-]+')
# Tabela: somente nomes em snake_case com ao menos um underscore ou mínimo 4 chars (excluir palavras comuns)
RE_TABELA = re.compile(r'`([a-z][a-z0-9_]{2,})`')
PALAVRAS_IGNORAR = {
    'id', 'md', 'null', 'true', 'false', 'java', 'xhtml', 'json', 'xml',
    'sql', 'ejb', 'war', 'ear', 'jar', 'jpa', 'jsf', 'seam', 'cdi',
    'string', 'long', 'int', 'boolean', 'void', 'list', 'set', 'map',
    'date', 'enum', 'class', 'bean', 'log', 'url', 'css', 'pdf',
    'get', 'set', 'add', 'put', 'run', 'new', 'use', 'all', 'any',
    'the', 'for', 'not', 'and', 'but', 'with', 'from', 'into',
    'null', 'none', 'true', 'false', 'main', 'test', 'mock', 'stub',
    'min', 'max', 'sum', 'avg', 'asc', 'desc', 'sql', 'ddl', 'dml',
    'gprev', 'ipmc', 'meta', 'sup', 'sisobi', 'comprev', 'siprev',
}

def is_tabela(nome):
    """Filtra identificadores que são provavelmente nomes de tabela (snake_case, não palavras comuns)."""
    if nome in PALAVRAS_IGNORAR:
        return False
    if len(nome) < 4:
        return False
    if '_' not in nome and nome.upper() == nome:
        return False
    return True

def find_files_by_prefix(prefix):
    """Retorna lista ordenada de arquivos no discovery/ com prefixo especificado."""
    return sorted([f for f in os.listdir(DISCOVERY_DIR) if f.startswith(prefix)])

def read_file(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()

def extract_tela_id_from_filename(filename):
    """Extrai o ID normalizado da tela a partir do nome do arquivo (ex: TELA-001)."""
    m = re.match(r'(TELA-\d{3})', filename)
    return m.group(1) if m else filename.replace('.md', '')

def build_crossmap():
    """Cria o dicionário consolidado de fluxos, telas, endpoints e tabelas."""
    fluxo_files = find_files_by_prefix('FLUXO-F')
    tela_files = find_files_by_prefix('TELA-')
    # Filtrar apenas .md
    fluxo_files = [f for f in fluxo_files if f.endswith('.md')]
    tela_files  = [f for f in tela_files  if f.endswith('.md') and re.match(r'TELA-\d{3}', f)]

    cross = {'fluxos': [], 'telas': [], 'endpoints': [], 'tabelas': []}
    tela_map = {}
    endpoint_map = defaultdict(set)
    tabela_map   = defaultdict(lambda: {'telas': set(), 'fluxos': set()})
    fluxo_map = {}

    # 1. Fluxos — lê cada arquivo FLUXO-FXXX individualmente
    for fname in fluxo_files:
        content = read_file(os.path.join(DISCOVERY_DIR, fname))
        m_id = RE_CF_ID.search(content) or RE_CF_ID_YAML.search(content) or RE_CF_ID_YAML2.search(content)
        if not m_id:
            continue
        cf_id = m_id.group(1)
        telas_num = sorted(set(RE_TELA_NUM.findall(content)))
        telas_rel = [f'TELA-{n}' for n in telas_num]
        endpoints_rel = sorted(set(RE_ENDPOINT.findall(content)))
        tabelas_rel = sorted({t for t in RE_TABELA.findall(content) if is_tabela(t)})
        cross['fluxos'].append({
            'id': cf_id,
            'arquivo': fname,
            'link': fname,
            'telas': telas_rel,
            'endpoints': endpoints_rel,
            'tabelas': tabelas_rel
        })
        fluxo_map[cf_id] = {
            'telas': set(telas_rel),
            'endpoints': set(endpoints_rel),
            'tabelas': set(tabelas_rel)
        }
        for tb in tabelas_rel:
            tabela_map[tb]['fluxos'].add(cf_id)

    # 2. Telas — lê cada arquivo TELA-XXX individualmente
    for fname in tela_files:
        tela_id = extract_tela_id_from_filename(fname)
        content = read_file(os.path.join(DISCOVERY_DIR, fname))
        fluxos_rel = sorted(set(RE_CF_REF.findall(content)))
        endpoints_rel = sorted(set(RE_ENDPOINT.findall(content)))
        tabelas_rel = sorted({t for t in RE_TABELA.findall(content) if is_tabela(t)})
        cross['telas'].append({
            'id': tela_id,
            'arquivo': fname,
            'link': fname,
            'fluxos': fluxos_rel,
            'endpoints': endpoints_rel,
            'tabelas': tabelas_rel
        })
        tela_map[tela_id] = {
            'fluxos': set(fluxos_rel),
            'endpoints': set(endpoints_rel),
            'tabelas': set(tabelas_rel)
        }
        for ep in endpoints_rel:
            endpoint_map[ep].add(tela_id)
        for tb in tabelas_rel:
            tabela_map[tb]['telas'].add(tela_id)

    # 3. Endpoints (agrupados por telas que os mencionam)
    for ep in sorted(endpoint_map):
        telas_set = sorted(endpoint_map[ep])
        tabelas_rel = sorted({tb for t in telas_set for tb in tela_map[t]['tabelas']})
        cross['endpoints'].append({
            'id': ep,
            'telas': telas_set,
            'tabelas': tabelas_rel
        })

    # 4. Tabelas (agrupadas por telas e fluxos que as mencionam)
    for tb in sorted(tabela_map):
        entry = tabela_map[tb]
        endpoints_rel = sorted({ep for t in entry['telas'] for ep in tela_map[t]['endpoints']})
        cross['tabelas'].append({
            'id': tb,
            'telas': sorted(entry['telas']),
            'endpoints': endpoints_rel,
            'fluxos': sorted(entry['fluxos'])
        })

    return cross

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_md(data, path):
    """Gera markdown navegável a partir do dicionário consolidado."""
    agora = datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = []
    lines.append('# Mapa Consolidado — Discovery Toolkit\n')
    lines.append(f'> Gerado em: {agora} | Skill: **discovery-80-consolidacao**\n')
    lines.append('---\n')

    # Sumário
    n_fluxos   = len(data['fluxos'])
    n_telas    = len(data['telas'])
    n_endpoints = len(data['endpoints'])
    n_tabelas  = len(data['tabelas'])
    lines.append('## Sumário\n')
    lines.append(f'| Artefato | Quantidade |')
    lines.append(f'|----------|-----------|')
    lines.append(f'| Fluxos (CF-XXX) | {n_fluxos} |')
    lines.append(f'| Telas (TELA-XXX) | {n_telas} |')
    lines.append(f'| Endpoints (/api/) | {n_endpoints} |')
    lines.append(f'| Tabelas | {n_tabelas} |')
    lines.append('')

    # lookup: tela_id -> nome real do arquivo
    tela_arquivo = {t['id']: t['arquivo'] for t in data['telas']}

    # Fluxos
    lines.append('## Fluxos e suas dependências\n')
    lines.append('| Fluxo | Telas | Endpoints | Tabelas |')
    lines.append('|-------|-------|-----------|---------|')
    for fluxo in data['fluxos']:
        telas_str = ', '.join(
            f'[{t}]({tela_arquivo.get(t, t + ".md")})'
            for t in fluxo['telas']
        )
        endpoints_str = ', '.join(f'`{e}`' for e in fluxo['endpoints'])
        tabelas_str = ', '.join(f'`{t}`' for t in fluxo['tabelas'])
        link = fluxo['link']
        lines.append(f"| [{fluxo['id']}]({link}) | {telas_str} | {endpoints_str} | {tabelas_str} |")
    lines.append('')

    # Telas
    lines.append('## Telas e suas dependências\n')
    lines.append('| Tela | Fluxos | Endpoints | Tabelas |')
    lines.append('|------|--------|-----------|---------|')
    for tela in data['telas']:
        fluxos_str = ', '.join(tela['fluxos'])
        endpoints_str = ', '.join(f'`{e}`' for e in tela['endpoints'])
        tabelas_str = ', '.join(f'`{t}`' for t in tela['tabelas'])
        lines.append(f"| [{tela['id']}]({tela['link']}) | {fluxos_str} | {endpoints_str} | {tabelas_str} |")
    lines.append('')

    # Endpoints
    if data['endpoints']:
        lines.append('## Endpoints e suas dependências\n')
        lines.append('| Endpoint | Telas | Tabelas |')
        lines.append('|----------|-------|---------|')
        for ep in data['endpoints']:
            telas_str = ', '.join(ep['telas'])
            tabelas_str = ', '.join(f'`{t}`' for t in ep['tabelas'])
            lines.append(f"| `{ep['id']}` | {telas_str} | {tabelas_str} |")
        lines.append('')

    # Tabelas
    lines.append('## Tabelas e suas dependências\n')
    lines.append('| Tabela | Fluxos | Telas | Endpoints |')
    lines.append('|--------|--------|-------|-----------|')
    for tb in data['tabelas']:
        fluxos_str = ', '.join(tb['fluxos'])
        telas_str = ', '.join(tb['telas'])
        endpoints_str = ', '.join(f'`{e}`' for e in tb['endpoints'])
        lines.append(f"| `{tb['id']}` | {fluxos_str} | {telas_str} | {endpoints_str} |")
    lines.append('')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    cross = build_crossmap()
    out_json = os.path.join(DISCOVERY_DIR, 'DISC-80-MAPA-CONSOLIDADO.json')
    out_md   = os.path.join(DISCOVERY_DIR, 'DISC-80-MAPA-CONSOLIDADO.md')
    save_json(cross, out_json)
    save_md(cross, out_md)
    n = lambda k: len(cross[k])
    print(f"Consolidação gerada: {out_json} e {out_md}")
    print(f"  Fluxos: {n('fluxos')} | Telas: {n('telas')} | Endpoints: {n('endpoints')} | Tabelas: {n('tabelas')}")

if __name__ == '__main__':
    main()
