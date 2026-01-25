@echo off
echo ================================================
echo Online Voting System - XAMPP Local Setup
echo ================================================
echo.
echo Make sure XAMPP MySQL is running!
echo.
echo Default MySQL Settings:
echo   Host: localhost
echo   User: root
echo   Password: root123
echo   Database: online_voting
echo   Port: 3307
echo.
echo ================================================

REM Set environment variables for XAMPP MySQL
set MYSQL_HOST=localhost
set MYSQL_USER=root
set MYSQL_PASSWORD=root123
set MYSQL_DB=online_voting
set MYSQL_PORT=3307

REM Setup database and run the app
echo.
echo Setting up database...
python setup_database.py

echo.
echo Starting the application...
python app.py

pause
