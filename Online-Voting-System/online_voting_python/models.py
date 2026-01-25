from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create db instance here to avoid circular imports
db = SQLAlchemy()

def init_login_manager(login_manager):
    """Initialize the login manager user loader."""
    @login_manager.user_loader
    def load_user(user_id):
        # Check if it's an admin or voter
        user_type, id = user_id.split('_')
        if user_type == 'admin':
            return Admin.query.get(int(id))
        return Voter.query.get(int(id))

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f'admin_{self.id}'
    
    @property
    def is_admin(self):
        return True

class Voter(UserMixin, db.Model):
    __tablename__ = 'voters'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    voter_id = db.Column(db.String(45), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    votes = db.relationship('Vote', backref='voter', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f'voter_{self.id}'
    
    @property
    def is_admin(self):
        return False

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.String(255))
    max_votes = db.Column(db.Integer, default=1)
    
    candidates = db.relationship('Candidate', backref='position', lazy=True)

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    votes_count = db.Column(db.Integer, default=0)
    photo = db.Column(db.String(255))
    
    votes = db.relationship('Vote', backref='candidate', lazy=True)

class Vote(db.Model):
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('voter_id', 'position_id', name='unique_vote_per_position'),
    )
