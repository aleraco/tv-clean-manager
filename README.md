# TV Clean Manager

**ADB-powered package management for Android TV & Google TV — with backups, guided actions, and a community-maintained experience catalog.**

[![Release](https://img.shields.io/badge/release-v0.7.0%20Beta-orange)](https://github.com/aleraco/tv-clean-manager/releases/tag/v0.7.0)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11%20x64-blue)](https://github.com/aleraco/tv-clean-manager/releases)
[![Community](https://img.shields.io/badge/community-explore%20reports-green)](https://aleraco.github.io/tv-clean-manager/)

**[Download the beta](https://github.com/aleraco/tv-clean-manager/releases/tag/v0.7.0)** · **[Explore the Community](https://aleraco.github.io/tv-clean-manager/)** · **[Report an issue](https://github.com/aleraco/tv-clean-manager/issues)**

> **Beta software — read before using.** Disabling a critical Android TV package can remove essential functions or prevent the device from booting. The application's backups are diagnostic snapshots and operation records, **not full firmware images or a guaranteed recovery method**. Community reports are user-submitted evidence, not proof that a change is safe on your device.

## What is TV Clean Manager?

TV Clean Manager is a Windows desktop tool for inspecting and managing application packages on compatible Android TV and Google TV devices over **ADB (Android Debug Bridge)**. The Windows executable includes the ADB components: users do not need to install Android SDK Platform-Tools separately.

The project combines a guided package-management interface with a public, searchable catalog of actions reported by users for specific **models, firmware versions, packages, and actions**.

### Current features (v0.7.0 Beta)

- Connect to a compatible TV using its **local IP address** and ADB port.
- Identify manufacturer, Android product, SDK level and firmware information.
- Search and inspect installed, enabled and disabled packages, including protected packages.
- Create diagnostic backups and preserve operation history.
- Offer guided package actions **only where the application's current safety rules allow them**; preserve protected system packages.
- Record and export previous manual ADB actions, external-tool actions, and app-recorded operations as separate sources.
- Import local community reports and open the public catalog.

**Scope:** the diagnostic features are intended for compatible Android TV / Google TV devices. Guided write operations are still restricted; broad device compatibility and real-world restoration have **not** been validated. The launcher-installation wizard is planned work, **not** a feature of this beta.

## Download and quick start

1. Visit **[GitHub Releases](https://github.com/aleraco/tv-clean-manager/releases/tag/v0.7.0)** and download the **application ZIP** from **Assets** (not GitHub's automatically generated *Source code* archives).
2. Extract the ZIP and run `TVCleanManager.exe` on **Windows 10/11 x64**.
3. On the TV, enable the applicable developer and network ADB debugging settings. These vary by manufacturer and Android version.
4. Enter the TV's **local network IP address** (and port, where applicable) in the application.
5. Approve the ADB authorization prompt **on the TV**, if one appears. Connect, inspect the package list, and create a backup **before considering any change**.
6. After use, consider disconnecting ADB and disabling debugging on the TV.

ADB connectivity is required for live device operations. Some televisions do not expose network ADB or use different pairing procedures; support is not universal.

## Community: who did what, and how?

**[Browse published experiences](https://aleraco.github.io/tv-clean-manager/)**

Each public action is associated with the contributor's declared identity, device model/product, Android SDK, firmware, target package, action and execution method. **Reboot** and **actual restoration** are reported separately.

| Method | Meaning | Counts as an independent manual-ADB testimony? |
| --- | --- | --- |
| `adb_manual` | A contributor reports performing the action directly through ADB | Potentially, after review |
| `external_tool` | A contributor reports using another script or utility | No |
| App-executed | TV Clean Manager recorded the operation | No; tracked separately |

**Two independent, matching manual-ADB testimonies** for the same **model + firmware + package + action** create a *candidate for community corroboration*, **not a safety certification**. Distinct nicknames alone do not establish independence. Moderators must review contributor identity and the underlying evidence. Subsequent app-executed actions are tracked separately, and **no community report automatically unlocks protected packages**.

A successful ADB command, a successful reboot, and a successful restoration are three different claims. Unknown or missing results must not be presented as successful tests.

### First published device example

The catalog includes a self-reported experience for a **Sony KD-55XE9005**, Android 9 / SDK 28, firmware **672201**, attributed to **`aleraco`**. It describes three Sony package disables and three actions involved in switching to the CleanYourTV launcher. A successful reboot was reported; **restoration on hardware was not documented**. It is **one contributor's experience**, not two independent confirmations.

## Contribute a report

1. Use the application's **Community** section to record your experience, including whether the action was performed manually with ADB, with another tool, or by TV Clean Manager.
2. Review the exported **schema-3 JSON**. Correct the model, firmware, action names, package names, contributor nickname and test results. Remove unnecessary installed-app inventory.
3. **Do not publish** IP addresses, serial numbers, ADB keys, raw logs, full device fingerprints, backup paths, tokens, or other private information.
4. Submit a **pull request** adding the reviewed JSON file to [`reports/`](https://github.com/aleraco/tv-clean-manager/tree/main/reports). The submission may require maintainer review; a pull request is not an approved experience.

**A GitHub account is currently needed to submit through pull requests.** Viewing the Community catalog does not require an account. Public authorship and declarations are not independently authenticated merely because they appear in a JSON file.

## Repository structure

| Path | Purpose |
| --- | --- |
| `reports/` | Reviewed community report JSON files |
| `scripts/build_catalog.py` | Validate reports and generate the public catalog |
| `tests/` | Tests for community-data generation and validation |
| `site/` | Static Community site published on GitHub Pages |
| `.github/workflows/pages.yml` | GitHub Actions validation and Pages deployment |

The Windows application is distributed through **[Releases](https://github.com/aleraco/tv-clean-manager/releases)**. This repository currently hosts the **Community infrastructure**; do not assume it contains the complete Windows application source code.

## Roadmap

- **v0.7 (current beta):** desktop app + public Community infrastructure.
- **v0.8 (planned):** guided launcher management, with checks and a documented recovery path.
- **v0.9 (planned):** broader device testing, safety review, accessibility and localization improvements.
- **v1.0 (goal):** public stable release after the required hardware and restoration tests.

Roadmap items are plans, not current capabilities.

## Safety and responsibility

- **Protected packages remain protected.** An unknown package is not automatically safe to disable.
- **Backups do not guarantee recovery.** If a modification prevents booting or breaks ADB, a saved report may be insufficient to restore the device.
- **Do not equate popularity with safety.** Two matching reports form a review candidate only.
- **Use at your own risk**, especially for modifications not validated on your exact model and firmware.
- **No automatic publication:** community sharing requires explicit review and submission.

## Links

- [TV Clean Manager Community](https://aleraco.github.io/tv-clean-manager/)
- [Windows releases](https://github.com/aleraco/tv-clean-manager/releases)
- [Issues and feedback](https://github.com/aleraco/tv-clean-manager/issues)
