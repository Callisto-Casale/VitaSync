./scripts/format.ps1

git add --all

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

if ($autoCommit) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Automatic push ($date)"
} else {
    $commitMessage = Read-Host "Enter commit message"
}

git commit -m "$commitMessage"

$branch = git branch --show-current
git push origin $branch

if ($reloadFlag) {
    Write-Host "Reloading project..."
    ./scripts/RELOAD_PROJECT.ps1
}
