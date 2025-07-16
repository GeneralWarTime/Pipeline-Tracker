# Pipeline - Job Tracking Dashboard

A comprehensive web application for recruiters to track active jobs, pipeline roles, and commission calculations.

## 🚀 Features

### 📊 Dashboard
- **Active Jobs Tracking**: Monitor jobs with Active, Pending, and Placed statuses
- **Real-time Statistics**: View deal sizes, commission calculations, and pipeline metrics
- **Month-based Dates**: Simple month selection instead of complex date formatting
- **Client Dropdown**: Automatic supplier margin settings based on client selection

### 👥 Contractors Management
- **Placed Candidates**: Track successfully placed contractors
- **Commission Tracking**: Automatic commission calculations (9% default)
- **Full CRUD Operations**: Create, read, update, and delete contractor records

### 💸 Money Lost Tracking
- **Closed Jobs**: Track jobs that didn't result in placements
- **Close Reasons**: Categorize losses (Lost to Competition, Cancelled or Hold, Aryan's Fault)
- **Revenue Impact**: Calculate lost deal sizes and commissions
- **Add Close Reasons**: Modal interface to add reasons to closed jobs

### 🗑️ Delete Functionality
- **Delete Jobs**: Remove jobs from the main pipeline
- **Delete Contractors**: Remove placed contractors
- **Delete Closed Jobs**: Remove entries from money lost tracking

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Modern CSS with responsive design

## 📋 Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd IN&OUT
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://127.0.0.1:5000`
   - The app will automatically create the database on first run

## 📱 Usage

### Adding Jobs
1. Click "Add New Job" on the dashboard
2. Fill in job details (title, client, hiring manager, etc.)
3. Select starting month from dropdown
4. Enter deal size and commission rate
5. Choose status (Active, Pending, Closed, Placed)
6. Save the job

### Managing Contractors
1. Navigate to the "Contractors" page
2. Add new contractors with their details
3. View placed candidates and their commission amounts
4. Delete contractors as needed

### Tracking Money Lost
1. Go to the "Money Lost" page
2. View closed jobs that didn't result in placements
3. Add close reasons using the "Add Close Reason" button
4. Track lost revenue and commission

### Closing Jobs
1. Edit a job and change status to "Closed"
2. Navigate to Money Lost page
3. Use "Add Close Reason" to categorize the loss
4. Track the financial impact

## 🗂️ Project Structure

```
IN&OUT/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html        # Dashboard page
│   ├── contractors.html  # Contractors management
│   └── money_lost.html   # Money lost tracking
├── instance/             # Database files (auto-created)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Key Features

### Database Models
- **Job**: Tracks active/pending jobs with deal sizes and commissions
- **Contractor**: Manages placed candidates with commission tracking

### API Endpoints
- `GET /api/jobs` - Retrieve all jobs
- `POST /api/jobs` - Create new job
- `PUT /api/jobs/<id>` - Update job (supports partial updates)
- `DELETE /api/jobs/<id>` - Delete job
- `GET /api/contractors` - Retrieve all contractors
- `POST /api/contractors` - Create new contractor
- `DELETE /api/contractors/<id>` - Delete contractor
- `GET /api/stats` - Dashboard statistics
- `GET /api/contractor-stats` - Contractor statistics
- `GET /api/money-lost` - Money lost statistics

### Frontend Features
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Automatic page refresh after operations
- **Confirmation Dialogs**: Safe delete operations
- **Form Validation**: Client-side and server-side validation
- **Modal Interfaces**: Clean user experience for data entry

## 🎯 Business Logic

### Commission Calculations
- Default commission rate: 9%
- Automatic calculation: `commission_amount = deal_size * commission_rate`
- Monthly projections: `yearly_commission / 12`

### Status Management
- **Active**: Jobs currently being worked on
- **Pending**: Jobs on hold or waiting for decisions
- **Closed**: Jobs that didn't result in placement (moved to Money Lost)
- **Placed**: Successful placements (moved to Contractors)

### Close Reasons
- **Lost to Competition**: Another recruiter won the placement
- **Cancelled or Hold**: Client put the role on hold
- **Aryan's Fault**: Internal issues with the recruitment process

## 🔒 Security Notes

- Development server only - not for production use
- SQLite database for simplicity
- No authentication implemented (add for production)

## 🚀 Deployment

For production deployment:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up proper authentication
3. Use a production database (PostgreSQL, MySQL)
4. Configure environment variables
5. Set up HTTPS

## 📝 License

This project is for internal use by the recruitment team.

## 🤝 Contributing

This is a private project for the recruitment team. For questions or issues, contact the development team. 