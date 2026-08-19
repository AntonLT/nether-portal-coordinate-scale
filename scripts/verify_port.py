#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIXIN_CLASS = "com.example.examplemod.mixin.DimensionTypeMixin"
MIXIN_CLASS_PATH = MIXIN_CLASS.replace(".", "/") + ".class"
MIXIN_CONFIG = "netherportalcoordinatescale.mixins.json"


def fail(message: str) -> None:
    raise RuntimeError(message)


def verify_source() -> None:
    source = (ROOT / "common/src/main/java/com/example/examplemod/mixin/DimensionTypeMixin.java").read_text()
    if "Services.PLATFORM.getConfigScale()" not in source:
        fail("Mixin does not read platform config")
    if "setReturnValue(1.0)" in source:
        fail("Mixin still returns a hardcoded scale")

    config = json.loads((ROOT / f"common/src/main/resources/{MIXIN_CONFIG}").read_text())
    if "DimensionTypeMixin" not in config.get("mixins", []):
        fail("DimensionTypeMixin is not registered as a general mixin")
    if any("DimensionTypeMixin" in config.get(side, []) for side in ("client", "server")):
        fail("DimensionTypeMixin is side-specific")
    if config.get("compatibilityLevel") != "JAVA_25":
        fail("Mixin compatibility level is not JAVA_25")


def release_jar(loader: str) -> Path:
    jars = [
        path
        for path in (ROOT / loader / "build/libs").glob("*.jar")
        if not any(marker in path.stem for marker in ("-sources", "-javadoc", "-dev", "-shadow"))
    ]
    if len(jars) != 1:
        fail(f"Expected one {loader} release JAR, found {len(jars)}")
    return jars[0]


def verify_artifact(loader: str) -> None:
    jar = release_jar(loader)
    with zipfile.ZipFile(jar) as archive:
        names = set(archive.namelist())
        if MIXIN_CONFIG not in names:
            fail(f"{loader} JAR does not contain {MIXIN_CONFIG}")
        if MIXIN_CLASS_PATH not in names:
            fail(f"{loader} JAR does not contain {MIXIN_CLASS_PATH}")

    result = subprocess.run(
        ["javap", "-classpath", str(jar), "-c", "-p", MIXIN_CLASS],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(f"javap failed for {loader}: {result.stderr.strip()}")
    if "getConfigScale:()D" not in result.stdout:
        fail(f"{loader} Mixin bytecode does not read platform config")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the Minecraft 26.x port")
    parser.add_argument("--artifacts", action="store_true", help="also inspect built loader JARs")
    args = parser.parse_args()

    try:
        verify_source()
        if args.artifacts:
            for loader in ("fabric", "neoforge"):
                verify_artifact(loader)
    except (OSError, RuntimeError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print(error, file=sys.stderr)
        return 1

    print("Port verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
