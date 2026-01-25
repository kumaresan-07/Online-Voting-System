from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, init_login_manager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Ensure database commits are properly handled
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            db.session.rollback()
        else:
            try:
                db.session.commit()
            except:
                db.session.rollback()
        db.session.remove()
    
    # Initialize the user loader
    init_login_manager(login_manager)
    
    with app.app_context():
        # Import models after db is initialized
        from models import Admin, Voter, Position, Candidate, Vote
        
        # Register blueprints
        from routes.auth import auth_bp
        from routes.voter import voter_bp
        from routes.admin import admin_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(voter_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        # Create tables
        try:
            db.create_all()
        except Exception as e:
            print(f"Warning: Could not create database tables: {e}")
            print("Make sure MySQL is running and credentials are correct.")
        
        # Create default admin if not exists
        try:
            if not Admin.query.filter_by(email='admin@gmail.com').first():
                admin = Admin(
                    first_name='Admin',
                    last_name='User',
                    email='admin@gmail.com'
                )
                admin.set_password('admin')
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            print(f"Warning: Could not create default admin: {e}")
        
        # Create default positions if not exist
        try:
            if not Position.query.first():
                positions = [
                    Position(name='Chairman', description='Head of the organization'),
                    Position(name='Vice-Chairman', description='Deputy head'),
                    Position(name='Secretary', description='Administrative head'),
                ]
                db.session.add_all(positions)
                db.session.commit()
        except Exception as e:
            print(f"Warning: Could not create default positions: {e}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=5000, use_reloader=False)
