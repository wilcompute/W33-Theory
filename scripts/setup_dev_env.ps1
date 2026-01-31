# PowerShell developer environment setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

Write-Host "Dev env ready. Run '.\\.venv\\Scripts\\Activate.ps1' to activate." -ForegroundColor Green
