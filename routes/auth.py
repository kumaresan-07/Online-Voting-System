from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import Admin, Voter, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('voter.vote'))
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('voter.vote'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        voter = Voter.query.filter_by(email=email).first()
        if voter and voter.check_password(password):
            login_user(voter)
            flash('Login successful!', 'success')
            return redirect(url_for('voter.vote'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('voter.vote'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        voter_id = request.form.get('voter_id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if Voter.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        if Voter.query.filter_by(voter_id=voter_id).first():
            flash('Voter ID already registered', 'error')
            return render_template('register.html')
        
        voter = Voter(
            first_name=first_name,
            last_name=last_name,
            email=email,
            voter_id=voter_id
        )
        voter.set_password(password)
        
        db.session.add(voter)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.index'))
