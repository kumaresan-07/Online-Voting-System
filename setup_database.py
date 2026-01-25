"""
Database Setup Script for Online Voting System
This script creates the MySQL database and initializes the tables.
"""

import pymysql
from config import Config

def create_database():
    """Create the MySQL database if it doesn't exist."""
    connection = None
    try:
        # Connect to MySQL server (without specifying database)
        # Force empty password for XAMPP localhost
        password = Config.MYSQL_PASSWORD if Config.MYSQL_PASSWORD else ''
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=password,
            port=int(Config.MYSQL_PORT),
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{Config.MYSQL_DB}' created or already exists.")
            
        connection.commit()
        
    except pymysql.Error as e:
        print(f"✗ Error creating database: {e}")
        raise
    finally:
        if connection:
            connection.close()

def init_app_tables():
    """Initialize application tables using Flask-SQLAlchemy."""
    from app import create_app
    from models import db, Admin, Voter, Position, Candidate, Vote
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully.")
        
        # Check if default admin exists
        admin = Admin.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin = Admin(
                first_name='Admin',
                last_name='User',
                email='admin@gmail.com'
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin user created (email: admin@gmail.com, password: admin)")
        else:
            print("✓ Default admin user already exists.")
        
        # Check if default positions exist
        if not Position.query.first():
            positions = [
                Position(name='Chairman', description='Head of the organization'),
                Position(name='Vice-Chairman', description='Deputy head of the organization'),
                Position(name='Secretary', description='Administrative head'),
                Position(name='Treasurer', description='Financial head'),
            ]
            db.session.add_all(positions)
            db.session.commit()
            print("✓ Default positions created.")
        else:
            print("✓ Positions already exist.")
        
        print("\n" + "="*50)
        print("Database setup completed successfully!")
        print("="*50)
        print("\nYou can now run the application with: python app.py")
        print("\nDefault Admin Credentials:")
        print("  Email: admin@gmail.com")
        print("  Password: admin")
        print("\nAccess the application at: http://localhost:5000")
        print("Admin panel at: http://localhost:5000/admin/login")

if __name__ == '__main__':
    print("="*50)
    print("Online Voting System - Database Setup")
    print("="*50)
    print()
    
    # Step 1: Create the database
    print("Step 1: Creating MySQL database...")
    create_database()
    print()
    
    # Step 2: Initialize tables
    print("Step 2: Initializing database tables...")
    init_app_tables()
