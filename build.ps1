$env:PYTHONUTF8=1
.\.venv\Scripts\pyinstaller.exe --clean --noconsole --onefile --collect-all customtkinter --name "PhoneTrackerPro_GUI" gui.py
Copy-Item "dist\PhoneTrackerPro_GUI.exe" -Destination ".\PhoneTrackerPro_GUI.exe" -Force
Write-Host "Build complete! EXE updated at: $((Get-Item '.\PhoneTrackerPro_GUI.exe').FullName)"
