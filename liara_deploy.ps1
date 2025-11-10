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

# Deploy to Liara with retry mechanism
Write-Host "🚀 Deploying to Liara..." -ForegroundColor Green
$maxRetries = 3
$retryCount = 0
$deployed = $false

while ($retryCount -lt $maxRetries -and -not $deployed) {
    try {
        $retryCount++
        Write-Host "Attempt $retryCount of $maxRetries..." -ForegroundColor Yellow
        
        # Deploy with timeout and better error handling
        $result = liara deploy --app chidmano 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
            $deployed = $true
        } else {
            Write-Host "⚠️  Deployment attempt $retryCount failed" -ForegroundColor Yellow
            Write-Host $result -ForegroundColor Red
            
            if ($retryCount -lt $maxRetries) {
                $waitTime = $retryCount * 10
                Write-Host "Waiting $waitTime seconds before retry..." -ForegroundColor Yellow
                Start-Sleep -Seconds $waitTime
            }
        }
    } catch {
        Write-Host "❌ Error during deployment: $_" -ForegroundColor Red
        if ($retryCount -lt $maxRetries) {
            $waitTime = $retryCount * 10
            Write-Host "Waiting $waitTime seconds before retry..." -ForegroundColor Yellow
            Start-Sleep -Seconds $waitTime
        }
    }
}

if (-not $deployed) {
    Write-Host "❌ Deployment failed after $maxRetries attempts" -ForegroundColor Red
    Write-Host "💡 Suggestions:" -ForegroundColor Yellow
    Write-Host "   1. Check your internet connection" -ForegroundColor Yellow
    Write-Host "   2. Try: liara deploy --app chidmano --debug" -ForegroundColor Yellow
    Write-Host "   3. Check Liara dashboard for server status" -ForegroundColor Yellow
    exit 1
}

