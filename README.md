# ONLINE VOTING SYSTEM

A modern, secure online voting system built with Python Flask, MySQL, HTML, JavaScript, and CSS.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher (or MariaDB)
- pip (Python package manager)

### Installation Steps

1. **Navigate to the Python project directory:**
   ```bash
   cd online_voting_python
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL Database:**
   
   Edit `config.py` and set your MySQL credentials:
   ```python
   MYSQL_HOST = 'localhost'
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'your_mysql_password'  # Set your password
   MYSQL_DB = 'online_voting'
   ```

5. **Set up the database (Choose one method):**

   **Option A - Automatic Setup (Recommended):**
   ```bash
   python setup_database.py
   ```

   **Option B - Manual SQL Setup:**
   ```bash
   mysql -u root -p < database_schema.sql
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```

7. **Access the application:**
   - **Voter Portal:** http://localhost:5000
   - **Admin Panel:** http://localhost:5000/admin/login

### Default Admin Credentials
- **Email:** admin@gmail.com
- **Password:** admin

> ⚠️ **Important:** Change the default admin password after first login!

---

## 📁 Project Structure

```
online_voting_python/
├── app.py                      # Main Flask application entry point
├── config.py                   # Configuration settings (MySQL connection)
├── models.py                   # Database models (SQLAlchemy ORM)
├── requirements.txt            # Python dependencies
├── setup_database.py           # Database setup script
├── database_schema.sql         # SQL schema for manual setup
│
├── routes/                     # Route handlers (Blueprints)
│   ├── __init__.py
│   ├── auth.py                # Authentication routes (login, register, logout)
│   ├── voter.py               # Voter routes (vote, results, profile)
│   └── admin.py               # Admin routes (dashboard, manage candidates, etc.)
│
├── static/                     # Static files
│   ├── css/
│   │   ├── style.css          # Main stylesheet
│   │   └── admin.css          # Admin panel stylesheet
│   └── js/
│       ├── main.js            # Main JavaScript
│       └── admin.js           # Admin panel JavaScript
│
└── templates/                  # Jinja2 HTML templates
    ├── base.html              # Base template (navbar, footer)
    ├── index.html             # Landing page
    ├── login.html             # Voter login
    ├── register.html          # Voter registration
    ├── vote.html              # Voting page
    ├── results.html           # Results page
    ├── profile.html           # User profile
    └── admin/                 # Admin templates
        ├── base.html          # Admin base template (sidebar)
        ├── login.html         # Admin login
        ├── dashboard.html     # Admin dashboard
        ├── positions.html     # Manage positions
        ├── candidates.html    # Manage candidates
        ├── voters.html        # View voters
        ├── results.html       # View results
        └── manage_admins.html # Manage administrators
```

## ✨ Features

### Voter Features
- ✅ User registration with voter ID
- ✅ Secure login/logout
- ✅ Vote for candidates by position
- ✅ View real-time results with charts
- ✅ Profile management
- ✅ One vote per voter enforcement

### Admin Features
- ✅ Admin dashboard with statistics
- ✅ Manage positions (CRUD)
- ✅ Manage candidates (CRUD)
- ✅ View registered voters
- ✅ View voting results with charts
- ✅ Manage administrators
- ✅ Reset all votes

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root for custom configuration:

```env
SECRET_KEY=your-super-secret-key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=online_voting
```

### MySQL Configuration

The database connection is configured in `config.py`. You can either:

1. **Edit `config.py` directly** - Set your MySQL credentials
2. **Use environment variables** - Create a `.env` file
3. **Use the DATABASE_URL** - Set a full connection string

## 📊 Database Schema

The system uses 5 main tables:

| Table | Description |
|-------|-------------|
| `admins` | Administrator accounts |
| `voters` | Registered voters |
| `positions` | Election positions (e.g., Chairman, Secretary) |
| `candidates` | Candidates for each position |
| `votes` | Recorded votes (one per voter per position) |

## 🛠️ Technologies Used

- **Backend:** Python 3.x, Flask 3.0
- **Database:** MySQL with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js
- **Icons:** Font Awesome 6
- **Authentication:** Flask-Login

## 🔒 Security Features

- Password hashing with Werkzeug (scrypt)
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Input validation and sanitization
- Secure authentication flow
- One vote per voter per position enforcement

## 📝 API Endpoints

### Authentication Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/login` | Voter login |
| GET/POST | `/register` | Voter registration |
| GET | `/logout` | Logout |

### Voter Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vote` | Voting page |
| POST | `/submit-vote` | Submit vote |
| GET | `/results` | View results |
| GET/POST | `/profile` | Manage profile |

### Admin Routes (prefix: `/admin`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/login` | Admin login |
| GET | `/dashboard` | Admin dashboard |
| GET/POST | `/positions` | Manage positions |
| GET/POST | `/candidates` | Manage candidates |
| GET | `/voters` | View voters |
| GET | `/results` | View results |
| GET/POST | `/admins` | Manage admins |
| POST | `/reset-votes` | Reset all votes |

## 🐛 Troubleshooting

### Common Issues

1. **MySQL Connection Error:**
   - Ensure MySQL server is running
   - Check credentials in `config.py`
   - Verify the database exists

2. **Module Not Found:**
   - Activate virtual environment
   - Run `pip install -r requirements.txt`

3. **Permission Denied:**
   - Check MySQL user permissions
   - Ensure user has CREATE DATABASE privilege

## 📄 License

MIT License

## 🙏 Credits

Converted from PHP Online Voting System to Python Flask.

