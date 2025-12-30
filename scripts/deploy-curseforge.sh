#!/bin/bash
# Deploy to CurseForge
# Usage: ./scripts/deploy-curseforge.sh <version> <changelog_file> <curseforge_token>

set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <version> <changelog_file> <curseforge_token>"
    echo ""
    echo "Example: $0 1.21.5 CHANGELOG.md your_curseforge_token"
    exit 1
fi

VERSION=$1
CHANGELOG_FILE=$2
CURSEFORGE_TOKEN=$3
PROJECT_ID=${CURSEFORGE_PROJECT_ID:-}

if [ -z "$PROJECT_ID" ]; then
    echo "Error: CURSEFORGE_PROJECT_ID environment variable not set"
    echo "Set it with: export CURSEFORGE_PROJECT_ID=<your_project_id>"
    exit 1
fi

# Get the Minecraft version from gradle.properties
MC_VERSION=$(grep "^minecraft_version=" gradle.properties | cut -d'=' -f2)

# Find JAR files
FABRIC_JAR=$(find fabric/build/libs -name "*-${VERSION}.jar" ! -name "*-sources.jar" ! -name "*-javadoc.jar" ! -name "*-dev.jar" | head -1)
NEOFORGE_JAR=$(find neoforge/build/libs -name "*-${VERSION}.jar" ! -name "*-sources.jar" ! -name "*-javadoc.jar" ! -name "*-dev.jar" | head -1)

if [ -z "$FABRIC_JAR" ] || [ -z "$NEOFORGE_JAR" ]; then
    echo "Error: Could not find JAR files for version $VERSION"
    echo "Fabric: $FABRIC_JAR"
    echo "NeoForge: $NEOFORGE_JAR"
    exit 1
fi

# Read changelog
if [ ! -f "$CHANGELOG_FILE" ]; then
    echo "Error: Changelog file not found: $CHANGELOG_FILE"
    exit 1
fi

CHANGELOG=$(cat "$CHANGELOG_FILE")

# Deploy Fabric
echo "Deploying Fabric JAR to CurseForge..."
curl -X POST \
    -H "X-API-Token: $CURSEFORGE_TOKEN" \
    -F "file=@$FABRIC_JAR" \
    -F "type=release" \
    -F "gameVersions=$MC_VERSION" \
    -F "displayName=Nether Portal Coordinate Scale - $VERSION (Fabric)" \
    -F "changelog=$CHANGELOG" \
    -F "changelogType=markdown" \
    -F "relations={\"projects\":[{\"slug\":\"fabric-api\",\"type\":\"requiredDependency\"}]}" \
    "https://wow.curseforge.com/api/projects/$PROJECT_ID/upload-file"

echo "✓ Fabric JAR deployed to CurseForge"

# Deploy NeoForge
echo "Deploying NeoForge JAR to CurseForge..."
curl -X POST \
    -H "X-API-Token: $CURSEFORGE_TOKEN" \
    -F "file=@$NEOFORGE_JAR" \
    -F "type=release" \
    -F "gameVersions=$MC_VERSION" \
    -F "displayName=Nether Portal Coordinate Scale - $VERSION (NeoForge)" \
    -F "changelog=$CHANGELOG" \
    -F "changelogType=markdown" \
    "https://wow.curseforge.com/api/projects/$PROJECT_ID/upload-file"

echo "✓ NeoForge JAR deployed to CurseForge"
echo ""
echo "✓ Successfully deployed version $VERSION to CurseForge"
