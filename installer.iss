; installer.iss
; Script de Inno Setup para "Conversor de Unidades"
;
; La versión NO está hardcodeada: se pasa como parámetro al compilar, ej:
;   ISCC.exe installer.iss /DMyAppVersion=1.0.0
;
; Esto permite que el mismo script sirva para cada release sin tocarlo,
; y que GitHub Actions (Paso 4) lo compile automáticamente con la
; versión correcta según el tag que se pusheó.

#ifndef MyAppVersion
  #define MyAppVersion "0.0.0-dev"
#endif

#define MyAppName "Conversor de Unidades"
#define MyAppPublisher "TuNombreOEmpresa"
#define MyAppExeName "Converter.exe"

; GUID único para esta app - generalo UNA VEZ en Inno Setup con:
; Tools > Generate GUID (te da algo como {A1B2C3D4-E5F6-...})
; Pegalo abajo TAL CUAL te lo da (con una sola llave de apertura y cierre)
; y NO lo cambies nunca en futuras versiones, o Windows va a tratar
; cada actualización como una app nueva en vez de un update.
#define MyAppId "{{CEDBA1E8-7B09-4967-877F-C4947ED0097C}}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; Nombre del instalador de salida: incluye la versión para identificarlo fácil
OutputBaseFilename=ConverterSetup-{#MyAppVersion}
OutputDir=installer_output
Compression=lzma
SolidCompression=yes
; Permite actualizar sobre una instalación previa sin pedir desinstalar antes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el Escritorio"; GroupDescription: "Accesos directos:"

[Files]
; Ajustá la ruta si tu .exe compilado está en otra carpeta
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar {#MyAppName}"; Flags: nowait postinstall skipifsilent
