# Portable runtime (MacBook / Windows / Linux)

Use Python 3.10+ on the host that actually executes the skill. A repository/Multica import does not transfer another computer's Python, virtual environment, SF installation, licence, endpoint or credentials. Never copy a Windows venv onto a Mac.

From the repository/installed skill root:

```bash
# MacBook / Linux
python3 scripts/setup_runtime.py --venv .venv
.venv/bin/python scripts/setup_runtime.py --venv .venv --check-only
.venv/bin/python scripts/onsite_checklist.py --config runs/current/config.json --run-dir .
```

The final command requires a current shared run/config.json and usable exports. Relative paths inside JSON resolve from that JSON's directory, so exports alongside it use source.export_directory="exports", not "runs/current/exports". CLI --run-dir follows the same convention: --run-dir . selects the config directory; this example writes to runs/current/content/. The coordinator can instead pass its resolved run path.

Optional environment-based JSON selection, using a current local JSON (not a GitHub URL or SF profile):

```bash
export ONSITE_AUDIT_CONFIG="runs/current/config.json"
.venv/bin/python scripts/onsite_checklist.py --run-dir .
```

Avoid carrying stale site configuration between audits. Explicit --config wins. If the installed skill directory is read-only, choose a writable venv path with --venv and call the interpreter reported by setup; do not attempt global dependency installation or overwrite the skill installation.

Windows equivalent:

```powershell
py -3 scripts/setup_runtime.py --venv .venv
.\.venv\Scripts\python.exe scripts/setup_runtime.py --venv .venv --check-only
.\.venv\Scripts\python.exe scripts/onsite_checklist.py --config runs/current/config.json --run-dir .
```

The setup helper resolves requirements.txt relative to its own installed location, selects bin/python on Mac/Linux or Scripts/python.exe on Windows, and invokes that interpreter for pip and verification. The --venv path is relative to the current working directory. Only an existing valid venv is reused; unrelated directories are rejected without deletion. No shell activation, fixed /Users path, executable path, SF launcher, port or Downloads assumption is required. Reuse verified setup rather than reinstall on every audit. --check-only never creates a venv or runs pip.

Failure cases: missing Python 3.10+/venv/pip, package download/network failure, unusable existing venv or inaccessible directory must be corrected on the actual host. Setup exits nonzero and does not claim readiness. Environment setup may download packages; the CSV audit does not contact websites. No system Python install/upgrade, configuration installation or crawl is performed by this helper.

For Multica, make both onsite-audit-content and sf-shared-config available to the executing agent, install this runtime there, and provide that host's accessible crawl/export paths. Follow the shared skill's host-aware profile delivery and manual Start contract. Changing local Python does not establish SF MCP connectivity. Paths/endpoints are user/runtime inputs and must not be committed as machine constants.
