$ErrorActionPreference = "Stop"
$FrpcConfigPath = Join-Path $PSScriptRoot "frpc.toml"

function Read-Required([string]$Prompt) {
    do {
        $raw = Read-Host $Prompt
        if ($null -eq $raw) { throw "$Prompt is required" }
        $value = $raw.Trim()
    } while ([string]::IsNullOrWhiteSpace($value))
    return $value
}

function Read-ProjectCount([string]$Prompt) {
    while ($true) {
        $raw = Read-Host $Prompt
        $value = if ($null -eq $raw) { "" } else { $raw.Trim() }
        if ([string]::IsNullOrWhiteSpace($value)) { return 1 }
        $count = 0
        if ([int]::TryParse($value, [ref]$count) -and $count -ge 1 -and $count -le 20) { return $count }
        Write-Host "Please enter a number between 1 and 20." -ForegroundColor Yellow
    }
}

function Get-ExistingConfig() {
    if (-not (Test-Path $FrpcConfigPath)) {
        return [pscustomobject]@{ Text = ""; Token = "change-this-frp-token"; Domains = @(); Names = @(); IsConfigured = $false }
    }

    $text = Get-Content -Raw $FrpcConfigPath
    $token = "change-this-frp-token"
    $tokenMatch = [regex]::Match($text, 'auth\.token\s*=\s*"([^"]+)"')
    if ($tokenMatch.Success) { $token = $tokenMatch.Groups[1].Value }

    $domains = @()
    foreach ($match in [regex]::Matches($text, 'customDomains\s*=\s*\[\s*"([^"]+)"\s*\]')) {
        $domains += $match.Groups[1].Value
    }

    $names = @()
    foreach ($match in [regex]::Matches($text, 'name\s*=\s*"([^"]+)"')) {
        $names += $match.Groups[1].Value
    }

    $isConfigured = ($domains.Count -gt 0) -and -not ($text -match "CHANGE_ME")
    return [pscustomobject]@{ Text = $text; Token = $token; Domains = $domains; Names = $names; IsConfigured = $isConfigured }
}

function Read-ExistingAction([object]$Config) {
    if (-not $Config.IsConfigured) { return "rebuild" }

    Write-Host ""
    Write-Host "Existing frpc.toml found:" -ForegroundColor Green
    foreach ($domain in $Config.Domains) { Write-Host "  - https://$domain" }
    Write-Host ""
    Write-Host "Press Enter to start with existing config."
    Write-Host "Type A to add project(s), or R to rebuild all config."

    while ($true) {
        $raw = Read-Host "Choose [S/A/R]"
        $choice = if ($null -eq $raw) { "" } else { $raw.Trim().ToLower() }
        if ([string]::IsNullOrWhiteSpace($choice) -or $choice -eq "s" -or $choice -eq "start") { return "start" }
        if ($choice -eq "a" -or $choice -eq "add") { return "add" }
        if ($choice -eq "r" -or $choice -eq "rebuild") { return "rebuild" }
        Write-Host "Please enter S, A, or R." -ForegroundColor Yellow
    }
}

function Read-ProjectConfig([int]$Index) {
    Write-Host ""
    Write-Host "Project #$Index"
    $localUrl = Read-Required "Local web URL"
    $projectName = Read-Required "Project name"
    $domainInput = (Read-Required "Subdomain or full domain").ToLower()

    try { $uri = [Uri]$localUrl } catch { throw "Local URL must look like http://127.0.0.1:8077/path" }
    if ($uri.Scheme -notin @("http", "https")) { throw "Only http/https local URLs are supported" }

    $domain = if ($domainInput.Contains(".")) { $domainInput } else { "$domainInput.aim888888.xyz" }
    $hostPrefix = $domain.Split(".")[0]
    if ($hostPrefix -notmatch "^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$") {
        throw "Subdomain must use lowercase letters, numbers, and hyphens"
    }

    $localIP = if ($uri.Host -eq "localhost") { "127.0.0.1" } else { $uri.Host }
    $localPort = if ($uri.IsDefaultPort) { if ($uri.Scheme -eq "https") { 443 } else { 80 } } else { $uri.Port }
    $safeName = ($projectName.ToLower() -replace "[^a-z0-9_.-]+", "-").Trim("-")
    if ([string]::IsNullOrWhiteSpace($safeName)) { $safeName = $hostPrefix }

    $publicPath = $uri.AbsolutePath
    if ([string]::IsNullOrWhiteSpace($publicPath)) { $publicPath = "/" }
    $publicUrl = "https://$domain$publicPath$($uri.Fragment)"

    return [pscustomobject]@{ Name = $safeName; Domain = $domain; LocalIP = $localIP; LocalPort = $localPort; PublicUrl = $publicUrl }
}

function Ensure-Token([string]$Token) {
    if ($Token -ne "change-this-frp-token") { return $Token }
    Write-Host ""
    Write-Host "auth.token is still placeholder." -ForegroundColor Yellow
    $typedToken = (Read-Host "FRP token from admin, press Enter to keep placeholder").Trim()
    if (-not [string]::IsNullOrWhiteSpace($typedToken)) { return $typedToken }
    return $Token
}

function Build-ProxyLines([array]$Projects) {
    $lines = @()
    foreach ($project in $Projects) {
        $lines += @(
            '',
            '[[proxies]]',
            "name = `"$($project.Name)`"",
            'type = "http"',
            "localIP = `"$($project.LocalIP)`"",
            "localPort = $($project.LocalPort)",
            "customDomains = [`"$($project.Domain)`"]"
        )
    }
    return $lines
}

function Write-NewConfig([string]$Token, [array]$Projects) {
    $lines = @(
        'serverAddr = "frp.aim888888.xyz"',
        'serverPort = 7000',
        "auth.token = `"$Token`"",
        'transport.tls.enable = true'
    )
    $lines += Build-ProxyLines $Projects
    [IO.File]::WriteAllText($FrpcConfigPath, ($lines -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
}

function Append-Projects([array]$Projects) {
    $appendText = (Build-ProxyLines $Projects) -join [Environment]::NewLine
    $path = Join-Path $PSScriptRoot "frpc.toml"
    $old = Get-Content -Raw $path
    $new = $old.TrimEnd() + [Environment]::NewLine + $appendText + [Environment]::NewLine
    [IO.File]::WriteAllText($path, $new, [Text.UTF8Encoding]::new($false))
}

function Read-Projects([int]$Count, [array]$ExistingDomains, [array]$ExistingNames) {
    $projects = @()
    $seenDomains = @{}
    $seenNames = @{}
    foreach ($domain in $ExistingDomains) { $seenDomains[$domain] = $true }
    foreach ($name in $ExistingNames) { $seenNames[$name] = $true }

    for ($i = 1; $i -le $Count; $i++) {
        $project = Read-ProjectConfig $i
        if ($seenDomains.ContainsKey($project.Domain)) { throw "Duplicate domain: $($project.Domain)" }
        if ($seenNames.ContainsKey($project.Name)) { $project.Name = "$($project.Name)-$i" }
        $seenDomains[$project.Domain] = $true
        $seenNames[$project.Name] = $true
        $projects += $project
    }
    return ,$projects
}

Write-Host ""
Write-Host "Tool-Nexus client setup"
Write-Host ""
Write-Host "Examples:"
Write-Host "  Local URL:    http://127.0.0.1:8077/management.html#/"
Write-Host "  Project name: cpa-proxy"
Write-Host "  Domain:       webxkk  or  webxkk.aim888888.xyz"
Write-Host ""

$config = Get-ExistingConfig
$action = Read-ExistingAction $config
if ($action -eq "start") {
    Write-Host ""
    Write-Host "[OK] Using existing frpc.toml. Starting frpc now." -ForegroundColor Green
    exit 0
}

$token = Ensure-Token $config.Token
if ($action -eq "add") {
    $count = Read-ProjectCount "How many projects do you want to add? [1]"
    $projects = @(Read-Projects $count $config.Domains $config.Names)
    Append-Projects $projects
    Write-Host ""
    Write-Host "[OK] Added $($projects.Count) project(s) to frpc.toml." -ForegroundColor Green
} else {
    $count = Read-ProjectCount "How many projects do you want to expose? [1]"
    $projects = @(Read-Projects $count @() @())
    Write-NewConfig $token $projects
    Write-Host ""
    Write-Host "[OK] frpc.toml generated for $($projects.Count) project(s)." -ForegroundColor Green
}

foreach ($project in $projects) { Write-Host "Public URL: $($project.PublicUrl)" -ForegroundColor Green }
Write-Host ""
Write-Host "If your app shows Vite allowedHosts error, add .aim888888.xyz to vite.config."
