# TV Clean Manager · Community repository (v0.7 starter)

This repository is a **starter**, not an already published service. To activate the site:

1. Create a **public** GitHub repository `aleraco/tv-clean-manager` (or change URLs in installer.ps1 and site/index.html).
2. Upload the entire contents of this folder to `main`.
3. Under **Settings → Pages**, select **GitHub Actions** as the source. Run `Validate reports and publish Community` from Actions.
4. The resulting URL will be `https://aleraco.github.io/tv-clean-manager/` if the suggested repository name and account are used.

### Report contribution

A contributor exports a schema-3 JSON report after reviewing its package list and private information, then creates a pull request adding it to `reports/`. Maintainers must verify the contributor's GitHub account, model, firmware, duplicate IDs, accuracy of the claimed actions, and evidence. An open PR is not a published record. Direct submission without a GitHub account is not supported in this first prototype.

**Identity**: `nickname` is a self-declared label. Counts of distinct nicknames are not proof of two independent people. Moderators should cross-check the contributor GitHub accounts before marking a combination as community corroborated. The provided builder deliberately sets `identity_and_independence_verified` to `false`. No automatic write authorization can be derived from it.

**Evidence**: `reboot_attested` and `restore_attested` remain self-reported. A TV working after reboot does not demonstrate successful restoration. No action is automatically marked safe.

**Privacy**: reports may reveal installed apps. Prefer sharing only relevant experiences and a minimized device profile. This prototype accepts complete schema-3 JSONs, so maintainers must review submissions carefully. Avoid uploading IP addresses, serial numbers, fingerprint strings, backup paths, tokens, or raw logs.

### Files

- `reports/`: human-reviewed schema-3 JSON documents. Empty initially.
- `scripts/build_catalog.py`: validates reports, deduplicates experience IDs and produces the index.
- `site/index.html`: responsive static public browser.
- `site/catalog/index.json`: generated public index.
- `.github/workflows/pages.yml`: CI validation and static site publishing.

App-generated completed actions can be included when a public nickname is explicitly entered in the export dialog; they remain distinct from ADB manual testimonies and do not satisfy the two-ADB threshold. An action listed in the app journal is not proof of successful reboot or successful restoration.

This is **not** a reversible-firmware-backup solution. The desktop app keeps its exact allowlist and safety protection unchanged.
