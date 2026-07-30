# Database MCP

Server Model Context Protocol para interagir com bases de dados PostgreSQL e SQL Server. Funciona integrado com o VS Code Chat via handoff.

Todos os artefatos gerados pelo MCP devem ser persistidos em `documentacao/banco_dados`, a partir da raiz do projeto.

## Características

- ✅ Exploração de schema (tabelas, views, colunas, índices)
- ✅ Query builder seguro (apenas SELECT)
- ✅ Análise de relacionamentos entre tabelas
- ✅ Mapeamento de keys e constraints
- ✅ Documentação de stored procedures e functions
- ✅ Busca por padrão em colunas
- ✅ Estatísticas de tabelas
- ✅ **Diagrama ER em Mermaid** gerado automaticamente em `DADOS-01-ER.md`
- ✅ Suporte para PostgreSQL e SQL Server
- ✅ Integração nativa com VS Code Chat
- ✅ **Atualização automática** do índice `documentacao/banco_dados/discovery-database.yml` e diagrama ER

## Requisitos

- Python 3.8+
- PostgreSQL 10+ ou SQL Server 2016+
- Driver ODBC 17 para SQL Server (se usar SQL Server)

## Instalação

### 1. Instalar dependências

```bash
cd src
pip install -r requirements.txt
```

### 2. Configurar credenciais

Edite `config.yaml` em `.vscode` ou `.github`.

**Exemplo:**

```yaml
datasource:
  default_profile: principal
  profiles:
    principal:
      type: postgresql
      server: localhost
      port: 5432
      database: seu_banco
      user: seu_usuario
      password: sua_senha
      schema: public
    homolog:
      type: sqlserver
      server: sql-homolog
      port: 1433
      database: seu_banco
      user: sa
      password: sua_senha
      schema: dbo
```

Se `.vscode/config.yaml` existir, ele tem prioridade. Caso contrário, o MCP usa `.github/config.yaml`.

### Exemplo de SQL Server com autenticação integrada

```yaml
datasource:
  default_profile: principal
  profiles:
    principal:
      type: sqlserver
      server: dbdev9\hml2014
      port: 1433
      database: ecompras
      schema: dbo
      integrated_security: true
```

## Uso

## Workflows operacionais

### 1. Extrair o corpo de uma procedure específica

Use este fluxo quando precisar documentar o SQL executado por uma rotina:

```bash
cd .github/skills/database-mcp/src
python mcp_server.py
```

Requisição JSON de exemplo:

```json
{
  "tool": "get_routine_code",
  "input": {
    "routine_name": "USP_PesquisaProcessosAguardandoInicio",
    "schema": "dbo",
    "profile": "principal"
  }
}
```

Resultado esperado:
- código-fonte da routine;
- tipo (`PROCEDURE`, `FUNCTION` ou `TRIGGER`);
- schema;
- metadados básicos.

Observação importante:
- em SQL Server, a extração usa `OBJECT_DEFINITION(OBJECT_ID('schema.rotina'))`;
- se a rotina estiver criptografada ou o usuário não tiver permissão de leitura da definição, o retorno pode vir vazio ou como objeto indisponível.

### 2. Mapear completamente um schema

```bash
cd .github/skills/database-mcp/src
python mcp_server.py
```

Requisição JSON:

```json
{
  "tool": "explore_schema",
  "input": {
    "schema": "dbo",
    "profile": "principal"
  }
}
```

Depois complemente com:

```json
{ "tool": "list_routines", "input": { "schema": "dbo", "profile": "principal" } }
```

```json
{ "tool": "list_indexes", "input": { "schema": "dbo", "profile": "principal" } }
```

```json
{ "tool": "list_foreign_keys", "input": { "schema": "dbo", "profile": "principal" } }
```

### 3. Executar consultas read-only seguras

```json
{
  "tool": "query_data",
  "input": {
    "profile": "principal",
    "query": "SELECT TOP 50 * FROM dbo.Processos ORDER BY PRO_IDF DESC",
    "limit": 50
  }
}
```

Para PostgreSQL:

```json
{
  "tool": "query_data",
  "input": {
    "profile": "principal",
    "query": "SELECT * FROM public.processos ORDER BY pro_idf DESC LIMIT 50",
    "limit": 50
  }
}
```

### 4. Investigar tabela e relacionamento

```json
{
  "tool": "describe_table",
  "input": {
    "profile": "principal",
    "schema": "dbo",
    "table_name": "Processos"
  }
}
```

```json
{
  "tool": "analyze_relationships",
  "input": {
    "profile": "principal",
    "schema": "dbo",
    "table_name": "Processos"
  }
}
```

## Scripts Python e responsabilidade

- `src/db_client.py`
  - encapsula conexão SQL Server / PostgreSQL;
  - executa queries `SELECT` seguras;
  - coleta tabelas, views, colunas, PK/FK e estatísticas.

- `src/mcp_server.py`
  - publica ferramentas MCP;
  - resolve profiles em `.vscode/config.yaml` ou `.github/config.yaml`;
  - mantém `documentacao/banco_dados/discovery-database.yml` sincronizado;
  - deve ser a base para qualquer investigação operacional desta skill.

## Critério de uso obrigatório em documentação

Quando esta skill for usada para apoiar documentação técnica de páginas, endpoints, jobs ou integrações, o agente deve usar os scripts Python acima para extrair evidência real do banco sempre que o SQL não estiver no repositório.
Não basta registrar a intenção de consulta: o resultado extraído deve ser refletido no documento final.

## Checklist de revisão operacional

- `list_profiles` retorna os profiles configurados corretamente.
- `explore_schema` gera ou atualiza `discovery-database.yml`.
- `get_routine_code` retorna o corpo da routine ou mensagem clara de indisponibilidade.
- `describe_table` informa colunas, PK e FKs.
- `query_data` bloqueia qualquer coisa que não seja `SELECT`.
- o diretório `documentacao/banco_dados` é usado como saída padrão dos artefatos.

## Saídas geradas

- `documentacao/banco_dados/discovery-database.yml`: índice automático do que existe no banco configurado
- `documentacao/banco_dados/DADOS-01-ER.md`: diagrama ER em formato Mermaid com tabelas, colunas, tipos e relacionamentos
- `documentacao/banco_dados/`: diretório obrigatório para qualquer documentação gerada pelo MCP
- `config.yaml`: origem dos profiles de conexão em `datasource.profiles`

Sempre que uma ferramenta de inspeção estrutural identificar alteração no schema, o MCP regrava automaticamente o arquivo `discovery-database.yml` e o diagrama ER `DADOS-01-ER.md`.

Se não houver profiles configurados, o handoff deve pedir os dados da conexão ao usuário. Se o usuário não responder, a tarefa deve ser encerrada imediatamente. Se o profile solicitado não existir, o MCP lista os profiles existentes e oferece usar um existente ou cadastrar um novo.

### Via VS Code Chat (Recomendado)

Invoque o handoff do database-mcp no seu prompt:

```
@database-mcp explore_schema schema=public
```

```
@database-mcp describe_table table_name=users schema=public
```

```
@database-mcp query_data query="SELECT * FROM users WHERE active = true"
```

### Via linha de comando

```bash
python src/mcp_server.py --list-tools
```

Saída:
```json
{
  "tools": {
    "explore_schema": {
      "description": "Explore database schema - list tables, views, and structure"
    },
    "list_tables": {
      "description": "List all tables in the specified schema"
    },
    ...
  }
}
```

### Iniciar servidor interativo

```bash
python src/mcp_server.py
```

O servidor lê requisições JSON do stdin e escreve respostas no stdout.

## Ferramentas Disponíveis

### Exploração de Schema

#### `explore_schema`
Explorar estrutura completa do schema.

**Entrada:**
```json
{
  "tool": "explore_schema",
  "input": {
    "schema": "public"
  }
}
```

**Saída:**
```json
{
  "status": "success",
  "result": {
    "schema": "public",
    "tables": 12,
    "views": 3,
    "tables_list": ["users", "orders", "products"],
    "views_list": ["active_users"]
  }
}
```

#### `list_tables`
Listar todas as tabelas em um schema.

**Entrada:**
```json
{
  "tool": "list_tables",
  "input": {
    "schema": "public"
  }
}
```

#### `describe_table`
Obter informações detalhadas de uma tabela (colunas, tipos, constraints).

**Entrada:**
```json
{
  "tool": "describe_table",
  "input": {
    "table_name": "users",
    "schema": "public"
  }
}
```

**Saída:**
```json
{
  "status": "success",
  "result": {
    "table": "users",
    "schema": "public",
    "columns": [
      {
        "column_name": "id",
        "data_type": "integer",
        "is_nullable": "NO",
        "column_default": null,
        "ordinal_position": 1
      },
      {
        "column_name": "email",
        "data_type": "character varying",
        "is_nullable": "NO",
        "column_default": null,
        "ordinal_position": 2
      }
    ],
    "primary_key": ["id"],
    "foreign_keys": [],
    "column_count": 2
  }
}
```

### Dados e Queries

#### `query_data`
Executar SELECT query (read-only).

**Entrada:**
```json
{
  "tool": "query_data",
  "input": {
    "query": "SELECT * FROM users WHERE active = true",
    "limit": 100
  }
}
```

#### `get_row_count`
Obter contagem de linhas em uma tabela.

**Entrada:**
```json
{
  "tool": "get_row_count",
  "input": {
    "table_name": "users",
    "schema": "public"
  }
}
```

#### `get_enum_values`
Obter valores distintos de uma coluna (útil para campos de status/tipo).

**Entrada:**
```json
{
  "tool": "get_enum_values",
  "input": {
    "table_name": "orders",
    "column_name": "status",
    "schema": "public",
    "limit": 50
  }
}
```

**Saída:**
```json
{
  "status": "success",
  "result": {
    "table": "orders",
    "column": "status",
    "schema": "public",
    "distinct_count": 4,
    "values": ["PENDING", "PROCESSING", "COMPLETED", "CANCELLED"]
  }
}
```

### Análise de Estrutura

#### `list_indexes`
Listar índices de uma tabela.

**Entrada:**
```json
{
  "tool": "list_indexes",
  "input": {
    "table_name": "users",
    "schema": "public"
  }
}
```

#### `list_foreign_keys`
Listar relacionamentos por chaves estrangeiras.

**Entrada:**
```json
{
  "tool": "list_foreign_keys",
  "input": {
    "table_name": "orders",
    "schema": "public"
  }
}
```

#### `analyze_relationships`
Analisar relacionamentos entre tabelas em profundidade.

**Entrada:**
```json
{
  "tool": "analyze_relationships",
  "input": {
    "table_name": "users",
    "schema": "public",
    "depth": 2
  }
}
```

#### `search_column`
Buscar colunas por padrão de nome.

**Entrada:**
```json
{
  "tool": "search_column",
  "input": {
    "column_pattern": "user_%",
    "schema": "public"
  }
}
```

### Rotinas do Banco

#### `list_routines`
Listar stored procedures, functions e triggers.

**Entrada:**
```json
{
  "tool": "list_routines",
  "input": {
    "schema": "public",
    "routine_type": "all"
  }
}
```

#### `get_routine_code`
Obter código-fonte de uma SP ou function.

**Entrada:**
```json
{
  "tool": "get_routine_code",
  "input": {
    "routine_name": "sp_process_order",
    "schema": "public",
    "routine_type": "procedure"
  }
}
```

### Estatísticas

#### `get_table_statistics`
Obter estatísticas de uma tabela (tamanho, contagem, última atualização).

**Entrada:**
```json
{
  "tool": "get_table_statistics",
  "input": {
    "table_name": "orders",
    "schema": "public"
  }
}
```

## Exemplos de Uso

### Exemplo 1: Explorar e documentar um novo schema

```
@database-mcp explore_schema schema=public
```

Resultado: lista de tabelas e views disponíveis.

### Exemplo 2: Entender estrutura de uma tabela

```
@database-mcp describe_table table_name=orders schema=public
```

Resultado: colunas, tipos, keys e constraints.

### Exemplo 3: Mapear valores de status

```
@database-mcp get_enum_values table_name=orders column_name=status
```

Resultado: todos os valores de status válidos na tabela.

### Exemplo 4: Buscar coluna por padrão

```
@database-mcp search_column column_pattern=user_% schema=public
```

Resultado: lista de colunas que começam com "user_".

### Exemplo 5: Analisar relacionamentos

```
@database-mcp analyze_relationships table_name=users depth=2
```

Resultado: tabelas que referenciam e são referenciadas.

### Exemplo 6: Executar query customizada

```
@database-mcp query_data query="SELECT COUNT(*) as usuario_count FROM users WHERE created_at > '2024-01-01'"
```

Resultado: resultado da query como lista de registros.

## Segurança

- ✅ **Apenas SELECT:** Nenhuma operação de escrita (INSERT, UPDATE, DELETE, DROP) é permitida
- ✅ **Validação de entrada:** Todas as queries são validadas antes de execução
- ✅ **Credenciais seguras:** Armazene a senha em variável de ambiente ou `.env` (não em config.json em produção)
- ⚠️ **Limite de queries:** Máximo 1000 linhas por query (configurável)

## Profiles de conexão

Os dados de conexão devem ser mantidos em `config.yaml`, sob a propriedade `datasource`.

Ferramentas auxiliares:

- `list_profiles` — lista os profiles disponíveis
- `configure_profile` — cria ou atualiza um profile em `config.yaml`

Ao executar ferramentas de banco, informe `profile` quando quiser escolher explicitamente uma conexão específica.

## Troubleshooting

### Erro: "psycopg2.OperationalError: could not connect to server"

Verifique:
- PostgreSQL está rodando?
- Credenciais estão corretas em `mcp_config.json`?
- Host e port estão corretos?

### Erro: "pyodbc.Error: ('28000', '[28000] ERROR state)"

SQL Server:
- SQL Server Browser está ativo?
- ODBC Driver 17 está instalado?
- Credenciais estão corretas?

### Timeout em query grande

Aumente o `limit` em `query_data` ou execute query mais específica com `WHERE`.

## Próximos Passos

- [ ] Adicionar suporte a MySQL/MariaDB
- [ ] Adicionar cache de schema
- [ ] Adicionar modo de gravação (auditado)
- [ ] Adicionar geração automática de diagramas ER
- [ ] Gerar documentação Markdown automaticamente em `documentacao/banco_dados`

## Licença

MIT
