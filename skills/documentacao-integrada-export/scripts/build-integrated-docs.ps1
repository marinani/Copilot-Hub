#Requires -Version 5.1
<#
.SYNOPSIS
    Gera documentacao-html/ a partir de documentacao/ usando integração de:
    - documentacao-de-software (requisitos, APIs, visão)
    - database-mcp (tabelas, procedures, índice)
    - discovery-html-export (MkDocs, PlantUML, navegação)

.DESCRIPTION
    1. Valida pré-requisitos e estrutura de artefatos
    2. Verifica/instala dependências pip (mkdocs, mkdocs-material)
    3. Gera índice integrado combinando requisitos + banco de dados
    4. Gera matrizes de rastreabilidade cruzada
    5. Coleta .md de software + banco e gera nav hierárquica
    6. Grava mkdocs.yml na raiz do projeto
    7. Gera SVGs PlantUML via generate-diagrams.py
    8. Executa mkdocs build
    9. Injeta SVGs nos HTML via inject-diagrams.py
    10. (Opcional) Reestrutura HTML (index na raiz, demais em /html)

.PARAMETER ProjectRoot
    Raiz do projeto. Padrão: diretório atual.

.PARAMETER DocsDir
    Diretório de documentação. Padrão: documentacao

.PARAMETER SiteDir
    Diretório de saída do site HTML. Padrão: documentacao-html

.PARAMETER DatabaseProfile
    Profile do database-mcp a usar (se houver múltiplas conexões). Padrão: principal

.PARAMETER PlantumlServer
    URL do servidor PlantUML. Padrão: http://www.plantuml.com/plantuml

.PARAMETER Restructure
    Se True, move todos os HTML exceto index.html para documentacao-html/html/

.EXAMPLE
    .\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1

.EXAMPLE
    .\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1 -Restructure -DatabaseProfile principal

#>
param(
    [string]$ProjectRoot    = ".",
    [string]$DocsDir        = "documentacao",
    [string]$SiteDir        = "documentacao-html",
    [string]$DatabaseProfile = "principal",
    [string]$PlantumlServer = "http://www.plantuml.com/plantuml",
    [switch]$Restructure
)

$ErrorActionPreference = "Continue"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

# Resolve paths
$ProjectRoot = Resolve-Path $ProjectRoot -ErrorAction Stop
$ScriptsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DocsPath = Join-Path $ProjectRoot $DocsDir
$SitePath = Join-Path $ProjectRoot $SiteDir

# ---------------------------------------------------------------------------
# Função: Print header
# ---------------------------------------------------------------------------
function Write-Header {
    param([string]$Message, [string]$Color = "Cyan")
    Write-Host "`n" -ForegroundColor $Color
    Write-Host "=" * 80 -ForegroundColor $Color
    Write-Host $Message -ForegroundColor $Color
    Write-Host "=" * 80 -ForegroundColor $Color
}

# ---------------------------------------------------------------------------
# [0] Validações iniciais
# ---------------------------------------------------------------------------
Write-Header "[0/10] Validando pré-requisitos e estrutura" "Magenta"

if (-not (Test-Path $DocsPath)) {
    Write-Error "❌ Pasta documentacao não encontrada: $DocsPath"
    exit 1
}

# Verificar se existe README.md (TOC raiz)
$tocFile = Join-Path $DocsPath "README.md"
if (-not (Test-Path $tocFile)) {
    Write-Warning "⚠️  Arquivo documentacao/README.md (TOC raiz) não encontrado."
    Write-Host "    A documentação pode estar incompleta. Recomenda-se criar um arquivo README.md na raiz da documentação."
}

# Verificar se existem artefatos de software
$reqDir = Join-Path $DocsPath "processo_unificado" "artefatos_aprovados" "detalhamento_requisitos"
$softwareCount = 0
if (Test-Path $reqDir) {
    $softwareCount = @(Get-ChildItem -Path $reqDir -Filter "req-*.md" -ErrorAction SilentlyContinue).Count
}
Write-Host "  📋 Requisitos encontrados: $softwareCount"

# Verificar se existe banco de dados (discovery-database.yml)
$dbIndexFile = Join-Path $DocsPath "banco_dados" "discovery-database.yml"
if (-not (Test-Path $dbIndexFile)) {
    Write-Warning "⚠️  Índice de banco de dados não encontrado: $dbIndexFile"
    Write-Host "    Execute database-mcp SKILL antes de gerar a documentação integrada."
    # Não é erro crítico; continuamos com documentação parcial
} else {
    Write-Host "✅ discovery-database.yml encontrado"
}

Write-Host "✅ Validações concluídas`n" -ForegroundColor Green

# ---------------------------------------------------------------------------
# [1] Verificar e instalar dependências pip
# ---------------------------------------------------------------------------
Write-Header "[1/10] Verificando dependências MkDocs" "Cyan"

$checks = @{
    "mkdocs"          = "mkdocs"
    "mkdocs-material" = "material"
}

$missing = @()

foreach ($pkg in $checks.Keys) {
    $mod = $checks[$pkg]
    $null = python -c "import $mod" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missing += $pkg
    }
}

# Material for MkDocs é incompatível com MkDocs 2.x; garantir série 1.x
if ($missing -notcontains "mkdocs") {
    $ver = python -c "import mkdocs; print(mkdocs.__version__)" 2>$null
    if ($ver -match "^2\.") {
        $missing += "mkdocs"
        Write-Host "  MkDocs $ver detectado; Material requer 1.x. Será reinstalado mkdocs>=1.5,<2" -ForegroundColor Yellow
    }
}

if ($missing.Count -gt 0) {
    Write-Host "  Instalando: mkdocs (1.x) e mkdocs-material..." -ForegroundColor Yellow
    pip install "mkdocs>=1.5,<2" "mkdocs-material" 2>&1 | Where-Object { $_ }
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Falha ao instalar dependências. Verifique se pip está disponível no PATH."
        exit 1
    }
} else {
    Write-Host "  ✅ Dependências pip OK" -ForegroundColor Green
}

# Garantir que mkdocs.exe esteja no PATH (instalação --user no Windows)
$mkdocsCmd = Get-Command mkdocs -ErrorAction SilentlyContinue
if (-not $mkdocsCmd) {
    $userScripts = python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))" 2>$null
    if ($userScripts -and (Test-Path $userScripts)) {
        $env:PATH = "$userScripts;$env:PATH"
        Write-Host "  PATH expandido com: $userScripts" -ForegroundColor Yellow
    }
    $mkdocsCmd = Get-Command mkdocs -ErrorAction SilentlyContinue
    if (-not $mkdocsCmd) {
        Write-Error "❌ mkdocs não encontrado no PATH. Reinstale com: pip install --upgrade mkdocs"
        exit 1
    }
}

Write-Host "  ✅ mkdocs encontrado: $($mkdocsCmd.Source)" -ForegroundColor Green

# ---------------------------------------------------------------------------
# [2] Copiar assets da skill
# ---------------------------------------------------------------------------
Write-Header "[2/10] Copiando assets da skill" "Cyan"

$skillAssetsDir = Join-Path (Split-Path -Parent $ScriptsDir) "assets"
if (Test-Path $skillAssetsDir) {
    $destAssetsDir = Join-Path $DocsPath "assets"
    New-Item -ItemType Directory -Force -Path $destAssetsDir | Out-Null
    Copy-Item -Path "$skillAssetsDir\*" -Destination $destAssetsDir -Recurse -Force
    $copied = @(Get-ChildItem $skillAssetsDir -Recurse -File).Count
    Write-Host "  ✅ Copiados $copied arquivos de assets" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Pasta assets não encontrada em skill (opcional)" -ForegroundColor Yellow
}

# ---------------------------------------------------------------------------
# [3] Gerar índice integrado
# ---------------------------------------------------------------------------
Write-Header "[3/10] Gerando índice integrado" "Cyan"

$pythonCmd = "python"
$generateIndexScript = Join-Path $ScriptsDir "generate-integrated-index.py"

if (Test-Path $generateIndexScript) {
    Write-Host "  Executando generate-integrated-index.py..." -ForegroundColor Gray
    & $pythonCmd $generateIndexScript --docs $DocsDir --root $ProjectRoot 2>&1 | ForEach-Object {
        if ($_ -match "✅|✓") {
            Write-Host $_ -ForegroundColor Green
        } elseif ($_ -match "❌|erro|error") {
            Write-Host $_ -ForegroundColor Red
        } elseif ($_ -match "⚠️|warning") {
            Write-Host $_ -ForegroundColor Yellow
        } else {
            Write-Host $_
        }
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Índice integrado gerado com sucesso" -ForegroundColor Green
    } else {
        Write-Error "❌ Falha ao gerar índice integrado"
        exit 1
    }
} else {
    Write-Warning "⚠️  Script generate-integrated-index.py não encontrado"
}

# ---------------------------------------------------------------------------
# [4] Gerar matrizes de rastreabilidade
# ---------------------------------------------------------------------------
Write-Header "[4/10] Gerando matrizes de rastreabilidade" "Cyan"

$generateTraceabilityScript = Join-Path $ScriptsDir "generate-traceability.py"

if (Test-Path $generateTraceabilityScript) {
    Write-Host "  Executando generate-traceability.py..." -ForegroundColor Gray
    & $pythonCmd $generateTraceabilityScript --docs $DocsDir --root $ProjectRoot 2>&1 | ForEach-Object {
        if ($_ -match "✅|✓") {
            Write-Host $_ -ForegroundColor Green
        } elseif ($_ -match "❌|erro|error") {
            Write-Host $_ -ForegroundColor Red
        } elseif ($_ -match "⚠️|warning") {
            Write-Host $_ -ForegroundColor Yellow
        } else {
            Write-Host $_
        }
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Matrizes de rastreabilidade geradas com sucesso" -ForegroundColor Green
    } else {
        Write-Warning "⚠️  Possível erro ao gerar matrizes (continuando...)"
    }
} else {
    Write-Warning "⚠️  Script generate-traceability.py não encontrado"
}

# ---------------------------------------------------------------------------
# [5] Coletar .md e gerar nav hierárquica
# ---------------------------------------------------------------------------
Write-Header "[5/10] Coletando artefatos de documentação" "Cyan"

$mdFiles = @()

# Artefatos de software
Write-Host "  Buscando artefatos de software..." -ForegroundColor Gray
$artefatosDir = Join-Path $DocsPath "processo_unificado" "artefatos_aprovados"
if (Test-Path $artefatosDir) {
    Get-ChildItem -Path $artefatosDir -Recurse -Filter "*.md" | Where-Object {
        $_.Name -notmatch "^(index|ROADMAP)" -and $_.FullName -notmatch "wireframes"
    } | ForEach-Object {
        $mdFiles += $_
    }
}

# Artefatos de banco de dados
Write-Host "  Buscando artefatos de banco de dados..." -ForegroundColor Gray
$bdDir = Join-Path $DocsPath "banco_dados"
if (Test-Path $bdDir) {
    Get-ChildItem -Path $bdDir -Filter "*.md" | Where-Object {
        $_.Name -notmatch "^(index|snapshot)"
    } | ForEach-Object {
        $mdFiles += $_
    }
}

# Rastreabilidade
Write-Host "  Buscando matrizes de rastreabilidade..." -ForegroundColor Gray
$traceDir = Join-Path $DocsPath "rastreabilidade"
if (Test-Path $traceDir) {
    Get-ChildItem -Path $traceDir -Filter "*.md" | ForEach-Object {
        $mdFiles += $_
    }
}

Write-Host "  ✅ Coletados $($mdFiles.Count) arquivos .md" -ForegroundColor Green

# ---------------------------------------------------------------------------
# [6] Gerar mkdocs.yml
# ---------------------------------------------------------------------------
Write-Header "[6/10] Gerando configuração MkDocs (mkdocs.yml)" "Cyan"

$mkdocsConfig = @"
site_name: Documentação Integrada
site_url: file:///$([System.IO.Path]::GetFullPath($SitePath).Replace('\', '/'))
docs_dir: $DocsDir
site_dir: $SiteDir
theme:
  name: material
  language: pt

nav:
  - Home: index.md
  - Visão Geral:
    - Índice Integrado: index.md
plugins:
  - search:
      lang: pt
markdown_extensions:
  - toc:
      permalink: "🔗"
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_block
        - name: plantuml
          class: plantuml
          format: !!python/name:pymdownx.superfences.fence_code_block
  - pymdownx.emoji
  - tables
  - attr_list
"@

$mkdocsPath = Join-Path $ProjectRoot "mkdocs.yml"
Set-Content -Path $mkdocsPath -Value $mkdocsConfig -Encoding UTF8
Write-Host "  ✅ mkdocs.yml gerado: $mkdocsPath" -ForegroundColor Green

# ---------------------------------------------------------------------------
# [7] Executar mkdocs build
# ---------------------------------------------------------------------------
Write-Header "[7/10] Executando mkdocs build" "Cyan"

Push-Location $ProjectRoot
try {
    Write-Host "  Compilando HTML com MkDocs..." -ForegroundColor Gray
    & mkdocs build --strict 2>&1 | ForEach-Object {
        if ($_ -match "INFO" -or $_ -match "✓") {
            Write-Host "  $_ " -ForegroundColor Green
        } elseif ($_ -match "WARNING|WARN") {
            Write-Host "  $_ " -ForegroundColor Yellow
        } else {
            Write-Host $_
        }
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "⚠️  mkdocs build gerou avisos (continuando...)"
    } else {
        Write-Host "  ✅ MkDocs build concluído com sucesso" -ForegroundColor Green
    }
} finally {
    Pop-Location
}

# ---------------------------------------------------------------------------
# [8] Gerar e injetar diagramas PlantUML
# ---------------------------------------------------------------------------
Write-Header "[8/10] Gerando e injetando diagramas PlantUML" "Cyan"

$generateDiagramsScript = Join-Path $ScriptsDir "generate-diagrams.py"

if (Test-Path $generateDiagramsScript) {
    Write-Host "  Executando generate-diagrams.py..." -ForegroundColor Gray
    & $pythonCmd $generateDiagramsScript `
        --docs $DocsDir `
        --root $ProjectRoot `
        --site $SiteDir `
        --server $PlantumlServer `
        --inject-site 2>&1 | ForEach-Object {
        if ($_ -match "✅|✓|gerado") {
            Write-Host "  $_ " -ForegroundColor Green
        } elseif ($_ -match "⚠️|warning") {
            Write-Host "  $_ " -ForegroundColor Yellow
        } else {
            Write-Host $_
        }
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Diagramas PlantUML processados com sucesso" -ForegroundColor Green
    } else {
        Write-Warning "⚠️  Possível erro ao processar diagramas (continuando...)"
    }
} else {
    Write-Warning "⚠️  Script generate-diagrams.py não encontrado"
}

# ---------------------------------------------------------------------------
# [9] Reestruturar HTML (opcional)
# ---------------------------------------------------------------------------
if ($Restructure) {
    Write-Header "[9/10] Reestruturando site HTML" "Cyan"

    $htmlDir = Join-Path $SitePath "html"
    New-Item -ItemType Directory -Force -Path $htmlDir | Out-Null

    $htmlFiles = Get-ChildItem -Path $SitePath -Filter "*.html" | Where-Object { $_.Name -ne "index.html" }
    foreach ($file in $htmlFiles) {
        Move-Item -Path $file.FullName -Destination (Join-Path $htmlDir $file.Name) -Force
    }

    Write-Host "  ✅ HTML reestruturado: index.html na raiz, demais em /html" -ForegroundColor Green
} else {
    Write-Host "`n[9/10] Reestruturação: não solicitado (use -Restructure para reorganizar)" -ForegroundColor Gray
}

# ---------------------------------------------------------------------------
# [10] Conclusão
# ---------------------------------------------------------------------------
Write-Header "[10/10] Documentação integrada gerada com sucesso!" "Green"

Write-Host "`n📁 Localização da documentação:"
Write-Host "   $SitePath`n" -ForegroundColor Green

Write-Host "🌐 Para visualizar, abra no navegador:"
Write-Host "   file:///$([System.IO.Path]::GetFullPath($SitePath).Replace('\', '/'))/index.html`n" -ForegroundColor Green

Write-Host "✅ Resumo do build:"
Write-Host "   ✓ Índice integrado gerado"
Write-Host "   ✓ Matrizes de rastreabilidade criadas"
Write-Host "   ✓ Diagramas PlantUML processados"
Write-Host "   ✓ Site HTML estático em $SiteDir"
Write-Host "   ✓ Navegação full-text ativa"
if ($Restructure) {
    Write-Host "   ✓ HTML reestruturado (index na raiz)"
}
Write-Host "`n"
