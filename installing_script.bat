@echo off

rem Check if Python 3.11 is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
) else (
    echo Installing Python 3.11 from the Microsoft Store...
    start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    echo Please install Python 3.11 from the Microsoft Store.
    pause
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Python is succesfully installed.
    ) else (
        echo Python is not installed. Try again.
        pause
	exit
    )
)

echo Installing pyttsx3...
pip install pyttsx3
echo pyttsx3 installed.

echo Installing pyperclip...
pip install pyperclip
echo pyperclip installed.

echo All dependencies installed.
pause