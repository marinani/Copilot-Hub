---
name: sonarqube-fix
description: Corrige issues do SonarQube (Code Smells, Bugs, Vulnerabilidades) consultando a API REST e aplicando correções no código fonte.
---

# SonarQube Fix

## Ativação

Quando o usuário mencionar SonarQube, issues do Sonar, qualidade de código ou análise estática:

1. **Pergunte o Project Key** se não souber (ex: `-CSDE-DOME`)
2. Siga o fluxo abaixo

## Fluxo de Correção Assistida

### 1. Buscar Issues

Use o script `scripts/sonarqube-api.ps1` para consultar a API:

```powershell
$env:SONAR_TOKEN = "<token>"

# Listar issues (com filtros opcionais)
$json = & "scripts/sonarqube-api.ps1" `
    -Action search-issues -ProjectKey "<project-key>" -Token $env:SONAR_TOKEN `
    [-Severity "CRITICAL"] [-Type "CODE_SMELL"] [-Status "OPEN,CONFIRMED"]
```

Ou diretamente via bash:

```powershell
$headers = @{Authorization = "Bearer $env:SONAR_TOKEN"; Accept = "application/json"}
$result = Invoke-RestMethod -Uri "https://sonarqube.ici.tec.br/api/issues/search?componentKeys=<project-key>&ps=50&statuses=OPEN,CONFIRMED" -Headers $headers
```

O retorno contém:
- `result.issues[]` → lista de issues
- `result.components[]` → mapeia componentKey para caminho do arquivo
- Cada issue tem: `key`, `rule`, `severity`, `type`, `component`, `line`, `message`, `textRange`, `status`

### 2. Exibir Issues ao Usuário

Para cada issue, mostre:

```
🔍 {issue.key}
   Regra:     {issue.rule}
   Tipo:      {issue.type}
   Gravidade: {issue.severity}
   Arquivo:   {component.path} (linha {issue.line})
   Mensagem:  {issue.message}
```

Extraia o `component.path` de `result.components[]` — encontre o componente cujo `key` corresponda ao `issue.component`.

### 3. Obter Detalhes + Descrição da Regra

```powershell
$detail = & "scripts/sonarqube-api.ps1" `
    -Action get-detail -IssueKey "<issue-key>" -ProjectKey "<project-key>" -Token $env:SONAR_TOKEN
```

O retorno contém:
- `detail.issue[]` → lista com 1 issue
- `detail.components[]` → componentes do projeto
- `detail.rule` → regra violada, com:
  - `detail.rule.descriptionSections[]` → seções de documentação (`how_to_fix`, `root_cause`, `resources`)
  - `detail.rule.name` → nome da regra

Extraia a descrição de `how_to_fix`:
```
$howToFix = $detail.rule.descriptionSections | Where-Object { $_.key -eq "how_to_fix" } | Select-Object -ExpandProperty content
```

### 4. Aplicar Correção (com aprovação)

Mostre o preview e aguarde aprovação do usuário:

1. **Leia o arquivo** na linha indicada
2. **Mostre o código atual** e a **sugestão de correção**
3. **Pergunte** se deseja aplicar

### 5. Padrões de Correção por Tipo de Issue

| Regra | Problema | Correção |
|-------|----------|----------|
| `csharpsquid:S100` | Naming convention | Renomear método para `camelCase` |
| `csharpsquid:S101` | Nome de classe | Renomear para `PascalCase` |
| `csharpsquid:S107` | Muitos parâmetros | Extrair parâmetros para uma classe/record |
| `csharpsquid:S112` | Exception genérica | Substituir `Exception` por exceção específica |
| `csharpsquid:S1135` | TODO comentado | Implementar ou remover o TODO |
| `csharpsquid:S1186` | Método vazio | Implementar ou remover o método |
| `csharpsquid:S125` | Código comentado | Remover bloco comentado |
| `csharpsquid:S1449` | CultureInfo | Especificar `StringComparison` ou `CultureInfo` |
| `csharpsquid:S1481` | Variável não usada | Remover a variável |
| `csharpsquid:S1854` | Atribuição não usada | Remover a atribuição morta |
| `csharpsquid:S1858` | ToString desnecessário | Remover `.ToString()` quando string já esperada |
| `csharpsquid:S2292` | Propriedade trivial | Usar `{ get; set; }` auto-implementada |
| `csharpsquid:S2325` | Método static | Adicionar `static` se não usar `this` |
| `csharpsquid:S2933` | readonly | Adicionar `readonly` em campos não modificados |
| `csharpsquid:S3267` | Loop para LINQ | Substituir loop por `.Select()` ou `.Where()` |
| `csharpsquid:S3443` | Expressão redundante | Simplificar a expressão |
| `csharpsquid:S3776` | Cognitive Complexity | Extrair blocos aninhados para métodos separados |
| `csharpsquid:S3878` | Array params | Usar `params` corretamente |
| `csharpsquid:S3881` | IDisposable | Implementar padrão Dispose corretamente |
| `csharpsquid:S3990` | Assembly visibility | Adicionar `[assembly: CLSCompliant]` |
| `csharpsquid:S3992` | Assembly description | Adicionar `[assembly: AssemblyDescription]` |
| `csharpsquid:S3993` | Assembly attributes | Adicionar atributos de assembly |

### 6. Resumo para o Usuário

Ao final, informe:
- Quantas issues foram corrigidas
- Quais arquivos foram modificados
- Quais issues precisam de revisão manual

## Referência da API

| Endpoint | Parâmetros | Descrição |
|----------|-----------|-----------|
| `GET /api/issues/search` | `componentKeys`, `severities`, `types`, `statuses`, `p`, `ps` | Buscar issues |
| `GET /api/rules/show` | `key` | Descrição completa da regra |
