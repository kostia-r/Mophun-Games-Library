#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, collections, csv

EXPECTED_COUNTS = {"T3xx":170,"T6xx":145,"T3xx+T6xx":69,"UIQ3":27,"Unknown":0}
EXPECTED_UNIQUE = sum(EXPECTED_COUNTS.values())
PROFILES = tuple(EXPECTED_COUNTS)
MPN_NAME_RULES = {
    "3679fac1":"EvilMirror.mpn", "f1c5d7e1":"EvilMirror.mpn",
    "07b76379":"Rally.mpn", "669f69b0":"Rally.mpn", "a8e33782":"Rally.mpn",
    "54f8b17d":"DragonTale.mpn", "688250d5":"DragonTale.mpn", "9ab16526":"DragonTale.mpn",
    "be99f382":"RCBattle.mpn",
    "e3fd4522":"microwar.mpn", "f665dde8":"microwar.mpn",
    "46e93ab8":"VRally.mpn", "dfbab38d":"VRally.mpn",
}

def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()

def load_lines(p):
    return [x.strip() for x in p.read_text(encoding="ascii").splitlines() if x.strip()]

def profile_files(root, suffix=None, name=None):
    found=[]
    for profile in PROFILES:
        folder=root/profile
        if not folder.is_dir():
            continue
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            if suffix is not None and path.suffix.lower()!=suffix:
                continue
            if name is not None and path.name.lower()!=name.lower():
                continue
            found.append(path)
    return sorted(found)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("library",type=Path)
    ap.add_argument("--data-dir",type=Path,default=Path(__file__).resolve().parent.parent/"_meta")
    args=ap.parse_args()
    root=args.library.resolve(); data=args.data_dir.resolve()

    expected_runtime=set(load_lines(data/"canonical_runtime_sha256.txt"))
    expected_mpc=collections.Counter(load_lines(data/"canonical_mpc_sha256_multiset.txt"))
    expected_lang=collections.Counter(load_lines(data/"canonical_language_sha256_multiset.txt"))

    with (data/"date_rules.csv").open(encoding="utf-8-sig",newline="") as f:
        date_rules={r["release_id"]:r for r in csv.DictReader(f)}

    with (data/"library_manifest.csv").open(encoding="utf-8-sig",newline="") as f:
        manifest=list(csv.DictReader(f))
    man_by_hash={row["sha256"]:row for row in manifest}

    mpns = profile_files(root, suffix=".mpn")
    mpcs = profile_files(root, suffix=".mpc")
    langs = profile_files(root, name="language")
    errors=[]

    actual={}
    for p in mpns:
        b=p.read_bytes()
        rel=p.relative_to(root).as_posix()
        profile=rel.split("/",1)[0]
        if not b.startswith(b"VMGP"):
            errors.append(f"non-VMGP: {rel}")
        h=hashlib.sha256(b).hexdigest(); rid=h[:8]; actual[h]=p
        if "[run " in p.name or "[date " in p.name:
            errors.append(f"date leaked into MPN filename: {rel}")
        if rid in MPN_NAME_RULES and p.name != MPN_NAME_RULES[rid]:
            errors.append(f"wrong MPC-linked MPN name for {rid}: {p.name}, expected {MPN_NAME_RULES[rid]}")
        if profile not in EXPECTED_COUNTS:
            errors.append(f"MPN outside profile folders: {rel}")

        row=man_by_hash.get(h)
        if row is None:
            errors.append(f"missing from manifest: {rel}")
        else:
            man_path=row["path"].replace("\\","/")
            if man_path!=rel:
                errors.append(f"manifest path stale for {rid}: {man_path} != {rel}")
            if row["profile"]!=profile:
                errors.append(f"manifest profile stale for {rid}: {row['profile']} != {profile}")

        rule=date_rules.get(rid)
        if rule:
            if rule["mode"]=="conflict":
                dt=p.parent/"dates.txt"
                if not dt.exists():
                    errors.append(f"missing dates.txt for {rid}: {rel}")
                else:
                    txt=dt.read_text(encoding="utf-8",errors="replace")
                    for d in [x for x in rule["candidate_dates"].split("|") if x]:
                        if d not in txt:
                            errors.append(f"dates.txt for {rid} misses {d}")
            else:
                label=rule["folder_label"]
                if label and label not in p.parent.name:
                    errors.append(f"date folder mismatch for {rid}: parent={p.parent.name!r}, expected to contain {label!r}")

    extra_manifest=set(man_by_hash)-set(actual)
    if extra_manifest:
        errors.append(f"manifest has {len(extra_manifest)} hashes not on disk")
        for h in sorted(extra_manifest)[:12]:
            errors.append(f"  extra manifest {h[:8]} {man_by_hash[h]['path']}")
    if len(manifest)!=EXPECTED_UNIQUE or len(man_by_hash)!=EXPECTED_UNIQUE:
        errors.append(
            f"manifest size {len(manifest)} unique={len(man_by_hash)}, expected {EXPECTED_UNIQUE}"
        )

    if set(actual)!=expected_runtime:
        errors.append(f"runtime hash set mismatch: missing={len(expected_runtime-set(actual))} extra={len(set(actual)-expected_runtime)}")
    fingerprint=hashlib.sha256("\n".join(sorted(actual)).encode("ascii")).hexdigest()
    fp_text=(data/"CANONICAL_FINGERPRINT.txt").read_text(encoding="ascii")
    if f"releases={EXPECTED_UNIQUE}" not in fp_text or fingerprint not in fp_text:
        errors.append("canonical fingerprint mismatch")
    if len(mpns) != EXPECTED_UNIQUE or len(actual) != EXPECTED_UNIQUE:
        errors.append(
            f"expected {EXPECTED_UNIQUE} unique MPN, got placements={len(mpns)} unique={len(actual)}"
        )

    if collections.Counter(sha256(p) for p in mpcs)!=expected_mpc:
        errors.append("MPC content multiset mismatch")
    if collections.Counter(sha256(p) for p in langs)!=expected_lang:
        errors.append("language content multiset mismatch")

    counts={}
    for profile in EXPECTED_COUNTS:
        d=root/profile
        counts[profile]=sum(1 for p in mpns if d in p.parents)
    if counts!=EXPECTED_COUNTS:
        errors.append(f"profile distribution mismatch: {counts}")

    print(f"MPN: {len(mpns)} / unique {len(actual)}")
    print("Profiles: "+", ".join(f"{k}={counts[k]}" for k in EXPECTED_COUNTS))
    print(f"MPC placements: {len(mpcs)}")
    print(f"language sidecars: {len(langs)}")
    print(f"date rules: {len(date_rules)}")
    print(f"dates.txt: {len(profile_files(root, name='dates.txt'))}")

    if errors:
        print("\nERRORS:")
        for e in errors: print(" -",e)
        print("\nLIBRARY STATUS: FAIL")
        return 2
    print("\nLIBRARY STATUS: CANONICAL-COMPLETE")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
