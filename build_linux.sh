#!/bin/bash
set -e

# Help message
show_help() {
    echo "Personal Manager CLI - Linux Packaging Script"
    echo "Usage: ./build_linux.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --deb      Package the compiled binary into a Debian (.deb) package"
    echo "  --rpm      Package the compiled binary into a Fedora/RHEL (.rpm) package"
    echo "  --arch     Package the compiled binary into an Arch Linux package (.pkg.tar.zst)"
    echo "  -h, --help Show this help message"
    echo ""
    echo "By default, running with no options compiles only the standalone binary inside 'dist/'."
}

# Parse options
BUILD_DEB=false
BUILD_RPM=false
BUILD_ARCH=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --deb) BUILD_DEB=true ;;
        --rpm) BUILD_RPM=true ;;
        --arch) BUILD_ARCH=true ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage details."
            exit 1
            ;;
    esac
    shift
done

# Perform early checks for package manager tools
if [ "$BUILD_DEB" = true ]; then
    if ! command -v dpkg-deb >/dev/null 2>&1; then
        echo "Error: 'dpkg-deb' utility is not installed."
        echo "For Ubuntu/Debian systems, install it using: sudo apt-get install dpkg"
        exit 1
    fi
fi

if [ "$BUILD_RPM" = true ]; then
    if ! command -v rpmbuild >/dev/null 2>&1; then
        echo "Error: 'rpmbuild' utility is not installed."
        echo "For Fedora/CentOS/RHEL systems, install it using: sudo dnf install rpm-build"
        exit 1
    fi
fi

if [ "$BUILD_ARCH" = true ]; then
    if ! command -v makepkg >/dev/null 2>&1; then
        echo "Error: 'makepkg' utility is not installed."
        echo "For Arch Linux, please make sure you have the 'base-devel' package installed."
        exit 1
    fi
fi

echo "=== Building Personal Manager Standalone Linux Binary ==="

# 1. Clean previous build artifacts
echo "Cleaning old builds..."
rm -rf build/ dist/

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

# 5. Build Debian Package
if [ "$BUILD_DEB" = true ]; then
    echo "=== Building Debian Package ==="
    echo "Preparing Debian package structure..."
    DEB_DIR="build/debian"
    mkdir -p "$DEB_DIR/DEBIAN"
    mkdir -p "$DEB_DIR/usr/bin"
    
    cp "dist/personal-manager" "$DEB_DIR/usr/bin/personal-manager"
    chmod +x "$DEB_DIR/usr/bin/personal-manager"
    
    cat <<EOT > "$DEB_DIR/DEBIAN/control"
Package: personal-manager
Version: 0.0.1
Section: utils
Priority: optional
Architecture: amd64
Maintainer: personal-manager dev <dev@personalmanager.local>
Description: Personal Manager CLI application with budgeting and plugin management.
EOT

    echo "Building deb package..."
    dpkg-deb --build "$DEB_DIR" personal-manager.deb
    echo "Debian package created: personal-manager.deb"
fi

# 6. Build RPM Package
if [ "$BUILD_RPM" = true ]; then
    echo "=== Building RPM Package ==="
    RPM_TOPDIR="$(pwd)/build/rpmbuild"
    echo "Preparing RPM package structure under $RPM_TOPDIR..."
    mkdir -p "$RPM_TOPDIR"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    
    # Copy binary to SOURCES
    cp "dist/personal-manager" "$RPM_TOPDIR/SOURCES/personal-manager"
    
    # Write RPM Spec file
    cat <<EOT > "$RPM_TOPDIR/SPECS/personal-manager.spec"
Name:           personal-manager
Version:        0.0.1
Release:        1%{?dist}
Summary:        Personal Manager CLI application with budgeting and plugin management
License:        MIT
URL:            https://github.com/archangel7431/personal_manager

%description
Personal Manager CLI application with budgeting and plugin management.

%install
mkdir -p %{buildroot}/usr/bin
cp %{_sourcedir}/personal-manager %{buildroot}/usr/bin/personal-manager
chmod +x %{buildroot}/usr/bin/personal-manager

%files
/usr/bin/personal-manager

%changelog
* Sun Aug 02 2026 Developer <dev@personalmanager.local> - 0.0.1-1
- Initial release of personal-manager binary packaging.
EOT

    echo "Building RPM package..."
    rpmbuild --define "_topdir $RPM_TOPDIR" -bb "$RPM_TOPDIR/SPECS/personal-manager.spec"
    
    # Find generated RPM and copy to root
    RPM_FILE=$(find "$RPM_TOPDIR/RPMS" -name "*.rpm" | head -n 1)
    if [ -f "$RPM_FILE" ]; then
        cp "$RPM_FILE" ./
        echo "RPM package created: $(basename "$RPM_FILE")"
    else
        echo "Error: Failed to find generated RPM package!"
        exit 1
    fi
fi

# 7. Build Arch Linux Package
if [ "$BUILD_ARCH" = true ]; then
    echo "=== Building Arch Linux Package ==="
    ARCH_DIR="build/arch"
    echo "Preparing Arch package structure under $ARCH_DIR..."
    mkdir -p "$ARCH_DIR"
    
    cp "dist/personal-manager" "$ARCH_DIR/personal-manager"
    
    # Write PKGBUILD
    cat <<EOT > "$ARCH_DIR/PKGBUILD"
pkgname=personal-manager
pkgver=0.0.1
pkgrel=1
pkgdesc="Personal Manager CLI application with budgeting and plugin management."
arch=('x86_64')
url="https://github.com/archangel7431/personal_manager"
license=('MIT')
depends=()
source=()

package() {
    install -Dm755 "\${srcdir}/../personal-manager" "\${pkgdir}/usr/bin/personal-manager"
}
EOT

    echo "Building Arch package..."
    (
        cd "$ARCH_DIR"
        makepkg -f --nodeps
    )
    
    # Find generated package and copy to root
    ARCH_FILE=$(find "$ARCH_DIR" -name "*.pkg.tar.*" | head -n 1)
    if [ -f "$ARCH_FILE" ]; then
        cp "$ARCH_FILE" ./
        echo "Arch Linux package created: $(basename "$ARCH_FILE")"
    else
        echo "Error: Failed to find generated Arch package!"
        exit 1
    fi
fi

echo "=== Build Process Complete! ==="
