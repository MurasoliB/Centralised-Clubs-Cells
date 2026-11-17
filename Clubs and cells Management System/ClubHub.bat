@echo off
setlocal EnableDelayedExpansion
title ClubHub - KEC
color 0B
chcp 65001 >nul

set "PROJ_DIR=%~dp0"

if exist "%~dp0package.json" (
    set "PROJ_DIR=%~dp0"
)

if exist "%~dp0Clubs and cells Management System\package.json" (
    set "PROJ_DIR=%~dp0Clubs and cells Management System"
) else if exist "%~dp0package.json" (
    set "PROJ_DIR=%~dp0"
)

cd /d "!PROJ_DIR!"

if "%~1"=="1" goto run_web
if "%~1"=="2" goto run_cli
if "%~1"=="3" exit /b 0

:menu
cls
echo ===============================================================================
echo.
echo     ###  #    #  # ###   #  # #  # ###  
echo    #   # #    #  # #  #  #  # #  # #  # 
echo    #     #    #  # ###   #### #  # ###  
echo    #   # #    #  # #  #  #  # #  # #  # 
echo     ###  ####  ##  ###   #  #  ##  ###  
echo.
echo   KONGU ENGINEERING COLLEGE (AUTONOMOUS) - IT DEPARTMENT
echo   CENTRALIZED CLUBS AND CELLS MANAGEMENT SYSTEM (2026-2027)
echo.
echo ===============================================================================
echo.
echo Select how you want to run ClubHub:
echo.
echo  [1] Launch Web Portal (http://localhost:5173/) [Default]
echo  [2] Command Prompt Console (Terminal CLI)
echo  [3] Exit
echo.
set /p opt="Enter option (1-3) [default: 1]: "

if "%opt%"=="2" goto run_cli
if "%opt%"=="3" exit /b 0
goto run_web

:run_cli
echo.
node scripts/console-menu.cjs
echo.
pause
goto menu

:run_web
echo.
echo ===============================================================================
echo   Starting Vite Dev Server at http://localhost:5173/ ...
echo ===============================================================================
echo.
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5173/"
npm run dev
pause
exit /b 0
