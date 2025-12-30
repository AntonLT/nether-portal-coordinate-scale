#!/bin/bash
# Deploy to both CurseForge and Modrinth
# Usage: ./scripts/deploy-all.sh <version> <changelog_file> <curseforge_token> <modrinth_token>

set -e

if [ $# -lt 4 ]; then
    echo "Usage: $0 <version> <changelog_file> <curseforge_token> <modrinth_token>"
    echo ""
    echo "Example: $0 1.21.5 CHANGELOG.md cf_token modrinth_token"
    exit 1
fi

VERSION=$1
CHANGELOG_FILE=$2
CURSEFORGE_TOKEN=$3
MODRINTH_TOKEN=$4

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "Deploying version $VERSION..."
echo ""

# Set environment variables
export CURSEFORGE_PROJECT_ID=${CURSEFORGE_PROJECT_ID:-}
export MODRINTH_PROJECT_ID=${MODRINTH_PROJECT_ID:-}

if [ -z "$CURSEFORGE_PROJECT_ID" ] || [ -z "$MODRINTH_PROJECT_ID" ]; then
    echo "Error: Missing project IDs in environment variables"
    echo "Set them with:"
    echo "  export CURSEFORGE_PROJECT_ID=<your_cf_project_id>"
    echo "  export MODRINTH_PROJECT_ID=<your_modrinth_project_id>"
    exit 1
fi

# Deploy to CurseForge
echo ">>> Deploying to CurseForge..."
"$SCRIPT_DIR/deploy-curseforge.sh" "$VERSION" "$CHANGELOG_FILE" "$CURSEFORGE_TOKEN"
echo ""

# Deploy to Modrinth
echo ">>> Deploying to Modrinth..."
"$SCRIPT_DIR/deploy-modrinth.sh" "$VERSION" "$CHANGELOG_FILE" "$MODRINTH_TOKEN"
echo ""

echo "✓✓✓ Successfully deployed version $VERSION to all platforms! ✓✓✓"
