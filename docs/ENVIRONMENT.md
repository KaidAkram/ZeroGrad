# Audited environment

Updated 2026-11-13T19:49:54.123963+00:00. Initial workspace contained only the master brief; it was not a Git repository. No existing source was overwritten or Git history reinitialized. Source revision is therefore `unversioned`; a release commit must be created by the owner.

- OS: Windows, PowerShell; Python 3.13.13.
- Node 24.14.1; npm.cmd used because npm.ps1 is blocked by PowerShell execution policy. No execution-policy changes made.
- CPU: 20 logical processors; approximately 15.7 GiB system RAM and 55.8 GiB free disk at initial audit. CUDA reported available, but all science uses CPU with two PyTorch threads; no GPU benchmark claim.
- FFmpeg/ffprobe 8.1.2 available; system Arial font rendered but not redistributed.
- Python versions: {"numpy": "2.4.6", "torch": "2.6.0+cu124", "scipy": "1.18.0", "scikit-learn": "1.8.0", "matplotlib": "3.11.0", "pydantic": "2.13.2", "Pillow": "12.2.0", "pytest": "9.1.1", "psutil": "7.2.2"}.
- `.venv` created with system-site-packages for the available trusted scientific stack. No global package changes. A clean environment install remains unverified because shell network sockets are blocked (WinError 10013 / EACCES).
- Official references could be read through the web tool. Shell GitHub/npm requests failed; no privileged retry.
- React/TypeScript/Vite dependencies were recovered from the existing read-only npm cache. studio/package-lock.json contains pinned integrity hashes. Production build succeeds locally.
- Installed Microsoft Edge/Playwright enabled local browser QA. No external hosting, account access, publishing or messaging performed.
- Skills applied: installed skill-installer, skill-creator, openai-docs and Sites instructions. Remotion installation blocked; original Pillow/FFmpeg fallback used.

Machine names, account secrets and unique hardware identifiers are intentionally excluded.
