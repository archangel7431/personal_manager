#!/bin/bash
set -e

echo "=== Building Personal Manager Standalone Linux Binary ==="

# 1. Clean previous build artifacts
echo "Cleaning old builds..."
rm -rf build/ dist/ personal-manager.deb

# 2. Ensure pyinstaller is installed in the uv environment
echo "Syncing uv environment..."
uv sync
echo "Installing PyInstaller..."
uv pip install pyinstaller

# 3. Compile the application with PyInstaller
echo "Compiling binary with PyInstaller..."
uv run pyinstaller --onefile --name personal-manager \
  --add-data "personal_manager/logging_config.yaml:personal_manager" \
  --collect-submodules personal_manager.plugins \
  personal_manager/main.py

# 4. Verify compiled binary exists
if [ ! -f "dist/personal-manager" ]; then
  echo "Error: Failed to compile executable!"
  exit 1
fi
echo "Executable compiled successfully at dist/personal-manager"

# 5. Create Debian package directory structure
echo "Preparing Debian package structure..."
DEB_DIR="build/debian"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/bin"

# 6. Copy binary to the debian structure
cp "dist/personal-manager" "$DEB_DIR/usr/bin/personal-manager"
chmod +x "$DEB_DIR/usr/bin/personal-manager"

# 7. Write Debian control file
cat <<EOT > "$DEB_DIR/DEBIAN/control"
Package: personal-manager
Version: 0.0.1
Section: utils
Priority: optional
Architecture: amd64
Maintainer: personal-manager dev <dev@personalmanager.local>
Description: Personal Manager CLI application with budgeting and plugin management.
EOT

# 8. Build the Debian package
echo "Building deb package..."
dpkg-deb --build "$DEB_DIR" personal-manager.deb

echo "=== Packaging Complete! ==="
echo "Debian package created: personal-manager.deb"
