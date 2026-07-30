[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$SourcePath
)

$ErrorActionPreference = 'Stop'

function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-ErrorColor {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Set-GitIgnoreEntry {
    param(
        [string]$RepositoryRoot,
        [string]$Entry
    )

    $gitignorePath = Join-Path $RepositoryRoot '.gitignore'

    if (-not (Test-Path -LiteralPath $gitignorePath -PathType Leaf)) {
        Set-Content -LiteralPath $gitignorePath -Value $Entry
        Write-Success ".gitignore criado com a entrada: $Entry"
        return
    }

    $gitignoreContent = Get-Content -LiteralPath $gitignorePath -Raw
    $escapedEntry = [regex]::Escape($Entry)

    if ($gitignoreContent -notmatch "(^|`r?`n)$escapedEntry(`r?`n|$)") {
        $prefix = if ([string]::IsNullOrWhiteSpace($gitignoreContent)) { '' } elseif ($gitignoreContent.EndsWith("`r`n") -or $gitignoreContent.EndsWith("`n")) { '' } else { "`r`n" }
        Add-Content -LiteralPath $gitignorePath -Value "$prefix$Entry"
        Write-Success "Entrada adicionada ao .gitignore: $Entry"
        return
    }

    Write-Success "Entrada ja presente no .gitignore: $Entry"
}

function Remove-GitIgnoreEntry {
    param(
        [string]$RepositoryRoot,
        [string]$Entry
    )

    $gitignorePath = Join-Path $RepositoryRoot '.gitignore'

    if (-not (Test-Path -LiteralPath $gitignorePath -PathType Leaf)) {
        return
    }

    $gitignoreLines = Get-Content -LiteralPath $gitignorePath
    $filteredLines = @($gitignoreLines | Where-Object { $_ -ne $Entry })

    if ($filteredLines.Count -ne $gitignoreLines.Count) {
        Set-Content -LiteralPath $gitignorePath -Value $filteredLines
        Write-Success "Entrada removida do .gitignore: $Entry"
    }
}

try {
    # Converte para caminho absoluto (full path), mesmo que venha relativo.
    $sourceFullPath = [System.IO.Path]::GetFullPath($SourcePath)

    # Segurança: valida se a origem existe e se e uma pasta.
    if (-not (Test-Path -LiteralPath $sourceFullPath -PathType Container)) {
        throw "A pasta de origem nao existe ou nao e um diretorio valido: $sourceFullPath"
    }

    $currentDir = (Get-Location).Path
    $destinationRoot = Join-Path $currentDir '.github\skills'

    # Garante a estrutura de destino.
    if (-not (Test-Path -LiteralPath $destinationRoot -PathType Container)) {
        New-Item -Path $destinationRoot -ItemType Directory | Out-Null
        Write-Success "Pasta de destino criada: $destinationRoot"
    }

    $sourceName = Split-Path -Path $sourceFullPath -Leaf
    $destinationLinkPath = Join-Path $destinationRoot $sourceName
    $ignoreEntry = ".github/skills/$sourceName/"

    Remove-GitIgnoreEntry -RepositoryRoot $currentDir -Entry '.github/skill/'
    Remove-GitIgnoreEntry -RepositoryRoot $currentDir -Entry ".github/skill/$sourceName/"
    Remove-GitIgnoreEntry -RepositoryRoot $currentDir -Entry '.github/skills/'
    Set-GitIgnoreEntry -RepositoryRoot $currentDir -Entry $ignoreEntry

    # Idempotencia: remove link/pasta/arquivo existente com o mesmo nome.
    if (Test-Path -LiteralPath $destinationLinkPath) {
        Remove-Item -LiteralPath $destinationLinkPath -Recurse -Force
        Write-Success "Destino anterior removido: $destinationLinkPath"
    }

    # Cria o vinculo via Junction para evitar exigir privilegios elevados no Windows.
    New-Item -Path $destinationLinkPath -ItemType Junction -Target $sourceFullPath | Out-Null

    Write-Success "Junction criada com sucesso:"
    Write-Success "  Origem:  $sourceFullPath"
    Write-Success "  Destino: $destinationLinkPath"
}
catch {
    Write-ErrorColor "Erro ao criar o vinculo de skill."
    Write-ErrorColor $_.Exception.Message
    exit 1
}
