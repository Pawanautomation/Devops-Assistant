function Show-DirectoryStructure {
    param (
        [string]$Path = ".",
        [int]$Level = 0
    )

    $indent = "|   " * $Level
    $items = Get-ChildItem -Path $Path -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch '(\.git|venv|__pycache__|node_modules|\.pytest_cache|\.vscode)' }

    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            Write-Host "$indent|-- $($item.Name)/"
            Show-DirectoryStructure -Path $item.FullName -Level ($Level + 1)
        }
        else {
            Write-Host "$indent|-- $($item.Name)"
        }
    }
}

Write-Host "DevOps-Assistant/"
Show-DirectoryStructure -Path "."