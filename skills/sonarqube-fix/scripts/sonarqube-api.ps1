param(
    [Parameter(Mandatory)]
    [string]$Action,

    [Parameter(Mandatory)]
    [string]$ProjectKey,

    [Parameter(Mandatory)]
    [string]$Token,

    [string]$Severity,
    [string]$Type,
    [string]$Status = "OPEN,CONFIRMED",
    [string]$IssueKey,
    [string]$RuleKey,
    [int]$Page = 1,
    [int]$PageSize = 100,
    [string]$SonarUrl = "https://sonarqube.ici.tec.br"
)

$headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/json"
}

switch ($Action) {
    "search-issues" {
        $query = @{
            componentKeys = $ProjectKey
            p = $Page
            ps = $PageSize
        }
        if ($Severity) { $query.severities = $Severity }
        if ($Type) { $query.types = $Type }
        if ($Status) { $query.statuses = $Status }

        $params = $query.Keys | ForEach-Object { "$_=$([Uri]::EscapeDataString($query[$_]))" }
        $uri = "$SonarUrl/api/issues/search?$($params -join '&')"

        $result = Invoke-RestMethod -Uri $uri -Headers $headers -TimeoutSec 30
        return $result | ConvertTo-Json -Depth 10 -Compress
    }

    "get-detail" {
        $uri = "$SonarUrl/api/issues/search?issues=$IssueKey"
        $result = Invoke-RestMethod -Uri $uri -Headers $headers -TimeoutSec 30

        $ruleDetail = $null
        if ($result.issues.Count -gt 0) {
            $ruleKey = $result.issues[0].rule
            try {
                $ruleUri = "$SonarUrl/api/rules/show?key=$ruleKey"
                $ruleDetail = Invoke-RestMethod -Uri $ruleUri -Headers $headers -TimeoutSec 10
            } catch { }
        }

        $output = @{
            issue = $result.issues
            components = $result.components
            rule = $ruleDetail.rule
        }
        return $output | ConvertTo-Json -Depth 10 -Compress
    }

    "get-rule" {
        $uri = "$SonarUrl/api/rules/show?key=$RuleKey"
        $result = Invoke-RestMethod -Uri $uri -Headers $headers -TimeoutSec 10
        return $result | ConvertTo-Json -Depth 10 -Compress
    }
}
