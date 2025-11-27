# PowerShell script to install all dependencies
# Run this script to ensure all required packages are installed

Write-Host "🔄 Installing Python dependencies..." -ForegroundColor Cyan

# Activate virtual environment if exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    . .venv\Scripts\Activate.ps1
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    . venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️ No virtual environment found. Installing to global Python..." -ForegroundColor Yellow
}

# Install from requirements.txt
Write-Host "📦 Installing packages from requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All dependencies installed successfully!" -ForegroundColor Green
    
    # Verify critical packages
    Write-Host "🔍 Verifying critical packages..." -ForegroundColor Cyan
    $packages = @("numpy", "pandas", "django", "psycopg2-binary")
    foreach ($pkg in $packages) {
        $result = pip show $pkg 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $pkg is installed" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $pkg is NOT installed" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green

