# Run format script
Write-Output "Running code formatting..."
./scripts/format.ps1

# Add all changes to Git
Write-Output "Staging all changes..."
git add --all

# Check for an argument (commit message mode)
if ($args.Count -gt 0 -and $args[0] -eq "auto") {
    # Auto commit with timestamp
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Automatic push ($date)"
} else {
    # Ask user for commit message
    $commitMessage = Read-Host "Enter commit message"
}

# Commit changes
Write-Output "Committing with message: $commitMessage"
git commit -m "$commitMessage"

# Push to GitHub
Write-Output "Pushing to GitHub..."
git push origin main

Write-Output "✅ Push complete!"
