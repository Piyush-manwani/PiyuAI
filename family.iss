; --- Inno Setup Script for PiyuAI ---

[Setup]
; Basic App Information
AppName=PiyuAI
AppVersion=1.0
AppPublisher=Piyush - Indus Ir
DefaultDirName={autopf}\PiyuAI
DefaultGroupName=PiyuAI

; Installer Settings
; This saves the final setup.exe to your Documents\Output folder
OutputDir=userdocs:Output
OutputBaseFilename=PiyuAI_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
; The source file path from your screenshot
Source: "C:\Users\Piyush - Indus Ir\Downloads\PiyuAI-main\PiyuAI-main\dist\piyuai.exe"; DestDir: "{app}"; Flags: ignoreversion
; Note: If your app needs other files from the 'dist' folder, add them here.

[Icons]
; Creates a Start Menu shortcut
Name: "{group}\PiyuAI"; Filename: "{app}\piyuai.exe"
; Creates a Desktop shortcut
Name: "{autodesktop}\PiyuAI"; Filename: "{app}\piyuai.exe"

[Run]
; Option to launch the app immediately after installation finishes
Filename: "{app}\piyuai.exe"; Description: "{cm:LaunchProgram,PiyuAI}"; Flags: nowait postinstall skipifsilent
