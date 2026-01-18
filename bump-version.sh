#!/bin/bash
# Version Management Script for HRMS
# Usage: ./bump-version.sh [major|minor|patch]

set -e

VERSION_FILE="VERSION"
INIT_FILE="__init__.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current version
CURRENT_VERSION=$(cat $VERSION_FILE)

echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}HRMS Version Management${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "Current Version: ${YELLOW}$CURRENT_VERSION${NC}"

# Parse version
IFS='.' read -r -a version_parts <<< "$CURRENT_VERSION"
MAJOR="${version_parts[0]}"
MINOR="${version_parts[1]}"
PATCH="${version_parts[2]}"

# Determine new version
BUMP_TYPE="${1:-patch}"

case $BUMP_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo -e "${RED}Error: Invalid bump type. Use 'major', 'minor', or 'patch'${NC}"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"

echo -e "Bump Type: ${YELLOW}$BUMP_TYPE${NC}"
echo -e "New Version: ${GREEN}$NEW_VERSION${NC}"
echo ""

# Prompt for confirmation
read -p "Do you want to update to version $NEW_VERSION? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Version update cancelled${NC}"
    exit 0
fi

# Update VERSION file
echo "$NEW_VERSION" > $VERSION_FILE
echo -e "${GREEN}✓${NC} Updated $VERSION_FILE"

# Update __init__.py
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" $INIT_FILE
rm -f ${INIT_FILE}.bak
echo -e "${GREEN}✓${NC} Updated $INIT_FILE"

# Git operations
if [ -d ".git" ]; then
    echo ""
    read -p "Do you want to commit and tag this version? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add $VERSION_FILE $INIT_FILE
        git commit -m "chore: bump version to $NEW_VERSION"
        git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
        
        echo -e "${GREEN}✓${NC} Created git commit and tag v$NEW_VERSION"
        echo ""
        echo -e "${YELLOW}Don't forget to push:${NC}"
        echo -e "  git push origin master"
        echo -e "  git push origin v$NEW_VERSION"
    fi
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Version updated successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "Old Version: ${YELLOW}$CURRENT_VERSION${NC}"
echo -e "New Version: ${GREEN}$NEW_VERSION${NC}"
