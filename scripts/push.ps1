./scripts/format.ps1

git add --all

# Check for arguments
$reloadFlag = $false
$autoCommit = $false

foreach ($arg in $args) {
    if ($arg -eq "--auto") {
        $autoCommit = $true
    }
    if ($arg -eq "--reload") {
        $reloadFlag = $true
    }
}

# Set commit message
if ($autoCommit) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Automatic push ($date)"
} else {
    $commitMessage = Read-Host "Enter commit message"
}

git commit -m "$commitMessage"

# Get current branch and push
$branch = git branch --show-current
git push origin $branch

# Run RELOAD_PROJECT.ps1 if --reload was passed
if ($reloadFlag) {
    Write-Host "Reloading project..."
    ./RELOAD_PROJECT.ps1
}
