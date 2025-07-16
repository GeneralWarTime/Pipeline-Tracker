#!/usr/bin/env python3
"""
Job Tracking Dashboard
A comprehensive tool for recruiters to track active jobs, pipeline roles, and commission calculations.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Job(db.Model):
    """Job model for tracking recruitment opportunities."""
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    hiring_manager = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)  # Store as month name
    deal_size = db.Column(db.Float, nullable=False)
    commission_rate = db.Column(db.Float, default=0.09)  # 9% default
    commission_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Active')  # Active, Closed, Pending, Placed
    close_reason = db.Column(db.String(100))  # Lost to Competition, Cancelled or Hold, Aryan's Fault
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def calculate_commission(self):
        """Calculate commission amount based on deal size and rate."""
        self.commission_amount = self.deal_size * self.commission_rate
        return self.commission_amount

    def to_dict(self):
        """Convert job to dictionary for JSON response."""
        return {
            'id': self.id,
            'job_title': self.job_title,
            'client_name': self.client_name,
            'hiring_manager': self.hiring_manager,
            'start_date': self.start_date,  # Month name as string
            'deal_size': self.deal_size,
            'commission_rate': self.commission_rate,
            'commission_amount': self.commission_amount,
            'status': self.status,
            'close_reason': self.close_reason,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'notes': self.notes
        }

class Contractor(db.Model):
    """Contractor model for tracking placed candidates."""
    id = db.Column(db.Integer, primary_key=True)
    contractor_name = db.Column(db.String(200), nullable=False)  # Required field
    job_title = db.Column(db.String(200), nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    hiring_manager = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)  # Store as month name
    deal_size = db.Column(db.Float, nullable=False)
    commission_rate = db.Column(db.Float, default=0.09)
    commission_amount = db.Column(db.Float, nullable=False)
    placed_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def calculate_commission(self):
        """Calculate commission amount based on deal size and rate."""
        self.commission_amount = self.deal_size * self.commission_rate
        return self.commission_amount

    def to_dict(self):
        """Convert contractor to dictionary for JSON response."""
        return {
            'id': self.id,
            'contractor_name': self.contractor_name,
            'job_title': self.job_title,
            'client_name': self.client_name,
            'hiring_manager': self.hiring_manager,
            'start_date': self.start_date,  # Month name as string
            'deal_size': self.deal_size,
            'commission_rate': self.commission_rate,
            'commission_amount': self.commission_amount,
            'placed_date': self.placed_date.strftime('%Y-%m-%d %H:%M') if self.placed_date else None,
            'notes': self.notes
        }

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/contractors')
def contractors():
    """Contractors page."""
    return render_template('contractors.html')

@app.route('/money-lost')
def money_lost():
    """Money Lost page."""
    return render_template('money_lost.html')

@app.route('/api/jobs')
def get_jobs():
    """Get all jobs."""
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job."""
    try:
        data = request.get_json()
        
        # Create new job
        job = Job(
            job_title=data['job_title'],
            client_name=data['client_name'],
            hiring_manager=data['hiring_manager'],
            start_date=data['start_date'],  # Store month name directly
            deal_size=float(data['deal_size']),
            commission_rate=float(data.get('commission_rate', 0.09)),
            status=data.get('status', 'Active'),
            close_reason=data.get('close_reason', ''),
            notes=data.get('notes', '')
        )
        
        # Calculate commission
        job.calculate_commission()
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({'success': True, 'job': job.to_dict()})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update an existing job."""
    try:
        job = Job.query.get_or_404(job_id)
        data = request.get_json()
        
        # Handle partial updates (like just updating close_reason)
        if len(data) == 1 and 'close_reason' in data:
            job.close_reason = data['close_reason']
            db.session.commit()
            return jsonify({'success': True, 'job': job.to_dict()})
        
        # Check if status is changing to "Placed"
        old_status = job.status
        new_status = data.get('status', 'Active')
        
        # Update fields
        job.job_title = data['job_title']
        job.client_name = data['client_name']
        job.hiring_manager = data['hiring_manager']
        job.start_date = data['start_date']  # Store month name directly
        job.deal_size = float(data['deal_size'])
        job.commission_rate = float(data.get('commission_rate', 0.09))
        job.status = new_status
        job.close_reason = data.get('close_reason', '')
        job.notes = data.get('notes', '')
        
        # Recalculate commission
        job.calculate_commission()
        
        # If status changed to "Placed", move to contractors
        if old_status != 'Placed' and new_status == 'Placed':
            # Get contractor name from request
            contractor_name = data.get('contractor_name', '')
            if not contractor_name:
                return jsonify({'success': False, 'error': 'Contractor name is required when placing a job'}), 400
            
            contractor = Contractor(
                contractor_name=contractor_name,
                job_title=job.job_title,
                client_name=job.client_name,
                hiring_manager=job.hiring_manager,
                start_date=job.start_date,
                deal_size=job.deal_size,
                commission_rate=job.commission_rate,
                notes=job.notes
            )
            contractor.calculate_commission()
            db.session.add(contractor)
            db.session.delete(job)  # Remove from jobs table
        
        db.session.commit()
        
        if new_status == 'Placed':
            return jsonify({'success': True, 'contractor': contractor.to_dict()})
        else:
            return jsonify({'success': True, 'job': job.to_dict()})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job."""
    try:
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/contractors')
def get_contractors():
    """Get all contractors."""
    contractors = Contractor.query.order_by(Contractor.placed_date.desc()).all()
    return jsonify([contractor.to_dict() for contractor in contractors])

@app.route('/api/contractors', methods=['POST'])
def create_contractor():
    """Create a new contractor directly."""
    try:
        data = request.get_json()
        
        # Create new contractor
        contractor = Contractor(
            contractor_name=data['contractor_name'],
            job_title=data['job_title'],
            client_name=data['client_name'],
            hiring_manager=data['hiring_manager'],
            start_date=data['start_date'],  # Store month name directly
            deal_size=float(data['deal_size']),
            commission_rate=float(data.get('commission_rate', 0.09)),
            notes=data.get('notes', '')
        )
        
        # Calculate commission
        contractor.calculate_commission()
        
        db.session.add(contractor)
        db.session.commit()
        
        return jsonify({'success': True, 'contractor': contractor.to_dict()})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/contractors/<int:contractor_id>', methods=['DELETE'])
def delete_contractor(contractor_id):
    """Delete a contractor."""
    try:
        contractor = Contractor.query.get_or_404(contractor_id)
        db.session.delete(contractor)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics - Jobs only (projected numbers, excluding closed jobs)."""
    try:
        # Job stats (projected numbers) - exclude closed jobs from main dashboard
        total_jobs = Job.query.filter(Job.status != 'Closed').count()
        active_jobs = Job.query.filter_by(status='Active').count()
        pending_jobs = Job.query.filter_by(status='Pending').count()
        
        # Job totals (projected) - exclude closed jobs
        job_deal_size = db.session.query(db.func.sum(Job.deal_size)).filter(Job.status != 'Closed').scalar() or 0
        job_commission = db.session.query(db.func.sum(Job.commission_amount)).filter(Job.status != 'Closed').scalar() or 0
        
        # Calculate yearly commission (9% of job deal size)
        yearly_commission = job_deal_size * 0.09
        
        # Calculate monthly commission (yearly commission divided by 12)
        monthly_commission = yearly_commission / 12
        
        return jsonify({
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'pending_jobs': pending_jobs,
            'job_deal_size': job_deal_size,
            'job_commission': job_commission,
            'yearly_commission': yearly_commission,
            'monthly_commission': monthly_commission
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/contractor-stats')
def get_contractor_stats():
    """Get contractor statistics - Actual placed numbers."""
    try:
        total_contractors = Contractor.query.count()
        
        # Contractor totals (actual)
        contractor_deal_size = db.session.query(db.func.sum(Contractor.deal_size)).scalar() or 0
        contractor_commission = db.session.query(db.func.sum(Contractor.commission_amount)).scalar() or 0
        
        # Calculate monthly commission (contractor commission divided by 12)
        monthly_commission = contractor_commission / 12
        
        return jsonify({
            'total_contractors': total_contractors,
            'contractor_deal_size': contractor_deal_size,
            'contractor_commission': contractor_commission,
            'monthly_commission': monthly_commission
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/money-lost')
def get_money_lost():
    """Get money lost statistics - Closed jobs with reasons only."""
    try:
        # Only include closed jobs that have a close reason
        closed_jobs = Job.query.filter(
            Job.status == 'Closed',
            Job.close_reason.isnot(None),
            Job.close_reason != ''
        ).all()
        
        total_closed_jobs = len(closed_jobs)
        lost_deal_size = sum(job.deal_size for job in closed_jobs)
        lost_commission = sum(job.commission_amount for job in closed_jobs)
        
        return jsonify({
            'total_closed_jobs': total_closed_jobs,
            'lost_deal_size': lost_deal_size,
            'lost_commission': lost_commission
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 