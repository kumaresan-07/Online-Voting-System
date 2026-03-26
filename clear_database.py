#!/usr/bin/env python3
"""
Script to clear all data from the Online Voting System database
while keeping the table structure intact.
"""

from app import create_app, db
from models import Vote, Candidate, Position, Voter, Admin

def clear_database():
    """Delete all data from database tables"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Starting database cleanup...")
            
            # Delete in order of foreign key dependencies
            print("Deleting votes...")
            Vote.query.delete()
            
            print("Deleting candidates...")
            Candidate.query.delete()
            
            print("Deleting positions...")
            Position.query.delete()
            
            print("Deleting voters...")
            Voter.query.delete()
            
            print("Deleting admins...")
            Admin.query.delete()
            
            # Commit all deletions
            db.session.commit()
            
            print("\n✅ All data has been deleted successfully!")
            print("Table structures are preserved.")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error clearing database: {str(e)}")
            print("Make sure MySQL is running and connected.")
            return False
    
    return True

if __name__ == '__main__':
    clear_database()
