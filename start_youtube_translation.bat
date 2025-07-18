@echo off
echo ========================================
echo 🇮🇷 YouTube Farsi Translation System
echo ========================================
echo.
echo Starting Flask web interface at http://localhost:5000
echo.
echo IMPORTANT: Make sure you've configured audio routing:
echo 1. Enable Stereo Mix in Windows Sound settings
echo 2. Route Stereo Mix to CABLE Input
echo.
echo Opening web interface in 3 seconds...
timeout /t 3 /nobreak >nul
echo.
echo Starting Flask translation system...
python flask_web_interface.py
echo.
echo If the web interface doesn't open automatically,
echo navigate to: http://localhost:5000
echo.
pause 