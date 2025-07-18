@echo off
echo ========================================
echo 🎥 OBS Studio Quick Setup for Subtitles
echo ========================================
echo.
echo This will guide you through setting up OBS Studio
echo for real-time Farsi subtitle display.
echo.
echo PREREQUISITES:
echo 1. Flask interface should be running at http://localhost:5000
echo 2. VB-Cable audio routing should be configured
echo 3. Translation system should be working
echo.
pause
echo.
echo STEP 1: Installing OBS Studio (if needed)
echo ========================================
echo If OBS Studio is not installed, run:
echo    winget install OBSProject.OBSStudio
echo.
echo Press any key when OBS Studio is installed...
pause
echo.
echo STEP 2: Loading the Translation Script
echo =====================================
echo 1. Open OBS Studio
echo 2. Go to Tools → Scripts
echo 3. Click the + button
echo 4. Navigate to this folder: %CD%
echo 5. Select: obs_integration.py
echo 6. Click Open
echo.
pause
echo.
echo STEP 3: Configure the Script
echo ===========================
echo In the script properties panel, set:
echo - Subtitle File: subtitle.txt
echo - Scene Name: Scene
echo - Font Size: 48
echo - Position Y: 80
echo.
echo Then click "Setup Scene" and "Test Subtitle"
echo.
pause
echo.
echo STEP 4: Add Browser Source
echo =========================
echo 1. In Sources panel, click +
echo 2. Select: Browser
echo 3. Name: YouTube_Video
echo 4. URL: https://www.youtube.com
echo 5. Width: 1920, Height: 1080
echo 6. Click OK
echo.
pause
echo.
echo STEP 5: Test Everything
echo ======================
echo 1. Start Flask interface: http://localhost:5000
echo 2. Click "Start Translation"
echo 3. In OBS browser source, play a YouTube video
echo 4. Watch for Farsi subtitles to appear
echo.
echo SUCCESS INDICATORS:
echo ✅ YouTube video plays in OBS
echo ✅ Farsi subtitles appear at bottom
echo ✅ Subtitles update every 3-5 seconds
echo.
echo If you need help, check: OBS_SETUP_COMPLETE.md
echo.
pause 