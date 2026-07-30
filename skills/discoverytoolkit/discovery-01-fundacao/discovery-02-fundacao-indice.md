---
name: discovery-02-fundacao-indice
description: Gera e valida índices completos de arquivos do projeto ativo (paths lidos de discovery-project.yml) e atualiza documentos DISC relacionados. Use quando o usuário pedir para gerar, regenerar ou validar os índices de arquivos, ou quando arquivos-legado.txt / arquivos-workspace.txt estiverem desatualizados.
---

# Discovery Index

> **Antes de qualquer ação:** ler `discovery-project.yml` e extrair `paths.legado`, `paths.workspace` e `paths.indices`.

## Responsabilidade

Gerar e manter dois índices de arquivos em `discovery/`:

| Arquivo | Conteúdo |
|---|---|
| `discovery/arquivos-workspace.txt` | Todos os arquivos de `paths.workspace` (de `discovery-project.yml`) |
| `discovery/arquivos-legado.txt` | Todos os arquivos de `paths.legado` (de `discovery-project.yml`) |

## Script de regeneração

Executar o script PowerShell abaixo. Os caminhos são lidos de `discovery-project.yml` — nunca hardcodar:

```powershell
# Script de geração de índices — caminhos lidos de discovery-project.yml
# Ler discovery-workspace.yml para identificar o projeto ativo e carregar seu discovery-project.yml

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
# $raiz e $discovery devem ser obtidos de paths.workspace e paths.discovery em discovery-project.yml
$raiz      = "<paths.workspace de discovery-project.yml>"
$discovery = "<paths.discovery de discovery-project.yml>"

# Extensões relevantes para .NET
$extensoes = @("*.cs","*.cshtml","*.razor","*.json","*.xml","*.config",
               "*.yaml","*.yml","*.sql","*.csproj","*.sln","*.md",
               "*.ps1","*.sh","*.txt","*.http")

# Pastas a excluir
$excluir = @("bin","obj",".vs","TestResults",".git","node_modules",
             "dist","packages","_historico")

# Coleta arquivos
$arquivos = Get-ChildItem -Path $raiz -Recurse -File |
    Where-Object {
        $rel = $_.FullName.Substring($raiz.Length + 1)
        $partes = $rel.Split([IO.Path]::DirectorySeparatorChar)
        -not ($partes | Where-Object { $excluir -contains $_ })
    } |
    ForEach-Object { $_.FullName.Substring($raiz.Length + 1) } |
    Sort-Object

# Grava arquivos-legado.txt (fonte primária das skills)
[System.IO.File]::WriteAllLines("$discovery\arquivos-legado.txt", $arquivos, $utf8NoBom)

# Grava arquivos-workspace.txt (cópia)
[System.IO.File]::WriteAllLines("$discovery\arquivos-workspace.txt", $arquivos, $utf8NoBom)

Write-Host "Índices gerados: $($arquivos.Count) arquivos"
```

O script é **idempotente** — pode ser executado a qualquer momento sem efeitos colaterais.

## Regras dos índices

- **Incluir** arquivos `.cs`, `.cshtml`, `.razor`, `.json`, `.xml`, `.csproj`, `.sln`, `.sql`, `.yaml`, `.md`
- **Excluir**: `bin/`, `obj/`, `.vs/`, `TestResults/`, `.git/`, `node_modules/`, `packages/`, `_historico/`
- Arquivos ordenados **alfabeticamente**
- Somente **caminhos relativos** — nenhum caminho absoluto deve aparecer no conteúdo do índice

## Validações obrigatórias após geração

Após gerar os índices, verificar:

1. Nenhum caminho absoluto (ex.: `C:\`, `/projetos/`) nos arquivos `.txt`
2. Nenhum nome de repositório externo indesejado nos caminhos
3. Contagem de linhas (`(Get-Content arquivo.txt).Count`) deve ser maior que zero
4. Arquivos `.cs` presentes no índice (validação mínima para projeto .NET)

```powershell
# Validações rápidas
$idx = Get-Content "<paths.discovery de discovery-project.yml>\arquivos-legado.txt"
Write-Host "Total de arquivos indexados: $($idx.Count)"
Write-Host "Arquivos .cs: $(($idx | Select-String '\.cs$').Count)"
Write-Host "Controllers: $(($idx | Select-String 'Controller\.cs').Count)"
Write-Host "Caminhos absolutos (deve ser 0): $(($idx | Select-String '^C:\\').Count)"
```

Se qualquer validação falhar, reportar ao usuário com o trecho problemático antes de prosseguir.

## Atualização de documentos DISC

Após validação bem-sucedida, verificar se é necessário atualizar:

- **DISC-97**: confirmar que o `paths.legado` do `discovery-project.yml` está registrado como fonte primária
- **DISC-00**: confirmar que os índices constam na tabela "Onde consultar cada assunto"

## Prompt padrão

```
Leia .github/skill/discoverytoolkit/discovery - 02 - fundacao - indice/SKILL.md e gere os índices de arquivos do projeto .NET api-156.
```

---

## Passo final — Atualizar o plano

Ao concluir a geração dos artefatos desta skill, **executar obrigatoriamente** a atualização do plano de discovery:

`
Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto
`

O plano re-inspeciona o estado real da pasta discovery/ e reflete os artefatos recém-gerados, desbloqueando automaticamente a próxima onda de execução.


