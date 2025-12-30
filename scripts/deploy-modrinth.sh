#!/bin/bash
# Deploy to Modrinth
# Usage: ./scripts/deploy-modrinth.sh <version> <changelog_file> <modrinth_token>

set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <version> <changelog_file> <modrinth_token>"
    echo ""
    echo "Example: $0 1.21.5 CHANGELOG.md your_modrinth_token"
    exit 1
fi

VERSION=$1
CHANGELOG_FILE=$2
MODRINTH_TOKEN=$3
PROJECT_ID=${MODRINTH_PROJECT_ID:-}

if [ -z "$PROJECT_ID" ]; then
    echo "Error: MODRINTH_PROJECT_ID environment variable not set"
    echo "Set it with: export MODRINTH_PROJECT_ID=<your_project_id>"
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

# Create JSON payload for Modrinth
MODRINTH_PAYLOAD=$(cat <<EOF
{
  "version_number": "$VERSION",
  "game_versions": ["$MC_VERSION"],
  "release_channel": "release",
  "loaders": ["fabric", "neoforge"],
  "featured": true,
  "changelog": "$CHANGELOG"
}
EOF
)

echo "Deploying to Modrinth..."

# Deploy Fabric JAR
echo "Uploading Fabric JAR..."
FABRIC_RESPONSE=$(curl -s -X POST \
    -H "Authorization: $MODRINTH_TOKEN" \
    -F "data=$MODRINTH_PAYLOAD" \
    -F "files=@$FABRIC_JAR" \
    "https://api.modrinth.com/api/v1/projects/$PROJECT_ID/versions")

echo "$FABRIC_RESPONSE" | grep -q "error" && {
    echo "✗ Error uploading Fabric JAR"
    echo "$FABRIC_RESPONSE"
    exit 1
} || echo "✓ Fabric JAR uploaded"

# Deploy NeoForge JAR
echo "Uploading NeoForge JAR..."
NEOFORGE_RESPONSE=$(curl -s -X POST \
    -H "Authorization: $MODRINTH_TOKEN" \
    -F "data=$MODRINTH_PAYLOAD" \
    -F "files=@$NEOFORGE_JAR" \
    "https://api.modrinth.com/api/v1/projects/$PROJECT_ID/versions")

echo "$NEOFORGE_RESPONSE" | grep -q "error" && {
    echo "✗ Error uploading NeoForge JAR"
    echo "$NEOFORGE_RESPONSE"
    exit 1
} || echo "✓ NeoForge JAR uploaded"

echo ""
echo "✓ Successfully deployed version $VERSION to Modrinth"
