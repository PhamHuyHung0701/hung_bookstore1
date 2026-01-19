@echo off
echo ================================================
echo Starting Microservices Bookstore
echo ================================================
echo.
echo Port 8001: Customer Service
echo Port 8002: Book Service
echo Port 8003: Cart Service
echo Port 8000: API Gateway (Web Interface)
echo.
echo ================================================

cd /d D:\hung_bookstore1\Microservices\services

echo Starting Customer Service on port 8001...
start "Customer Service - Port 8001" cmd /k "cd customer_service && python manage.py runserver 8001"

timeout /t 2 /nobreak > nul

echo Starting Book Service on port 8002...
start "Book Service - Port 8002" cmd /k "cd book_service && python manage.py runserver 8002"

timeout /t 2 /nobreak > nul

echo Starting Cart Service on port 8003...
start "Cart Service - Port 8003" cmd /k "cd cart_service && python manage.py runserver 8003"

timeout /t 2 /nobreak > nul

echo Starting API Gateway on port 8000...
start "API Gateway - Port 8000" cmd /k "cd api_gateway && python manage.py runserver 8000"

echo.
echo ================================================
echo All services started!
echo Open http://localhost:8000 in your browser
echo ================================================
pause
