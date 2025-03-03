./scripts/format.ps1

git add --all

if ($args.Count -gt 0 -and $args[0] -eq "auto") {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Automatic push ($date)"
} else {
    $commitMessage = Read-Host "Enter commit message"
}

git commit -m "$commitMessage"

git push origin main

