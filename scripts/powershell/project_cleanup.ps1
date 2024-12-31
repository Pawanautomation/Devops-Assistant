$projectRoot = "C:\Users\pawan\Documents\Workspace\Devops-Assistant"

# 1. Create directories array for project structure
$directories = @(
    "app/api/v1",
    "app/config",
    "app/models",
    "app/services",
    "app/utils",
    "environments",
    "infrastructure/docker",
    "infrastructure/vector",
    "migrations",
    "scripts",
    "tests/test_api",
    "tests/test_services"
)

# 2. Create directories
foreach ($dir in $directories) {
    $fullPath = Join-Path -Path $projectRoot -ChildPath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force
        Write-Host "Created directory: $dir"
    }
}

# 3. Fix **init**.py files (only in project directories, excluding venv)
Get-ChildItem -Path $projectRoot -Recurse -Filter "**init**.py" | 
    Where-Object { $_.FullName -notlike "*\venv\*" } | 
    ForEach-Object {
        $directory = $_.DirectoryName
        $newPath = Join-Path -Path $directory -ChildPath "__init__.py"
        
        if (Test-Path $newPath) {
            Remove-Item $newPath -Force
        }
        
        Rename-Item -Path $_.FullName -NewName "__init__.py" -Force
        Write-Host "Fixed init file in: $directory"
    }

# 4. Move environment files
if ((Test-Path "$projectRoot\.env") -or (Test-Path "$projectRoot\Production .env")) {
    # Move environment files
    if (Test-Path "$projectRoot\.env") {
        Move-Item "$projectRoot\.env" "$projectRoot\environments\development.env" -Force
        Write-Host "Moved .env to environments/development.env"
    }
    if (Test-Path "$projectRoot\Production .env") {
        Move-Item "$projectRoot\Production .env" "$projectRoot\environments\production.env" -Force
        Write-Host "Moved Production .env to environments/production.env"
    }
    
    # Create symlink for default environment
    Copy-Item "$projectRoot\environments\development.env" "$projectRoot\.env" -Force
    Write-Host "Created .env symlink"
}

# 5. Clean up redundant files and folders
$redundantItems = @(
    "app/main.py.backup",
    "backups",
    "app/supabase",
    "app/api/routes"
)

foreach ($item in $redundantItems) {
    $fullPath = Join-Path -Path $projectRoot -ChildPath $item
    if (Test-Path $fullPath) {
        Remove-Item $fullPath -Recurse -Force
        Write-Host "Removed redundant item: $item"
    }
}

Write-Host "`nCleanup completed! Run dir_structure.ps1 to verify the new structure."