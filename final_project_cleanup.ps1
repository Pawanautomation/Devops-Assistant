$projectRoot = "C:\Users\pawan\Documents\Workspace\Devops-Assistant"

# 1. Clean up root directory scripts
$scriptsToRemove = @(
    "cleanup.ps1",
    "final_cleanup.ps1",
    "fix_init_files.ps1",
    "setup_project_structure.ps1",
    "show_structure.ps1"
)

foreach ($script in $scriptsToRemove) {
    $fullPath = Join-Path -Path $projectRoot -ChildPath $script
    if (Test-Path $fullPath) {
        Remove-Item $fullPath -Force
        Write-Host "Removed: $script"
    }
}

# 2. Create missing __init__.py files
$initLocations = @(
    "app",
    "app/api",
    "app/api/v1",
    "app/config",
    "app/models",
    "app/services",
    "app/utils",
    "tests",
    "tests/test_api",
    "tests/test_services"
)

foreach ($loc in $initLocations) {
    $initPath = Join-Path -Path $projectRoot -ChildPath "$loc/__init__.py"
    if (-not (Test-Path $initPath)) {
        New-Item -ItemType File -Path $initPath -Force
        Write-Host "Created: $loc/__init__.py"
    }
}

# 3. Move scripts to scripts directory
$scriptsToMove = @(
    "dir_structure.ps1",
    "project_cleanup.ps1"
)

if (-not (Test-Path "$projectRoot\scripts\powershell")) {
    New-Item -ItemType Directory -Path "$projectRoot\scripts\powershell" -Force
}

foreach ($script in $scriptsToMove) {
    $sourcePath = Join-Path -Path $projectRoot -ChildPath $script
    $destPath = Join-Path -Path "$projectRoot\scripts\powershell" -ChildPath $script
    if (Test-Path $sourcePath) {
        Move-Item $sourcePath $destPath -Force
        Write-Host "Moved: $script to scripts/powershell/"
    }
}

# 4. Ensure core files exist with basic content
$coreFiles = @{
    "app/config/settings.py" = @"
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DevOps Teaching Assistant"
    version: str = "0.1.0"
    debug: bool = False
    
    supabase_url: str
    supabase_key: str
    
    class Config:
        env_file = ".env"
"@

    "app/api/v1/__init__.py" = @"
from fastapi import APIRouter

router = APIRouter()

from .questions import *
from .responses import *
"@

    "app/main.py" = @"
from fastapi import FastAPI
from app.api.v1 import router as v1_router
from app.config.settings import Settings

settings = Settings()
app = FastAPI(title=settings.app_name, version=settings.version)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
"@
}

foreach ($file in $coreFiles.Keys) {
    $filePath = Join-Path -Path $projectRoot -ChildPath $file
    if (-not (Test-Path $filePath)) {
        Set-Content -Path $filePath -Value $coreFiles[$file]
        Write-Host "Created: $file"
    }
}

Write-Host "`nCleanup completed successfully!"
Write-Host "Run scripts/powershell/dir_structure.ps1 to verify the new structure."