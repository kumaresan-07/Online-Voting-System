from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Position, Candidate, Vote, Voter, db
from functools import wraps

voter_bp = Blueprint('voter', __name__)

def voter_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin:
            flash('Please login as a voter to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@voter_bp.route('/vote')
@login_required
@voter_required
def vote():
    if current_user.has_voted:
        flash('You have already voted!', 'info')
        return render_template('vote.html', positions=Position.query.all(), voted=True)
    
    positions = Position.query.all()
    return render_template('vote.html', positions=positions)

@voter_bp.route('/submit-vote', methods=['POST'])
@login_required
@voter_required
def submit_vote():
    if current_user.has_voted:
        flash('You have already voted!', 'error')
        return redirect(url_for('voter.results'))
    
    positions = Position.query.all()
    
    try:
        for position in positions:
            candidate_id = request.form.get(f'position_{position.id}')
            if candidate_id:
                candidate = Candidate.query.get(int(candidate_id))
                if candidate and candidate.position_id == position.id:
                    vote = Vote(
                        voter_id=current_user.id,
                        candidate_id=candidate.id,
                        position_id=position.id
                    )
                    candidate.votes_count += 1
                    db.session.add(vote)
        
        current_user.has_voted = True
        db.session.commit()
        flash('Your vote has been submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while submitting your vote.', 'error')
    
    return redirect(url_for('voter.vote'))

@voter_bp.route('/results')
@login_required
def results():
    # Only admins can view this page
    if not current_user.is_admin:
        flash('Results are only available to administrators.', 'error')
        return render_template('vote.html', positions=Position.query.all())
    
    # Admin can view results
    positions = Position.query.all()
    return render_template('results.html', positions=positions)

@voter_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@voter_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if current_user.check_password(current_password):
                current_user.set_password(new_password)
                flash('Profile updated successfully!', 'success')
            else:
                flash('Current password is incorrect.', 'error')
                return render_template('profile.html')
        else:
            flash('Profile updated successfully!', 'success')
        
        db.session.commit()
    
    return render_template('profile.html')
