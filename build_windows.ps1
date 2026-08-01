# Windows PowerShell build script for Personal Manager CLI

Write-Host "=== Building Personal Manager Standalone Windows Binary ==="

# 1. Clean previous build directories
Write-Host "Cleaning old builds..."
If (Test-Path build) { Remove-Item -Recurse -Force build }
If (Test-Path dist) { Remove-Item -Recurse -Force dist }

# 2. Synchronize virtual environment & install PyInstaller
Write-Host "Syncing environment..."
uv sync
Write-Host "Installing PyInstaller..."
uv pip install pyinstaller

# 3. Run PyInstaller
Write-Host "Running PyInstaller to compile executable..."
uv run pyinstaller --onefile --name personal-manager `
  --add-data "personal_manager/logging_config.yaml;personal_manager" `
  --collect-submodules personal_manager.plugins `
  personal_manager/main.py

Write-Host "=== Packaging Complete! ==="
Write-Host "Windows executable generated: dist/personal-manager.exe"
