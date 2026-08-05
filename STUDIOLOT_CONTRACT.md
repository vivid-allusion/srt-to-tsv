# STUDIOLOT_CONTRACT.md

> This repo is part of the studiolot ecosystem.
> Preserve the CLI contract below when modifying this script.

---

## What studiolot is

studiolot is a TUI that orchestrates AI media generation. It drives scripts
like this one by passing `--output_dir` (and optionally `--input_dir`). The
same script runs standalone (with its own `USER-FILES/` defaults) or under
studiolot (with paths injected by the TUI).

Full architecture: `studiolot/docs/architecture/PHILOSOPHY.md`

---

## Dual-mode contract

| Mode | How invoked | Input | Output | Profile |
|------|------------|-------|--------|---------|
| **Standalone** | `python run.py` from repo root | `USER-FILES/04.INPUT/` | `USER-FILES/05.OUTPUT/` | (none) |
| **Studiolot** | `python <entry> --output_dir X [--input_dir Y]` | `--input_dir` value (optional) | `--output_dir` value | (none) |

The script detects its mode by checking whether `--output_dir` was passed on
the command line.

---

## REQUIRED — Utility contract (pure Python logic, no API)

- [ ] Accepts `--output_dir` CLI flag (`--input_dir` optional)
- [ ] No network I/O, no API keys, no provider SDK imports
- [ ] Outputs to `--output_dir` (or `USER-FILES/05.OUTPUT/` in standalone)
- [ ] Do NOT hardcode folder paths (no `03_INPUT_SHOTLIST(STILL)`, etc.)
- [ ] Do NOT move or delete user files from input directories
- [ ] CLI flags take priority over standalone defaults

---

## Reference — studiolot repo

| Doc | What it covers |
|-----|---------------|
| `docs/architecture/PHILOSOPHY.md` | Why, folder model, bullet format, sidecar, copy-forward |
| `docs/architecture/DASH_CONTRACT.md` | TUI panel responsibilities, execution paths, keybindings |
| `docs/architecture/ENGINE_CONTRACT.md` | Engine interface, datatypes, repo structure, discovery |
| `docs/architecture/VEHICLE_CONTRACT.md` | Vehicle CLI contract, engine discovery, standalone UX |
| `pipeline/engine_loader.py` | Canonical `load_engine()` — vendored copies must match |
| `pipeline/constants.py` | Canonical folder names, action verbs, conventions |
| `console/studiolot/screens/project_init/tools_data.py` | `UTILITY_REPOS` + `APPLICATION_REGISTRY` — what's wired |

The studiolot repo is at:
`/home/admin/Nextcloud/00-DEVELOPMENT/MISC_DEV_TOOLS/studiolot/`

---

## Session History

<!-- Add entries here when changes are made. Same format as FC's AGENTS.md. -->
