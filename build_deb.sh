#!/bin/bash
#
# PyTo-Do .deb Package Builder
# Creates Debian packages for PyTo-Do application
#

set -e

# Package information
PACKAGE_NAME="pytodo"
VERSION="1.1.0"
ARCHITECTURE="all"
MAINTAINER="https://github.com/mdnoyon9758"
DESCRIPTION="PyTo-Do: A simple yet powerful task management app built with pure Python"
HOMEPAGE="https://github.com/CosmicLM/PyTo-Do"
SECTION="utils"
PRIORITY="optional"
LICENSE="MIT"

# Directories
BUILD_DIR="build_deb"
PACKAGE_DIR="$BUILD_DIR/$PACKAGE_NAME"
DEBIAN_DIR="$PACKAGE_DIR/DEBIAN"
INSTALL_DIR="$PACKAGE_DIR/opt/pytodo"
BIN_DIR="$PACKAGE_DIR/usr/bin"
DESKTOP_DIR="$PACKAGE_DIR/usr/share/applications"
ICON_DIR="$PACKAGE_DIR/usr/share/pixmaps"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 PyTo-Do .deb Package Builder${NC}"
echo "=================================="

# Check if we're on Linux (required for .deb packaging)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ Error: .deb packaging requires Linux environment${NC}"
    echo "Please run this script on a Linux system or WSL"
    exit 1
fi

# Check dependencies
echo -e "${YELLOW}📋 Checking dependencies...${NC}"

# Check if dpkg-deb is available
if ! command -v dpkg-deb &> /dev/null; then
    echo -e "${RED}❌ dpkg-deb not found. Please install: sudo apt-get install dpkg-dev${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All dependencies satisfied${NC}"

# Clean previous build
if [ -d "$BUILD_DIR" ]; then
    echo -e "${YELLOW}🧹 Cleaning previous build...${NC}"
    rm -rf "$BUILD_DIR"
fi

# Create directory structure
echo -e "${YELLOW}📁 Creating package structure...${NC}"
mkdir -p "$DEBIAN_DIR"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Copy application files
echo -e "${YELLOW}📦 Copying application files...${NC}"
cp -r backend "$INSTALL_DIR/"
cp -r frontend "$INSTALL_DIR/"
cp -r assets "$INSTALL_DIR/"
cp main.py "$INSTALL_DIR/"
cp gui.py "$INSTALL_DIR/"
cp storage.json "$INSTALL_DIR/"
cp README.MD "$INSTALL_DIR/"
cp LICENSE "$INSTALL_DIR/"
cp CONTRIBUTING.md "$INSTALL_DIR/"

# Create control file
echo -e "${YELLOW}📝 Creating control file...${NC}"
cat > "$DEBIAN_DIR/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: $SECTION
Priority: $PRIORITY
Architecture: $ARCHITECTURE
Depends: python3 (>= 3.8), python3-tk
Maintainer: $MAINTAINER
Description: $DESCRIPTION
 PyTo-Do is a simple yet powerful task management application built with pure Python.
 It provides both CLI and GUI interfaces for managing tasks with persistent storage.
 .
 Features:
  - Add, Delete, and Mark Tasks with full CRUD functionality
  - Persistent Storage with automatic saving to JSON
  - Clean & Intuitive CLI and GUI interfaces
  - Lightweight and dependency-free
  - Cross-platform compatibility
Homepage: $HOMEPAGE
EOF

# Create postinst script
echo -e "${YELLOW}⚙️  Creating post-installation script...${NC}"
cat > "$DEBIAN_DIR/postinst" << 'EOF'
#!/bin/bash
set -e

# Create symlinks in /usr/bin
ln -sf /opt/pytodo/main.py /usr/bin/pytodo
ln -sf /opt/pytodo/gui.py /usr/bin/pytodo-gui

# Make scripts executable
chmod +x /opt/pytodo/main.py
chmod +x /opt/pytodo/gui.py
chmod +x /usr/bin/pytodo
chmod +x /usr/bin/pytodo-gui

echo "PyTo-Do installed successfully!"
echo "Run 'pytodo' for CLI version or 'pytodo-gui' for GUI version"
EOF

# Create prerm script
echo -e "${YELLOW}⚙️  Creating pre-removal script...${NC}"
cat > "$DEBIAN_DIR/prerm" << 'EOF'
#!/bin/bash
set -e

# Remove symlinks
rm -f /usr/bin/pytodo
rm -f /usr/bin/pytodo-gui

echo "PyTo-Do removed successfully!"
EOF

# Make maintainer scripts executable
chmod +x "$DEBIAN_DIR/postinst"
chmod +x "$DEBIAN_DIR/prerm"

# Create desktop entry
echo -e "${YELLOW}🖥️  Creating desktop entry...${NC}"
cat > "$DESKTOP_DIR/pytodo.desktop" << EOF
[Desktop Entry]
Name=PyTo-Do
Comment=Task Management Application
Exec=/usr/bin/pytodo-gui
Icon=pytodo
Terminal=false
Type=Application
Categories=Office;Utility;
Keywords=todo;task;management;productivity;
EOF

# Copy icon if available
if [ -f "assets/Py-ToDoLogo.png" ]; then
    cp "assets/Py-ToDoLogo.png" "$ICON_DIR/pytodo.png"
fi

# Calculate installed size
INSTALLED_SIZE=$(du -sk "$PACKAGE_DIR" | cut -f1)
echo "Installed-Size: $INSTALLED_SIZE" >> "$DEBIAN_DIR/control"

# Build the package
echo -e "${YELLOW}🔨 Building .deb package...${NC}"
dpkg-deb --build "$PACKAGE_DIR" "${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"

# Move package to release directory
mkdir -p release
mv "${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb" release/

# Verify package
echo -e "${YELLOW}🔍 Verifying package...${NC}"
dpkg-deb --info "release/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
dpkg-deb --contents "release/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"

echo -e "${GREEN}🎉 .deb package created successfully!${NC}"
echo -e "${GREEN}📦 Package location: release/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb${NC}"
echo ""
echo -e "${BLUE}Installation instructions:${NC}"
echo "  sudo dpkg -i release/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
echo "  sudo apt-get install -f  # Fix dependencies if needed"
echo ""
echo -e "${BLUE}Usage after installation:${NC}"
echo "  pytodo        # CLI version"
echo "  pytodo-gui    # GUI version"

# Clean up
rm -rf "$BUILD_DIR"

echo -e "${GREEN}✅ Build completed successfully!${NC}"
