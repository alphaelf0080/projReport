@echo off
title Game Dump Tool Architecture Documentation Server
echo Starting Game Dump Tool Architecture Documentation Server...
echo.
echo Server will be available at:
echo - Local: http://localhost:3000
echo - Network: http://[your-ip]:3000
echo.
echo Press Ctrl+C to stop the server
echo.

npx http-server -p 3000 -a 0.0.0.0 -c-1

pause