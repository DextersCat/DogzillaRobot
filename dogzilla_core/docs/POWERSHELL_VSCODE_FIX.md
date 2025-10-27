# PowerShell Detection Fix for VS Code
# Date: October 25, 2025

# This file contains solutions for VS Code PowerShell detection issues

## Problem: VS Code can't find PowerShell
"Unable to find PowerShell! Do you have it installed? You can also configure custom installations with the 'powershell.powerShellAdditionalExePaths' setting."

## Solutions:

### Solution 1: Check PowerShell Installation
# Run these commands in Command Prompt or existing PowerShell to verify installation:

# Check Windows PowerShell 5.1
powershell -Command "Get-Host"

# Check PowerShell 7+ (if installed)
pwsh -Command "Get-Host"

# Check installation paths
where powershell
where pwsh

### Solution 2: Configure VS Code Settings
# Add to VS Code settings.json:

{
    "powershell.powerShellAdditionalExePaths": [
        {
            "exePath": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "versionName": "Windows PowerShell 5.1"
        },
        {
            "exePath": "C:\\Program Files\\PowerShell\\7\\pwsh.exe", 
            "versionName": "PowerShell 7"
        }
    ],
    "powershell.powerShellDefaultVersion": "Windows PowerShell 5.1",
    "terminal.integrated.defaultProfile.windows": "PowerShell"
}

### Solution 3: Manual PowerShell Paths
# Common PowerShell installation locations:

# Windows PowerShell 5.1 (Always present on Windows 10+)
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

# PowerShell 7+ (Microsoft Store)
C:\Users\[USERNAME]\AppData\Local\Microsoft\WindowsApps\pwsh.exe

# PowerShell 7+ (MSI Install)
C:\Program Files\PowerShell\7\pwsh.exe

# PowerShell 7+ (GitHub Release)
C:\Program Files\PowerShell\[VERSION]\pwsh.exe

### Solution 4: VS Code Settings UI Method
1. Open VS Code
2. Press Ctrl+Comma (Settings)
3. Search: "powershell additional exe paths"
4. Click "Edit in settings.json"
5. Add the paths above

### Solution 5: Reload VS Code Extension
1. Press Ctrl+Shift+P
2. Type: "PowerShell: Restart Current Session"
3. Or: "Developer: Reload Window"

### Solution 6: Reinstall PowerShell Extension
1. Go to Extensions (Ctrl+Shift+X)
2. Search "PowerShell"
3. Uninstall Microsoft PowerShell extension
4. Reinstall it
5. Restart VS Code

### Solution 7: Environment Variables Check
# Verify PATH includes PowerShell:
echo $env:PATH

# Should include:
# C:\Windows\System32\WindowsPowerShell\v1.0\

### Solution 8: Run as Administrator
# If all else fails, run VS Code as administrator:
1. Right-click VS Code icon
2. "Run as administrator"
3. Try PowerShell again