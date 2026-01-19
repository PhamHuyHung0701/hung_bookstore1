@echo off
echo Stopping all microservices...
taskkill /FI "WINDOWTITLE eq Customer Service*" /F
taskkill /FI "WINDOWTITLE eq Book Service*" /F
taskkill /FI "WINDOWTITLE eq Cart Service*" /F
taskkill /FI "WINDOWTITLE eq API Gateway*" /F
echo All services stopped.
pause
