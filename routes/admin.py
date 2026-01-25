from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import Admin, Voter, Position, Candidate, Vote, db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
@admin_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_voters': Voter.query.count(),
        'voted_count': Voter.query.filter_by(has_voted=True).count(),
        'total_positions': Position.query.count(),
        'total_candidates': Candidate.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/positions', methods=['GET', 'POST'])
@login_required
@admin_required
def positions():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name')
            description = request.form.get('description')
            
            if Position.query.filter_by(name=name).first():
                flash('Position already exists', 'error')
            else:
                try:
                    position = Position(name=name, description=description)
                    db.session.add(position)
                    db.session.commit()
                    db.session.expunge_all()
                    flash('Position added successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error adding position: {str(e)}', 'error')
        
        elif action == 'delete':
            position_id = request.form.get('position_id')
            try:
                position = Position.query.get(position_id)
                if position:
                    db.session.delete(position)
                    db.session.commit()
                    db.session.expunge_all()
                    flash('Position deleted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting position: {str(e)}', 'error')
        
        elif action == 'edit':
            position_id = request.form.get('position_id')
            try:
                position = Position.query.get(position_id)
                if position:
                    position.name = request.form.get('name')
                    position.description = request.form.get('description')
                    db.session.commit()
                    db.session.expunge_all()
                    flash('Position updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating position: {str(e)}', 'error')
    
    db.session.expire_all()
    positions = Position.query.all()
    return render_template('admin/positions.html', positions=positions)

@admin_bp.route('/candidates', methods=['GET', 'POST'])
@login_required
@admin_required
def candidates():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name')
            position_id = request.form.get('position_id')
            
            try:
                candidate = Candidate(name=name, position_id=position_id)
                db.session.add(candidate)
                db.session.commit()
                db.session.expunge_all()
                flash('Candidate added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding candidate: {str(e)}', 'error')
        
        elif action == 'delete':
            candidate_id = request.form.get('candidate_id')
            try:
                candidate = Candidate.query.get(candidate_id)
                if candidate:
                    db.session.delete(candidate)
                    db.session.commit()
                    db.session.expunge_all()
                    flash('Candidate deleted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting candidate: {str(e)}', 'error')
        
        elif action == 'edit':
            candidate_id = request.form.get('candidate_id')
            try:
                candidate = Candidate.query.get(candidate_id)
                if candidate:
                    candidate.name = request.form.get('name')
                    candidate.position_id = request.form.get('position_id')
                    db.session.commit()
                    db.session.expunge_all()
                    flash('Candidate updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating candidate: {str(e)}', 'error')
    
    db.session.expire_all()
    candidates = Candidate.query.all()
    positions = Position.query.all()
    return render_template('admin/candidates.html', candidates=candidates, positions=positions)

@admin_bp.route('/voters')
@login_required
@admin_required
def voters():
    voters = Voter.query.all()
    return render_template('admin/voters.html', voters=voters)

@admin_bp.route('/voters/delete/<int:voter_id>', methods=['POST'])
@login_required
@admin_required
def delete_voter(voter_id):
    voter = Voter.query.get_or_404(voter_id)
    Vote.query.filter_by(voter_id=voter_id).delete()
    db.session.delete(voter)
    db.session.commit()
    flash('Voter deleted successfully!', 'success')
    return redirect(url_for('admin.voters'))

@admin_bp.route('/results')
@login_required
@admin_required
def results():
    positions = Position.query.all()
    results_data = []
    
    for position in positions:
        candidates = Candidate.query.filter_by(position_id=position.id).order_by(Candidate.votes_count.desc()).all()
        results_data.append({
            'position': position,
            'candidates': candidates,
            'total_votes': sum(c.votes_count for c in candidates)
        })
    
    return render_template('admin/results.html', results_data=results_data)

@admin_bp.route('/results/data')
@login_required
@admin_required
def results_data():
    positions = Position.query.all()
    data = []
    
    for position in positions:
        candidates = Candidate.query.filter_by(position_id=position.id).all()
        data.append({
            'position': position.name,
            'candidates': [{'name': c.name, 'votes': c.votes_count} for c in candidates]
        })
    
    return jsonify(data)

@admin_bp.route('/admins', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_admins():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            
            if Admin.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
            else:
                try:
                    admin = Admin(first_name=first_name, last_name=last_name, email=email)
                    admin.set_password(password)
                    db.session.add(admin)
                    db.session.flush()  # Flush to database
                    db.session.commit()  # Commit transaction
                    flash('Admin added successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    print(f"Error adding admin: {str(e)}")
                    flash(f'Error: {str(e)}', 'error')
        
        elif action == 'delete':
            admin_id = request.form.get('admin_id')
            if int(admin_id) == current_user.id:
                flash('You cannot delete yourself!', 'error')
            else:
                try:
                    admin = Admin.query.get(admin_id)
                    if admin:
                        db.session.delete(admin)
                        db.session.flush()
                        db.session.commit()
                        flash('Admin deleted successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    print(f"Error deleting admin: {str(e)}")
                    flash(f'Error: {str(e)}', 'error')
    
    admins = Admin.query.all()
    return render_template('admin/manage_admins.html', admins=admins)

@admin_bp.route('/reset-votes', methods=['POST'])
@login_required
@admin_required
def reset_votes():
    Vote.query.delete()
    Candidate.query.update({Candidate.votes_count: 0})
    Voter.query.update({Voter.has_voted: False})
    db.session.commit()
    flash('All votes have been reset!', 'success')
    return redirect(url_for('admin.results'))
