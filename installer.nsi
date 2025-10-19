; HRMS Application Installer Script
; This script creates a Windows installer for the HRMS application

!define APPNAME "HRMS Application"
!define COMPANYNAME "HRMS Company"
!define DESCRIPTION "Human Resource Management System"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/harrington40/hr-management-system"
!define UPDATEURL "https://github.com/harrington40/hr-management-system/releases"
!define ABOUTURL "https://github.com/harrington40/hr-management-system"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\${APPNAME}"
Name "${APPNAME}"
outFile "${APPNAME}_installer.exe"

!include LogicLib.nsh
!include nsDialogs.nsh
!include WinMessages.nsh

page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    # Files for the install directory - to build the installer, these should be in the same directory as the install script (this file)
    setOutPath $INSTDIR

    # Copy all application files
    file /r "dist\HRMS_Application.exe"
    file "assets"
    file "config"
    file "database"
    file "README.md"
    file "SECURITY_GUIDE.md"

    # Create desktop shortcut
    createShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\HRMS_Application.exe" "" "$INSTDIR\HRMS_Application.exe"

    # Create start menu entries
    createDirectory "$SMPROGRAMS\${APPNAME}"
    createShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\HRMS_Application.exe" "" "$INSTDIR\HRMS_Application.exe"
    createShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe"

    # Registry information for add/remove programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\HRMS_Application.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}

    # Create uninstaller
    writeUninstaller "$INSTDIR\uninstall.exe"

    # Check if PostgreSQL is installed, if not, prompt user
    nsExec::ExecToLog '"$SYSDIR\sc.exe" query PostgreSQL'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_YESNO "PostgreSQL database server is not detected. Would you like to install it?" IDYES install_postgres IDNO skip_postgres
        install_postgres:
            ExecWait '"$INSTDIR\database\install_postgres.bat"'
        skip_postgres:
    ${EndIf}

sectionEnd

section "uninstall"
    # Stop the application if running
    nsExec::ExecToLog '"$SYSDIR\taskkill.exe" /F /IM HRMS_Application.exe'

    # Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

    # Remove files
    delete "$INSTDIR\HRMS_Application.exe"
    delete "$INSTDIR\uninstall.exe"
    rmDir /r "$INSTDIR\assets"
    rmDir /r "$INSTDIR\config"
    rmDir /r "$INSTDIR\database"
    delete "$INSTDIR\README.md"
    delete "$INSTDIR\SECURITY_GUIDE.md"

    # Remove shortcuts
    delete "$DESKTOP\${APPNAME}.lnk"
    rmDir /r "$SMPROGRAMS\${APPNAME}"

    # Remove directories
    rmDir "$INSTDIR"
sectionEnd