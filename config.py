import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Database Mode: 'mysql' or 'sqlite' (use sqlite for testing/deployment without MySQL)
    DB_MODE = os.environ.get('DB_MODE', 'sqlite')
    
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'online_voting')
    
    # SQLAlchemy Database URI
    if DB_MODE == 'mysql':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///voting.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
