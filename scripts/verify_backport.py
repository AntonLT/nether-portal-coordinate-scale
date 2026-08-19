#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIXIN_CLASS = "com.example.examplemod.mixin.DimensionTypeMixin"
MIXIN_ENTRY = "com/example/examplemod/mixin/DimensionTypeMixin.class"
REJECTED_SUFFIXES = ("-sources.jar", "-javadoc.jar", "-dev.jar")


def fail(message: str) -> None:
    raise SystemExit(message)


def properties() -> dict[str, str]:
    result = {}
    for raw in (ROOT / "gradle.properties").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def verify_source(props: dict[str, str]) -> list[str]:
    mixin = (ROOT / "common/src/main/java/com/example/examplemod/mixin/DimensionTypeMixin.java").read_text(encoding="utf-8")
    if "Services.PLATFORM.getConfigScale()" not in mixin:
        fail("Mixin does not read platform config")
    if re.search(r"setReturnValue\(\s*1\.0[Dd]?\s*\)", mixin):
        fail("Mixin still returns literal 1.0")

    registration = json.loads((ROOT / "common/src/main/resources/netherportalcoordinatescale.mixins.json").read_text(encoding="utf-8"))
    if "DimensionTypeMixin" not in registration.get("mixins", []):
        fail("DimensionTypeMixin is not generally registered")
    if "DimensionTypeMixin" in registration.get("client", []):
        fail("DimensionTypeMixin remains client-only")
    if "DimensionTypeMixin" in registration.get("server", []):
        fail("DimensionTypeMixin must not be duplicated in server")
    if props.get("version") != "1.0.2":
        fail(f"Expected version 1.0.2, found {props.get('version')!r}")

    fabric_config = (ROOT / "fabric/src/main/java/com/example/examplemod/config/Config.java").read_text(encoding="utf-8")
    for token in ("JsonParseException", "Double.isFinite", "MIN_SCALE", "MAX_SCALE"):
        if token not in fabric_config:
            fail(f"Fabric config is missing validation token {token}")

    fabric_helper = (ROOT / "fabric/src/main/java/com/example/examplemod/platform/FabricPlatformHelper.java").read_text(encoding="utf-8")
    if "return Config.getInstance().scale;" not in fabric_helper:
        fail("Fabric helper does not return the loaded scale")

    loaders = ["fabric"]
    secondary = "neoforge" if (ROOT / "neoforge").is_dir() else "forge"
    secondary_helper = (ROOT / secondary / f"src/main/java/com/example/examplemod/platform/{'NeoForge' if secondary == 'neoforge' else 'Forge'}PlatformHelper.java").read_text(encoding="utf-8")
    secondary_config = (ROOT / secondary / "src/main/java/com/example/examplemod/config/Config.java").read_text(encoding="utf-8")
    if "return Config.INSTANCE.SCALE.get();" not in secondary_helper:
        fail(f"{secondary} helper does not return the loaded scale")
    if not all(value in secondary_config for value in ("defineInRange", "1.0", "0.01", "64.0")):
        fail(f"{secondary} config does not enforce the scale range")
    loaders.append(secondary)
    return loaders


def release_jar(loader: str, version: str) -> Path:
    candidates = [
        path for path in (ROOT / loader / "build/libs").glob("*.jar")
        if version in path.name and not path.name.endswith(REJECTED_SUFFIXES)
    ]
    if len(candidates) != 1:
        fail(f"Expected one {loader} release JAR, found {[p.name for p in candidates]}")
    return candidates[0]


def verify_metadata(jar: Path, loader: str, props: dict[str, str]) -> None:
    with zipfile.ZipFile(jar) as archive:
        names = set(archive.namelist())
        for required in (MIXIN_ENTRY, "netherportalcoordinatescale.mixins.json", "META-INF/MANIFEST.MF"):
            if required not in names:
                fail(f"{jar.name} is missing {required}")
        manifest = archive.read("META-INF/MANIFEST.MF").decode("utf-8", "replace")
        if f"Built-On-Minecraft: {props['minecraft_version']}" not in manifest:
            fail(f"{jar.name} has wrong Minecraft manifest metadata")
        if loader == "fabric":
            metadata = json.loads(archive.read("fabric.mod.json"))
            if metadata.get("id") != "netherportalcoordinatescale" or metadata.get("version") != "1.0.2":
                fail(f"{jar.name} has wrong Fabric id/version")
            if props["minecraft_version"] not in metadata.get("depends", {}).get("minecraft", ""):
                fail(f"{jar.name} has wrong Fabric Minecraft metadata")
        else:
            metadata_name = "META-INF/neoforge.mods.toml" if loader == "neoforge" else "META-INF/mods.toml"
            metadata = archive.read(metadata_name).decode("utf-8")
            if 'modId = "netherportalcoordinatescale"' not in metadata and 'modId="netherportalcoordinatescale"' not in metadata:
                fail(f"{jar.name} has wrong {loader} mod id")
            if 'version = "1.0.2"' not in metadata and 'version="1.0.2"' not in metadata:
                fail(f"{jar.name} has wrong {loader} version")
            if props["minecraft_version"] not in metadata:
                fail(f"{jar.name} has wrong {loader} Minecraft metadata")


def verify_bytecode(jar: Path) -> None:
    output = subprocess.run(
        ["javap", "-classpath", str(jar), "-c", "-p", MIXIN_CLASS],
        check=True, text=True, capture_output=True,
    ).stdout
    if "IPlatformHelper.getConfigScale:()D" not in output:
        fail(f"{jar.name} Mixin bytecode does not invoke getConfigScale()")
    if re.search(r"dconst_1\s+\d+: invokestatic\s+.*Double\.valueOf", output):
        fail(f"{jar.name} Mixin bytecode returns constant 1.0")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", action="store_true")
    args = parser.parse_args()
    props = properties()
    loaders = verify_source(props)
    if args.artifacts:
        dist = ROOT / "dist"
        if dist.exists():
            shutil.rmtree(dist)
        dist.mkdir()
        for loader in loaders:
            jar = release_jar(loader, props["version"])
            verify_metadata(jar, loader, props)
            verify_bytecode(jar)
            shutil.copy2(jar, dist / f"netherportalcoordinatescale-{loader}-{props['minecraft_version']}-{props['version']}.jar")
    print(f"Verified Minecraft {props['minecraft_version']}: {', '.join(loaders)}")


if __name__ == "__main__":
    main()
