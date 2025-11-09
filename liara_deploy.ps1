# PowerShell deployment script for Chidmano on Liara (Windows)
# This script helps with deployment tasks on Windows

Write-Host "🚀 Starting Chidmano deployment process..." -ForegroundColor Green

# Check if liara CLI is installed
try {
    $null = Get-Command liara -ErrorAction Stop
} catch {
    Write-Host "❌ Liara CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "npm install -g @liara/cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Liara
try {
    $null = liara account:current 2>&1
} catch {
    Write-Host "⚠️  Not logged in to Liara. Please login first:" -ForegroundColor Yellow
    Write-Host "liara login" -ForegroundColor Yellow
    exit 1
}

# Run migrations before deployment (optional, main.py will handle it)
Write-Host "📊 Running migrations..." -ForegroundColor Green
try {
    python manage.py migrate --noinput
} catch {
    Write-Host "⚠️  Migration warning (continuing anyway)" -ForegroundColor Yellow
}

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Green
try {
    python manage.py collectstatic --noinput
} catch {
    Write-Host "⚠️  Collectstatic warning (continuing anyway)" -ForegroundColor Yellow
}

# Deploy to Liara
Write-Host "🚀 Deploying to Liara..." -ForegroundColor Green
liara deploy

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green

