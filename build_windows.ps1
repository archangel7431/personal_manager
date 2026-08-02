param (
    [switch]$Zip
)

# Windows PowerShell build script for Personal Manager CLI

Write-Host "=== Building Personal Manager Standalone Windows Binary ==="

# 1. Clean previous build directories
Write-Host "Cleaning old builds..."
If (Test-Path build) { Remove-Item -Recurse -Force build }
If (Test-Path dist) { Remove-Item -Recurse -Force dist }

# Check if uv is installed on the Windows host
$useUv = $null -ne (Get-Command uv -ErrorAction SilentlyContinue)

if ($useUv) {
    Write-Host "uv found on Windows. Syncing environment..."
    uv sync
    Write-Host "Installing PyInstaller..."
    uv pip install pyinstaller
    
    # 2. Run PyInstaller
    Write-Host "Running PyInstaller to compile executable..."
    uv run pyinstaller --onefile --name personal-manager `
      --add-data "personal_manager/logging_config.yaml;personal_manager" `
      --collect-submodules personal_manager.plugins `
      personal_manager/main.py
} else {
    Write-Host "uv not found on Windows. Falling back to native python/pip..."
    
    # Verify python is installed
    If ($null -eq (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Error "Error: Neither 'uv' nor 'python' was found on your Windows path."
        Write-Error "Please install Python for Windows (https://www.python.org/downloads/) or install 'uv' to run compilation."
        exit 1
    }
    
    Write-Host "Installing PyInstaller with pip..."
    python -m pip install pyinstaller
    
    # 2. Run PyInstaller
    Write-Host "Running PyInstaller to compile executable..."
    pyinstaller --onefile --name personal-manager `
      --add-data "personal_manager/logging_config.yaml;personal_manager" `
      --collect-submodules personal_manager.plugins `
      personal_manager/main.py
}

Write-Host "=== Packaging Complete! ==="
Write-Host "Windows executable generated: dist/personal-manager.exe"

# 3. Optional ZIP Packaging
if ($Zip) {
    Write-Host "=== Packaging into ZIP Archive ==="
    # Remove old ZIP if it exists
    if (Test-Path personal-manager.zip) { Remove-Item -Force personal-manager.zip }
    Compress-Archive -Path dist/personal-manager.exe -DestinationPath ./personal-manager.zip -Force
    Write-Host "ZIP package created: personal-manager.zip"
}
