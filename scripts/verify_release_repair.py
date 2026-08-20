from pathlib import Path

try:
    import yaml
except ImportError as error:
    raise SystemExit(
        "Install verifier dependencies: python -m pip install -r "
        "scripts/requirements-release-verifier.txt"
    ) from error


workflow = Path(".github/workflows/repair-v1.0.2-1.21.11.yml")
data = yaml.load(workflow.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)

assert data["on"] == {"workflow_dispatch": ""}
assert data["permissions"] == {"contents": "write"}

steps = data["jobs"]["repair"]["steps"]
by_name = {step["name"]: step for step in steps}

checkout = by_name["Checkout immutable release tag"]
assert checkout["with"]["ref"] == "v1.0.2-1.21.11"

commands = (
    by_name["Guard release identity and missing destinations"]["run"]
    + by_name["Rebuild and verify tagged artifacts"]["run"]
)
for token in (
    "6f7a17e9471572f5c7b64680d572931e7c02f5b0",
    "version=1.0.2",
    "minecraft_version=1.21.11",
    "java_version=21",
    "python3 scripts/verify_backport.py --artifacts",
):
    assert token in commands

guard = by_name["Guard configured marketplace state"]["run"]
for token in (
    "v2/project/$MODRINTH_PROJECT_ID/version",
    'test "$CURSEFORGE_PROJECT_ID" = "1282016"',
    "CurseForge Fabric file 8690943",
):
    assert token in guard
assert "api/projects/$CURSEFORGE_PROJECT_ID/files" not in guard
assert "update-file" not in guard
assert "CURSEFORGE_TOKEN" not in by_name["Guard configured marketplace state"].get("env", {})

fabric = by_name["Publish missing Fabric Modrinth version"]
assert fabric["with"]["name"] == "NPCS 1.0.2 1.21.11 Fabric"
assert fabric["with"]["version"] == "1.0.2-1.21.11-fabric"
assert "modrinth-token" in fabric["with"]
assert "curseforge-token" not in fabric["with"]
assert "github-token" not in fabric["with"]

neoforge_modrinth = by_name["Publish missing NeoForge Modrinth version"]
assert neoforge_modrinth["with"]["name"] == "NPCS 1.0.2 1.21.11 NeoForge"
assert "modrinth-token" in neoforge_modrinth["with"]
assert "curseforge-token" not in neoforge_modrinth["with"]

github = by_name["Create GitHub release"]["run"]
assert 'gh release create "v1.0.2-1.21.11"' in github
assert github.count("dist/netherportalcoordinatescale-") == 2
assert "--verify-tag" in github

neoforge_curseforge = by_name["Publish missing NeoForge CurseForge file"]
assert neoforge_curseforge["with"]["name"] == "NPCS 1.0.2 1.21.11 NeoForge"
assert "curseforge-token" in neoforge_curseforge["with"]
assert "modrinth-token" not in neoforge_curseforge["with"]
assert steps.index(fabric) < steps.index(by_name["Create GitHub release"])
assert steps.index(neoforge_modrinth) < steps.index(by_name["Create GitHub release"])
assert steps.index(neoforge_curseforge) < steps.index(by_name["Create GitHub release"])

print("Release repair workflow contract verified")
