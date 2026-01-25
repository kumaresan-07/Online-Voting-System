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
echo   Password: (empty)
echo   Database: online_voting
echo   Port: 3306
echo.
echo ================================================

REM Set environment variables for XAMPP MySQL
set MYSQL_HOST=localhost
set MYSQL_USER=root
set MYSQL_PASSWORD=
set MYSQL_DB=online_voting
set MYSQL_PORT=3306

REM Setup database and run the app
echo.
echo Setting up database...
python setup_database.py

echo.
echo Starting the application...
python app.py

pause
