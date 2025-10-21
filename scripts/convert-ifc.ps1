Param(
    [Parameter(Mandatory = $true)][string]$Source,
    [string]$Out,
    [switch]$Log
)

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found on PATH. Install Node.js LTS, reopen PowerShell, and retry."; exit 1
}
if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
    Write-Error "npx not found. Reinstall Node.js (ensure npm is included)."; exit 1
}

if (-not (Test-Path -LiteralPath $Source)) {
    Write-Error "Source file not found: $Source"; exit 1
}

if (-not $Out) {
    $dir = Split-Path -Path $Source -Parent
    $base = [System.IO.Path]::GetFileNameWithoutExtension($Source)
    $Out = Join-Path $dir ("$base.xkt")
}

$pkg = '@xeokit/xeokit-convert'
$args = @('-y', $pkg, '--', '-s', $Source, '-o', $Out)
if ($Log) { $args += '-l' }

Write-Host "Converting IFC -> XKT" -ForegroundColor Cyan
Write-Host "Source: $Source" -ForegroundColor DarkGray
Write-Host "Output: $Out" -ForegroundColor DarkGray

npx @args

if ($LASTEXITCODE -ne 0) {
    Write-Error "Conversion failed with exit code $LASTEXITCODE"; exit $LASTEXITCODE
}

Write-Host "Done." -ForegroundColor Green
