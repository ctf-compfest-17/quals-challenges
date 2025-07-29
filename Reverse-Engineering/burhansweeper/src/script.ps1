$ErrorActionPreference = "Stop"

Write-Host "[1/6] Running love ."
Start-Process -Wait -NoNewWindow "love.exe" "."

# Paths
$bytecodeDir = "bytecode"
$tempZip = "game.zip"
$loveFile = "../public/game.love"
$exeFile = "../public/game.exe"
$publicDir = "../public"
$love2dDir = "love2d"

Write-Host "[2/6] Creating game.love from bytecode folder..."
if (Test-Path $tempZip) { Remove-Item $tempZip }
if (Test-Path $loveFile) { Remove-Item $loveFile }

Compress-Archive -Path "$bytecodeDir\*" -DestinationPath $tempZip
Move-Item -Path $tempZip -Destination $loveFile

Write-Host "[3/6] Copying LÖVE runtime to public directory..."
if (!(Test-Path $publicDir)) { New-Item -ItemType Directory -Path $publicDir | Out-Null }
Copy-Item "$love2dDir\*" $publicDir -Recurse -Force

Write-Host "[4/6] Creating game.exe..."
$loveExePath = Join-Path $love2dDir "love.exe"

$out = [System.IO.File]::Create($exeFile)
try {
    [byte[]]$exeBytes = [System.IO.File]::ReadAllBytes($loveExePath)
    [byte[]]$loveBytes = [System.IO.File]::ReadAllBytes($loveFile)
    $out.Write($exeBytes, 0, $exeBytes.Length)
    $out.Write($loveBytes, 0, $loveBytes.Length)
} finally {
    $out.Close()
}

Write-Host "[5/6] Removing unneeded files from public..."
$filesToRemove = @(
    "license.txt",
    "love.ico",
    "lovec.exe",
    "love.exe",
    "readme.txt",
    "changes.txt",
    "game.love"
)

foreach ($file in $filesToRemove) {
    $path = Join-Path $publicDir $file
    if (Test-Path $path) {
        Remove-Item $path -Force
        Write-Host "Removed $file"
    }
}

Write-Host "[6/6] Build complete. Output: $exeFile"
