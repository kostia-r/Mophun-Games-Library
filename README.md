# Mophun Games Library

A curated and normalized collection of Mophun game releases organized by target device profile.

The library is intended for compatibility testing, preservation research, and use with Mophun-compatible runtimes such as OpenMophun.

## Library status

Current canonical set:

* **435 unique Mophun releases**
* **136** T3xx
* **126** T6xx
* **86** T3xx + T6xx compatible
* **24** UIQ3
* **63** currently unclassified

SDK samples under `SDK/` are kept in the repository but are not part of the canonical release set.

Profile counts reflect confirmed runtime evidence from the STM32 compatibility sweep: T3xx vs T6xx mismatches were reclassified; uncertain titles remain in `Unknown`.

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

Valid Mophun releases for which the target profile has not yet been identified with sufficient confidence.

Files are kept here rather than being classified heuristically.

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
* Historical runtime dates that cannot be recovered from the game binary may remain as `[run YYYY-MM-DD]`.

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
runtime_date_overrides.csv
canonical_runtime_sha256.txt
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
MPN: 435 / unique 435
Profiles: T3xx=136, T6xx=126, T3xx+T6xx=86, UIQ3=24, Unknown=63
MPC placements: 20
language sidecars: 8

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

Uncertain releases should remain in `Unknown`.

## Rights

Mophun game binaries and associated game assets are third-party works and remain the property of their respective authors, developers, publishers, and other rights holders.

This repository does not claim ownership of third-party game content.

Project-generated metadata, verification tools, and other original repository material should be treated separately from the game binaries. See `RIGHTS.md` for details.
