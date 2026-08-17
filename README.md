# Mophun Games Library

A curated and normalized collection of Mophun game releases organized by target device profile.

The library is intended for compatibility testing, preservation research, and use with Mophun-compatible runtimes such as OpenMophun.

## Library status

Current canonical set:

* **411 unique Mophun releases**
* **170** T3xx
* **145** T6xx
* **69** T3xx + T6xx compatible
* **27** UIQ3
* **0** currently unclassified

SDK samples under `SDK/` are kept in the repository but are not part of the canonical release set.

Profile counts follow the current folder layout. Remaining `Unknown` titles were classified into T3xx, T6xx, T3xx+T6xx, or UIQ3; titles removed from the tree are no longer in the canonical set.

Exact binary duplicates, broken archive artifacts, incomplete multipart files, and non-Mophun files have been removed.

## Profiles

### `T3xx`

Games targeting the Sony Ericsson T3xx device family and compatible low-resolution profiles.

Typical display profile: **101×80**.

### `T6xx`

Games targeting the Sony Ericsson T6xx device family, including T610-class devices.

Typical display profile: **128×160**.

### `T3xx+T6xx`

Game releases known to be compatible with both T3xx and T6xx profiles.

### `UIQ3`

Mophun releases targeting Symbian UIQ 3 devices.

### `Unknown`

Reserved for valid Mophun releases whose target profile is not yet identified with sufficient confidence.

The current canonical set has classified every remaining title, so this folder is empty.

## Release naming

Filenames are intentionally kept compact for use on embedded devices.

Examples:

```text
Deep Abyss.mpn
Game [Demo].mpn
Game [v1.0].mpn
Game [v1.1].mpn
```

Rules:

* Full releases are not explicitly marked.
* Demo releases use `[Demo]`.
* Version numbers are shown only when needed to distinguish multiple releases.
* Short release identifiers are used only when otherwise indistinguishable binaries exist.
* Dates embedded directly in Mophun metadata are not included in filenames.
* Historical runtime dates that cannot be recovered from the game binary live in the parent folder name (`run YYYY-MM-DD` or `date YYYY-MM-DD..YYYY-MM-DD`), not in the `.mpn` filename.

## External resources

Some games require additional files alongside the main `.mpn`.

These include:

```text
*.mpc
language
```

Such files are part of the corresponding game release and should be copied together with its `.mpn`.

Do not move an `.mpn` out of its release directory without also checking for these sidecar files.

## Metadata

The `_meta` directory contains machine-readable information used to verify and maintain the library.

Important files include:

```text
library_manifest.csv
date_rules.csv
runtime_date_overrides.csv
canonical_runtime_sha256.txt
canonical_mpc_sha256_multiset.txt
canonical_language_sha256_multiset.txt
CANONICAL_FINGERPRINT.txt
```

The manifest records the canonical SHA-256 identity and location of each release.

## Verification

The library can be verified with:

```bash
python tools/verify_library.py .
```

Expected result:

```text
MPN: 411 / unique 411
Profiles: T3xx=170, T6xx=145, T3xx+T6xx=69, UIQ3=27, Unknown=0
MPC placements: 20
language sidecars: 6
date rules: 94
dates.txt: 4

LIBRARY STATUS: CANONICAL-COMPLETE
```

Some `.mpc` filename-reference checks may currently produce non-fatal review warnings. These do not indicate missing content.

## Repository maintenance

New releases should be compared by binary hash before being added.

A different filename does not necessarily mean a different release, while two files with the same game title may represent genuinely different versions.

Profile changes should only be made when supported by reliable evidence such as:

* original target-device information;
* game metadata;
* binary evidence;
* matching releases from known device-specific distributions;
* confirmed runtime behavior.

Uncertain new releases should go in `Unknown` until classified.

## Rights

Mophun game binaries and associated game assets are third-party works and remain the property of their respective authors, developers, publishers, and other rights holders.

This repository does not claim ownership of third-party game content.

Project-generated metadata, verification tools, and other original repository material should be treated separately from the game binaries. See `RIGHTS.md` for details.
