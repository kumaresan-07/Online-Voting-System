import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Database Mode: 'mysql' for XAMPP local MySQL
    DB_MODE = 'mysql'
    
    # XAMPP MySQL Database Configuration
    # Default XAMPP settings: host=localhost, user=root, password='root123'
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root123')  # XAMPP default is empty password
    MYSQL_DB = os.environ.get('MYSQL_DB', 'online_voting')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3307')  # XAMPP default port
    
    # SQLAlchemy Database URI for XAMPP MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
