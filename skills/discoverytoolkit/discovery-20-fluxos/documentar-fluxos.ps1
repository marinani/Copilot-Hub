param(
    [int]$Limite   = 999,
    [string]$De    = "",
    [string]$Ate   = ""
)

$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("PATH","User")

if (-not (Get-Command copilot -ErrorAction SilentlyContinue)) {
    Write-Host "ERRO: copilot nao encontrado no PATH." -ForegroundColor Red
    exit 1
}

$catalogo = "d:\projetos\Gprev-app\discovery\DISC-03-CATALOGO-DE-FLUXOS.md"
$logFile  = "d:\projetos\Gprev-app\discovery\log-documentar-fluxos.txt"

if (-not (Test-Path $catalogo)) {
    Write-Host "ERRO: catalogo nao encontrado: $catalogo" -ForegroundColor Red
    Write-Host "Execute antes a skill discovery-20-fluxos-catalago." -ForegroundColor Yellow
    exit 1
}

$pendentes = Get-Content $catalogo |
    Where-Object { $_ -match '\| (CF-\d{3}) \|' -and $_ -match 'pendente' } |
    ForEach-Object {
        if ($_ -match '\| (CF-\d{3}) \|') {
            [PSCustomObject]@{ Num = [int]($Matches[1] -replace 'CF-',''); ID = $Matches[1] }
        }
    }

if ($De -ne "") { $deNum = [int]$De; $pendentes = $pendentes | Where-Object { $_.Num -ge $deNum } }
if ($Ate -ne "") { $ateNum = [int]$Ate; $pendentes = $pendentes | Where-Object { $_.Num -le $ateNum } }
$pendentes = $pendentes | Select-Object -First $Limite

Write-Host "============================================" -ForegroundColor Yellow
Write-Host " Documentar Fluxos - GitHub Copilot CLI"    -ForegroundColor Yellow
Write-Host " Pendentes: $($pendentes.Count) fluxos"     -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow

if ($pendentes.Count -eq 0) { Write-Host "Nenhum fluxo pendente." -ForegroundColor Green; exit 0 }

$ok = 0; $falha = 0; $total = $pendentes.Count; $i = 0

foreach ($fluxo in $pendentes) {
    $i++
    $prompt = "use a skill discovery-20-fluxos-gerar e documente o fluxo $($fluxo.ID) seguindo DISC-03-CATALOGO-DE-FLUXOS.md em d:\projetos\Gprev-app\discovery\DISC-03-CATALOGO-DE-FLUXOS.md"
    Write-Host "[$i/$total] $($fluxo.ID) ..." -ForegroundColor Cyan

    $output = copilot -p $prompt --allow-all --autopilot 2>&1
    $output | Write-Host

    $status = if ($output -and $output.Count -gt 0) { "OK" } else { "FALHA" }
    "$((Get-Date).ToString('dd/MM/yyyy HH:mm:ss')) | $($fluxo.ID) | $status" | Add-Content $logFile

    if ($status -eq "OK") { $ok++; Write-Host "  OK $($fluxo.ID)" -ForegroundColor Green }
    else { $falha++; Write-Host "  FALHA $($fluxo.ID)" -ForegroundColor Red }

    Start-Sleep -Seconds 2
}

Write-Host "============================================" -ForegroundColor Yellow
Write-Host " Concluido: $ok OK - $falha falha(s)"       -ForegroundColor Yellow
Write-Host " Log: $logFile"                              -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
