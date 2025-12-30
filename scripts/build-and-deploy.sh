#!/bin/bash
# Build and deploy release
# Usage: ./scripts/build-and-deploy.sh <changelog_file> <curseforge_token> <modrinth_token>

set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <changelog_file> <curseforge_token> <modrinth_token>"
    echo ""
    echo "Example: $0 CHANGELOG.md cf_token modrinth_token"
    exit 1
fi

CHANGELOG_FILE=$1
CURSEFORGE_TOKEN=$2
MODRINTH_TOKEN=$3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Get version from gradle.properties
VERSION=$(grep "^version=" gradle.properties | cut -d'=' -f2)

echo "Building version $VERSION..."
./gradlew clean build

echo ""
echo "Build successful!"
echo ""

# Deploy
"$SCRIPT_DIR/deploy-all.sh" "$VERSION" "$CHANGELOG_FILE" "$CURSEFORGE_TOKEN" "$MODRINTH_TOKEN"
