$projectRoot = "C:\Users\pawan\Documents\Workspace\Devops-Assistant"

# 1. Fix all **init**.py files
Get-ChildItem -Path $projectRoot -Recurse -File | 
    Where-Object { $_.Name -eq "**init**.py" -and $_.FullName -notlike "*\venv\*" } | 
    ForEach-Object {
        $directory = $_.DirectoryName
        $newPath = Join-Path -Path $directory -ChildPath "__init__.py"
        
        if (Test-Path $newPath) {
            Remove-Item $newPath -Force
        }
        
        try {
            Rename-Item -Path $_.FullName -NewName "__init__.py" -Force -ErrorAction Stop
            Write-Host "Fixed init file in: $directory"
        } catch {
            Write-Host "Error fixing init file in: $directory" -ForegroundColor Red
        }
    }

# 2. Move final cleanup script to scripts/powershell
if (Test-Path "$projectRoot\final_project_cleanup.ps1") {
    Move-Item "$projectRoot\final_project_cleanup.ps1" "$projectRoot\scripts\powershell\" -Force
    Write-Host "Moved final_project_cleanup.ps1 to scripts/powershell/"
}

# 3. Create proper __init__.py files where missing
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

Write-Host "`nFinal cleanup completed successfully!"
Write-Host "Run scripts/powershell/dir_structure.ps1 to verify the structure."