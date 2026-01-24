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
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.filter_by(email='admin@gmail.com').first():
            admin = Admin(
                first_name='Admin',
                last_name='User',
                email='admin@gmail.com'
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
        
        # Create default positions if not exist
        if not Position.query.first():
            positions = [
                Position(name='Chairman', description='Head of the organization'),
                Position(name='Vice-Chairman', description='Deputy head'),
                Position(name='Secretary', description='Administrative head'),
            ]
            db.session.add_all(positions)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
