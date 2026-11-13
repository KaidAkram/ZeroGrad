$ErrorActionPreference = 'Stop'
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements-cpu.txt
& ./.venv/Scripts/python.exe -m pip install -e . --no-deps
Push-Location studio
try { npm.cmd ci } finally { Pop-Location }
