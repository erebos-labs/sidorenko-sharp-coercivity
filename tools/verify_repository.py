#!/usr/bin/env python3
"""Verify all frozen mathematical packages and optional release assets."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VARIANCE_ARCHIVE = "sidorenko_variance_v1.0.1.zip"
VARIANCE_SHA256 = "b8befea81b161205fee8ec90413ad368b50532a287862aa77ee0999d3325ddf1"
FULL_SLACK_ARCHIVE = "sidorenko_full_slack_v1.0.1.zip"
FULL_SLACK_SHA256 = "95ba9115ff88b93e2d875e9bfc5e17e4042c96ce0f9376ce1a8a211db8db45ce"
DEFECT_ARCHIVE = "sidorenko_defect_one_v1.0.1.zip"
DEFECT_SHA256 = "51287961912e0117300c1b87c3a3fd8f22e15d66705a49f6850e2ed9f290c9a5"
FROZEN = {
    "tools/verify_coercivity.py": "88f7aa8c8ddba92c071db120d695d767d221ebbad52e25b63abad02392971bf4",
    "variance/SHA256SUMS": "175ec3bce6e7da5e946ab6de9a347729cf822289c0063b837fb8b1c4990eb4c7",
    "artifacts/sidorenko_variance_v1.0.1.sha256": "6312fced34d9948ff41defaa5030d7d14c5a9b97809e276c1eea74670aa22da6",
    "artifacts/sidorenko_variance_v1.0.1.release.json": "1c509ba7954168d2b9378f80456cc42d1eedcc8f03bea162623c60655d37d46a",
    "full-slack/SHA256SUMS": "99e4ddf8d9576defdc30177ba336c3899b5a6acaa0ddc71973a8bb061b10e630",
    "artifacts/sidorenko_full_slack_v1.0.1.sha256": "1e2a83d4752f0d69d1593a39e913c1210fb66711758f26f03e38c99816f89f66",
    "artifacts/sidorenko_full_slack_v1.0.1.release.json": "5dd8d1ef7dac29076a78d6c25c62e20fa0a1500da875fd9ce908fd8dc932636a",
    "defect-one/SHA256SUMS": "dc867119d306102b23a518aca5a496a9939b9e1d0596ccac724df0e3e97f6f2f",
    "artifacts/sidorenko_defect_one_v1.0.1.sha256": "d106e2a3a6f92f50fb63a6400f134e3bb4e5a3112ba54602b9dc6e21e6dbc2a1",
    "artifacts/sidorenko_defect_one_v1.0.1.release.json": "98c261453b5abc62cc34043368f4f54941999b8b12d2ad2352ca69625eb9cb1b",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(arguments):
    result = subprocess.run([sys.executable, "-I", "-B", *map(str, arguments)],
                            text=True, capture_output=True, timeout=300)
    require(result.returncode == 0, "Command failed: " + Path(str(arguments[0])).name
            + "\n" + result.stdout + result.stderr)
    return result.stdout


def bindings():
    for name, expected in FROZEN.items():
        require(sha((ROOT/name).read_bytes()) == expected, "Frozen release binding changed: " + name)
    require((ROOT/"LICENSE").read_bytes() == (ROOT/"variance/LICENSE").read_bytes(),
            "Variance contribution license differs")
    receipt = json.loads((ROOT/"artifacts"/VARIANCE_ARCHIVE.replace(".zip",".release.json")).read_text())
    require(receipt["archive"]["sha256"] == VARIANCE_SHA256
            and receipt["full_replay_requires_external_source_cache"]
            and not receipt["source_cache_redistributed"]
            and not receipt["fetched_programs_executed"], "Variance release receipt differs")
    inventory = json.loads(run([ROOT/"variance/verify_package.py","--inventory-only"]))
    require(inventory["status"] == "INVENTORY_ONLY_PASS"
            and inventory["full_replay"] == "NOT_RUN"
            and inventory["retained_source_checks"] == 5
            and inventory["external_sources_required"] == 18, "Variance inventory boundary changed")
    print("PASS frozen variance manifest, licenses, metadata and 5/18 source partition", flush=True)
    require((ROOT/"LICENSE").read_bytes() == (ROOT/"full-slack/LICENSE").read_bytes(),
            "Full-slack contribution license differs")
    spec = importlib.util.spec_from_file_location("full_slack_inventory",ROOT/"full-slack/verify_package.py")
    package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(package)
    require(package.verify_manifest() == 41,"Full-slack inventory differs")
    receipt = json.loads((ROOT/"artifacts"/FULL_SLACK_ARCHIVE.replace(".zip",".release.json")).read_text())
    require(receipt["archive"]["sha256"] == FULL_SLACK_SHA256
            and receipt["repository_version"] == "v1.3.0"
            and receipt["package_version"] == "1.0.1"
            and receipt["self_contained_offline_new_package_replay"]
            and not receipt["fetched_programs_executed"],"Full-slack release receipt differs")
    print("PASS frozen full-slack manifest, MIT/Apache notices and release metadata",flush=True)
    require((ROOT/"LICENSE").read_bytes()==(ROOT/"defect-one/LICENSE").read_bytes(),
            "Defect-one contribution license differs")
    spec=importlib.util.spec_from_file_location("defect_inventory",ROOT/"defect-one/verify_package.py")
    package=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(package)
    require(package.verify_manifest()==35,"Defect-one inventory differs")
    receipt=json.loads((ROOT/"artifacts"/DEFECT_ARCHIVE.replace(".zip",".release.json")).read_text())
    require(receipt["archive"]["sha256"]==DEFECT_SHA256
            and receipt["repository_version"]=="v1.4.0" and receipt["package_version"]=="1.0.1"
            and receipt["self_contained_offline_new_package_replay"]
            and not receipt["external_source_cache_redistributed"]
            and not receipt["fetched_programs_executed"]
            and receipt["claim_scope"]["sufficient_even_D"]==600
            and receipt["claim_scope"]["evenD1198_fallback_retained"],"Defect-one receipt differs")
    print("PASS frozen defect-one manifest, licensed source boundary and conditional metadata",flush=True)


def verify_defect_assets(folder):
    require(sha((folder/DEFECT_ARCHIVE).read_bytes())==DEFECT_SHA256,"Defect-one ZIP hash differs")
    for suffix in (".sha256",".release.json"):
        name=DEFECT_ARCHIVE.replace(".zip",suffix)
        require((folder/name).read_bytes()==(ROOT/"artifacts"/name).read_bytes(),
                "Defect-one asset metadata differs: "+name)
    seen=set()
    with zipfile.ZipFile(folder/DEFECT_ARCHIVE) as z:
        require(z.testzip() is None,"Defect-one ZIP CRC failure")
        for entry in z.infolist():
            path=PurePosixPath(entry.filename)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in entry.filename
                    and len(path.parts)>1 and path.parts[0]=="sidorenko_defect_one_v1.0.1"
                    and stat.S_ISREG(entry.external_attr>>16) and not entry.flag_bits&1,
                    "Unsafe defect-one ZIP member")
            name=PurePosixPath(*path.parts[1:]).as_posix()
            require(name not in seen,"Duplicate defect-one ZIP member")
            seen.add(name)
            require(z.read(entry)==(ROOT/"defect-one"/name).read_bytes(),
                    "Defect-one ZIP/repository bytes differ: "+name)
    files={p.relative_to(ROOT/"defect-one").as_posix() for p in (ROOT/"defect-one").rglob("*") if p.is_file()}
    require(seen==files,"Defect-one ZIP/repository coverage differs")
    print("PASS defect-one ZIP hash, checksum, receipt and all "+str(len(seen))+" package files",flush=True)


def verify_full_slack_assets(folder):
    require(sha((folder/FULL_SLACK_ARCHIVE).read_bytes()) == FULL_SLACK_SHA256,"Full-slack ZIP hash differs")
    for suffix in (".sha256",".release.json"):
        name = FULL_SLACK_ARCHIVE.replace(".zip",suffix)
        require((folder/name).read_bytes() == (ROOT/"artifacts"/name).read_bytes(),
                "Full-slack asset metadata differs: " + name)
    seen=set()
    with zipfile.ZipFile(folder/FULL_SLACK_ARCHIVE) as z:
        require(z.testzip() is None,"Full-slack ZIP CRC failure")
        for entry in z.infolist():
            path=PurePosixPath(entry.filename)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in entry.filename
                    and len(path.parts)>1 and path.parts[0]=="sidorenko_full_slack_v1.0.1"
                    and stat.S_ISREG(entry.external_attr>>16) and not entry.flag_bits&1,
                    "Unsafe full-slack ZIP member")
            name=PurePosixPath(*path.parts[1:]).as_posix()
            require(name not in seen,"Duplicate full-slack ZIP member")
            seen.add(name)
            require(z.read(entry)==(ROOT/"full-slack"/name).read_bytes(),
                    "Full-slack ZIP/repository bytes differ: "+name)
    files={p.relative_to(ROOT/"full-slack").as_posix() for p in (ROOT/"full-slack").rglob("*") if p.is_file()}
    require(seen==files,"Full-slack ZIP/repository coverage differs")
    print("PASS full-slack ZIP hash, checksum, receipt and all "+str(len(seen))+" package files",flush=True)


def verify_variance_assets(folder):
    require(sha((folder/VARIANCE_ARCHIVE).read_bytes()) == VARIANCE_SHA256, "Variance ZIP hash differs")
    for suffix in (".sha256",".release.json"):
        name = VARIANCE_ARCHIVE.replace(".zip",suffix)
        require((folder/name).read_bytes() == (ROOT/"artifacts"/name).read_bytes(),
                "Variance asset metadata differs: " + name)
    seen = set()
    with zipfile.ZipFile(folder/VARIANCE_ARCHIVE) as z:
        require(z.testzip() is None, "Variance ZIP CRC failure")
        for entry in z.infolist():
            path = PurePosixPath(entry.filename)
            require(not path.is_absolute() and ".." not in path.parts
                    and "\\" not in entry.filename
                    and path.parts[0] == "sidorenko_variance_v1.0.1"
                    and stat.S_ISREG(entry.external_attr>>16) and not entry.flag_bits & 1,
                    "Unsafe variance ZIP member")
            name = PurePosixPath(*path.parts[1:]).as_posix()
            require(name not in seen, "Duplicate variance ZIP member")
            seen.add(name)
            require(z.read(entry) == (ROOT/"variance"/name).read_bytes(),
                    "Variance ZIP/repository bytes differ: " + name)
    files = {p.relative_to(ROOT/"variance").as_posix()
             for p in (ROOT/"variance").rglob("*") if p.is_file()}
    require(seen == files, "Variance ZIP/repository coverage differs")
    print("PASS variance ZIP hash, checksum, receipt and all " + str(len(seen)) + " package files",flush=True)


def assets(folder):
    found = False
    if (folder/DEFECT_ARCHIVE).is_file():
        verify_defect_assets(folder)
        found = True
    if (folder/FULL_SLACK_ARCHIVE).is_file():
        verify_full_slack_assets(folder)
        found = True
    if (folder/VARIANCE_ARCHIVE).is_file():
        verify_variance_assets(folder)
        found = True
    if (folder/"sidorenko_sharp_constant_v1.1.0.zip").is_file():
        spec = importlib.util.spec_from_file_location("frozen_coercivity_assets",
                                                     ROOT/"tools/verify_coercivity.py")
        legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(legacy)
        legacy.verify_assets(ROOT, folder)
        found = True
    require(found, "No supported release archive in release directory")


def replay(cache):
    require(cache != ROOT and ROOT not in cache.parents and cache not in ROOT.parents,
            "Keep the source cache separate from the repository")
    fetched = json.loads(run([ROOT/"variance/fetch_sources.py","--cache",cache]))
    require(fetched["status"] == "SOURCE_CACHE_VERIFIED" and fetched["files"] == 18
            and not fetched["programs_executed"], "Source cache validation failed")
    full = json.loads(run([ROOT/"variance/verify_package.py","--source-cache",cache,"--regenerate"]))
    require(full["status"] == "FULL_REPLAY_PASS"
            and full["retained_source_checks"] == 5 and full["external_source_checks"] == 18
            and len(full["checks"]) == 7 and not full["retrieved_programs_executed"],
            "Full variance replay failed")
    controls = json.loads(run([ROOT/"variance/test_release.py","--source-cache",cache]))
    require(controls["status"] == "PASS" and len(controls["controls"]) == 18,
            "Variance packaging controls failed")
    print("PASS variance: all 23 sources; 35 local/19 downstream identities; eight original mutation rejections",flush=True)
    print("PASS independent 1,251,801 local tuples/625 boundaries/24 probes/14,757 activity tests",flush=True)
    print("PASS byte-identical regeneration and all 18 packaging/retrieval controls; cached programs never executed",flush=True)


def main():
    require(sys.flags.optimize == 0,"Use Python without -O/-OO")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-cache",type=Path)
    parser.add_argument("--release-dir",type=Path)
    parser.add_argument("--assets-only",action="store_true")
    args = parser.parse_args()
    if args.assets_only and not args.release_dir:
        parser.error("--assets-only requires --release-dir")
    bindings()
    if not args.assets_only:
        print(run([ROOT/"tools/verify_coercivity.py"]),end="",flush=True)
        if args.source_cache:
            replay(args.source_cache.resolve())
        else:
            with TemporaryDirectory(prefix="sidorenko-public-source-cache-") as tmp:
                replay(Path(tmp).resolve())
        full = json.loads(run([ROOT/"full-slack/verify_package.py"]))
        require(full["status"]=="PASS" and full["manifest_files"]==41
                and len(full["fresh_working_directory_replay"])==3
                and all(check["recorded_JSON_matches"] for check in full["fresh_working_directory_replay"])
                and full["packaging_controls"]["rejection_controls"]==18
                and full["optimized_execution"]=="REJECTED_AS_EXPECTED","Full-slack replay failed")
        print("PASS full-slack: 46 local/10 downstream identities, 21 examples, 12 math mutations and 18 packaging rejections",flush=True)
        defect=json.loads(run([ROOT/"defect-one/verify_package.py"]))
        require(defect["status"]=="PASS" and defect["manifest_files"]==35
                and len(defect["runs"])==2 and all(check["byte_identical"] for check in defect["runs"])
                and defect["packaging_controls"]["rejection_controls"]==18,"Defect-one replay failed")
        print("PASS defect-one: 25 identities, 6 source bindings, geometric/weighted controls, 14 math mutations and 18 packaging rejections",flush=True)
    if args.release_dir:
        assets(args.release_dir.resolve())
    if args.assets_only:
        print("PASS downloaded assets; arithmetic NOT_RUN in assets-only mode",flush=True)
    else:
        print("PASS all four packages and scoped conditional certificates; conventional proofs remain necessary",flush=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError,OSError,ValueError,KeyError,subprocess.TimeoutExpired,zipfile.BadZipFile) as err:
        print("FAIL repository verification: " + str(err),file=sys.stderr)
        raise SystemExit(1)
