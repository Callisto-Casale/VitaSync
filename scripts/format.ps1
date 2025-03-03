# This format.ps1 file acts like a simple way of applying style-related rules
# This script will be ran when running ./push,ps1
# The script can also be ran by hand by doing ./format.ps1


# Isort automatically sorts and organizes all import statements in this project.
# it keeps the imports consistent, organized, and avoids duplicate or unordered imports
isort . *> $null


# Automatically formats Python code to follow the PEP 8 style guide.
# Ensures consistent code formatting, so you don’t have to worry about spacing, line breaks, or indentation.
black . *> $null


#  Checks Python code for errors, unused variables, and bad practices (linting).
#  Helps catch syntax errors, missing imports, bad indentation, and unused variables.
flake8 . --ignore E501 > $null
