# 🎓 Tech Fest Management System (DBMS Mini Project)

A comprehensive web-based platform built using Django to manage Tech Fest activities with complete CRUD operations, CSV import/export functionality, and role-based access control.

The system allows departments to create events, students to register, organizers to manage activities, and winners to be recorded. It demonstrates advanced DBMS concepts with MySQL integration, referential integrity, and complex querying.

## 🌐 Deployed Link
**Live Demo:** [https://dbmsdeplaoylive.onrender.com/](https://dbmsdeplaoylive.onrender.com/)

---

## ✨ Features

### 🔐 Authentication & Authorization
- **User Authentication**: Login/Logout functionality
- **Role-Based Access Control**: Admin and regular user permissions
- **Protected Routes**: Admin-only access for create/update/delete operations
- **Session Management**: Secure session handling

### 📋 Core Modules (Full CRUD Operations)

#### 1️⃣ **Department Management**
- ✅ Add new departments with HOD details
- ✏️ Edit existing department information
- 📄 View all departments in organized lists
- 🗑️ Safe deletion with referential integrity checks
- 🔗 Foreign key relationships with students and events

#### 2️⃣ **Student Management**
- ✅ Register students with unique roll numbers
- 📧 Email validation and department assignment
- 🔄 Update student information
- 🔍 View complete student directory
- ⚠️ Duplicate roll number prevention
- 🗑️ Protected deletion (prevents if registrations exist)

#### 3️⃣ **Venue Management**
- 🏛️ Add venues with location and capacity details
- 📊 Track venue utilization
- ✏️ Update venue specifications
- 📍 Location-based organization
- 🗑️ Safe deletion with event dependency checks

#### 4️⃣ **Event Management**
- 🎪 Create events with comprehensive details
- 📅 Date scheduling and management
- 🏢 Link events to departments and venues
- 📝 Rich descriptions and event metadata
- 🔄 Update event information
- 🗑️ Cascade protection for related records

#### 5️⃣ **Registration System**
- 📝 Student event registration
- ⏰ Automatic timestamp recording
- 🚫 Duplicate registration prevention
- ✏️ Edit existing registrations
- 📊 View all registrations with student and event details
- 🗑️ Clean deletion management

#### 6️⃣ **Winner Management**
- 🏆 Record event winners (1st, 2nd, 3rd positions)
- ✅ Position uniqueness validation per event
- 🎯 Link winners to students and events
- ✏️ Update winner information
- 📊 Winner leaderboard display
- ⚠️ Prevent duplicate position awards

#### 7️⃣ **Organizer Management**
- 👥 Assign organizers to events
- 📞 Store contact information
- 🔗 Event-organizer relationship tracking
- ✏️ Update organizer details
- 📋 View organizer assignments

### 📊 Advanced Features

#### 📤 CSV Import System (Bulk Data Upload)
- **Import Departments**: Bulk upload with name and HOD details
- **Import Students**: Mass student registration with department linking
- **Import Venues**: Quick venue setup with capacity management
- **Import Events**: Event creation with venue and department associations
- **Import Registrations**: Batch registration using roll numbers and event titles
- **Import Winners**: Bulk winner recording with position validation
- **Import Organizers**: Quick organizer assignment to events

**Features:**
- ✅ CSV validation and error reporting
- 📊 Success/failure statistics
- ⚠️ Detailed error messages (shows first 5 errors)
- 📝 Sample CSV format examples provided
- 🔄 Relationship validation (checks if referenced records exist)
- 🛡️ Duplicate prevention

#### 📥 CSV Export System (Data Download)
- Export any entity data to CSV format
- Includes all relationships (foreign keys shown as names)
- Formatted date/time fields
- One-click download functionality
- Supports all 7 entities:
  - Departments
  - Students (with department names)
  - Venues
  - Events (with venue and department names)
  - Registrations (with student and event details)
  - Winners (with event and student information)
  - Organizers (with event titles)

#### 🛡️ Data Integrity Features
- **Safe Delete Mechanism**: Prevents deletion of records with dependencies
- **Referential Integrity**: Foreign key constraints enforced
- **Unique Constraints**: Roll numbers, event positions
- **Validation**: Email format, capacity limits, position ranges (1-3)
- **Error Handling**: User-friendly error messages
- **Transaction Management**: Database consistency maintained

#### 🏥 Health Check Endpoint
- `/health/` endpoint for monitoring
- Returns JSON status for deployment health checks
- Used by Render/AWS/Heroku for uptime monitoring

---

## 🛠️ Tech Stack

### Backend
- **Python** 3.13
- **Django** 5.2.3
- **MySQL** (Production) / SQLite (Development)
- **mysqlclient** 2.2.7 - MySQL database adapter

### Frontend
- **HTML5** & **CSS3**
- **Bootstrap** 4+ - Responsive UI framework
- **JavaScript** - Interactive features

### Deployment & DevOps
- **WhiteNoise** 6.9.0 - Static file serving
- **Gunicorn** 23.0.0 - WSGI HTTP server
- **dj-database-url** 3.0.0 - Database URL parsing
- **python-decouple** 3.8 - Settings management
- **Render** - Cloud hosting platform

### Additional Libraries
- **Django REST Framework** 3.16.0
- **django-import-export** 4.3.7
- **Cloudinary** 1.44.1 (for media storage)
- **django-cloudinary-storage** 0.3.0

---

## 📁 Project Structure

```
TechFestDeployed/
│
├── techfest/                    # Project configuration
│   ├── settings.py             # Django settings with MySQL config
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
│
├── festapp/                     # Main application
│   ├── models.py               # Database models (7 entities)
│   ├── views.py                # Business logic & request handling
│   ├── forms.py                # Form definitions
│   ├── urls.py                 # App-specific URL patterns
│   ├── admin.py                # Django admin configuration
│   ├── migrations/             # Database migration files
│   └── templates/festapp/      # HTML templates
│       ├── base.html           # Base template
│       ├── index.html          # Homepage
│       ├── login.html          # Login page
│       ├── *_list.html         # List views for entities
│       ├── *_form.html         # Create/Edit forms
│       ├── csv_import.html     # CSV import selector
│       ├── csv_import_form.html # CSV upload interface
│       ├── export_data.html    # CSV export page
│       ├── confirm_delete.html # Deletion confirmation
│       └── delete_error.html   # Protected deletion errors
│
├── static/                      # Static files
│   └── images/                 # Logo and images
│       └── LBSLogoWhite.png
│
├── staticfiles/                 # Collected static files (for production)
│
├── csv_samples/                 # Sample CSV files for import
│   ├── sample_departments.csv
│   ├── sample_students.csv
│   ├── sample_venues.csv
│   ├── sample_events.csv
│   ├── sample_registrations.csv
│   ├── sample_winners.csv
│   └── sample_organizers.csv
│
├── requirements.txt             # Python dependencies
├── Procfile                     # Render deployment config
├── manage.py                    # Django management script
├── README.md                    # This file
├── .env                         # Environment variables (not in git)
└── CSV_IMPORT_GUIDE.md         # Detailed CSV import instructions

```

---

## 🚀 Installation (Local Development)

### Prerequisites
- Python 3.10 or higher
- MySQL Server 8.0+ (or MariaDB)
- pip (Python package manager)
- Git

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/SRINIVASRAOAMMANGOD/TechFestDeployed.git
cd TechFestDeployed

# 2. Create a virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with your configuration
# Copy the example below and update with your values

# 6. Set up MySQL database (see Database Setup section)

# 7. Apply database migrations
python manage.py migrate

# 8. Create a superuser (admin account)
python manage.py createsuperuser

# 9. Collect static files
python manage.py collectstatic --noinput

# 10. Run development server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 🗄️ Database Setup

### MySQL Configuration

```sql
-- Create database
CREATE DATABASE techfest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'festuser'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON techfest_db.* TO 'festuser'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;
```

### Environment Variables (.env file)

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-django-secret-key-here
DEBUG=True

# Database Configuration
DATABASE_URL=mysql://festuser:your_secure_password@localhost:3306/techfest_db

# For production (Render)
# DATABASE_URL=mysql://user:password@host:3306/database_name
```

### Database Schema

The system uses 7 main tables:

1. **department** - Stores academic departments
2. **student** - Student information with department FK
3. **venue** - Event locations and capacity
4. **event** - Festival events with venue and department FKs
5. **registration** - Student event registrations (many-to-many)
6. **winner** - Event winners with positions
7. **organizer** - Event organizers and contacts

---

## 📤 CSV Import/Export Guide

### Importing Data

1. Navigate to **CSV Import** from the main menu
2. Select the entity type to import
3. Download the sample CSV format (shown on screen)
4. Prepare your CSV file matching the format
5. Upload and import
6. View success/error statistics

### CSV Format Examples

**Departments:**
```csv
name,hod_name
Computer Science,Dr. Smith
Electronics,Dr. Johnson
```

**Students:**
```csv
name,roll_number,email,department
John Doe,CS001,john@example.com,Computer Science
Jane Smith,CS002,jane@example.com,Electronics
```

**Events:**
```csv
title,description,date,venue,department
Coding Contest,Programming competition,2025-10-25,Main Hall,Computer Science
Robotics,Robot building event,2025-10-26,Auditorium,Electronics
```

See `csv_samples/` folder for complete examples.

### Exporting Data

1. Navigate to **Export Data** from the main menu
2. Select entity type
3. Click Export
4. CSV file downloads automatically

---

## 🔒 Security Features

- **CSRF Protection**: All forms protected
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Template auto-escaping
- **Authentication Required**: Protected routes
- **Role-Based Access**: Admin-only operations
- **Environment Variables**: Sensitive data in .env
- **Referential Integrity**: Database constraints
- **Input Validation**: Form and model validation

---

## 🌐 Deployment on Render

### Configuration

**Environment Variables:**
```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=mysql://user:password@host:3306/database
ALLOWED_HOSTS=yourdomain.onrender.com
```

**Render Settings:**
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start Command: `gunicorn techfest.wsgi:application`
- Health Check Path: `/health/`

---

## 📱 API Endpoints

### Public Routes
- `/` - Homepage
- `/login/` - User login
- `/logout/` - User logout
- `/health/` - Health check (JSON response)

### Entity Routes (Pattern for all entities)
- `/entities/` - List view
- `/entities/add/` - Create (Admin only)
- `/entities/<id>/edit/` - Update (Admin only)
- `/entities/<id>/delete/` - Delete (Admin only)

### CSV Operations
- `/csv-import/` - Import selector
- `/csv-import/<entity>/` - Entity-specific import
- `/export/` - Export selector

---

## 🎯 Future Enhancements

- [ ] Email notifications for registrations
- [ ] Event capacity tracking
- [ ] Student dashboard with registered events
- [ ] QR code generation for registrations
- [ ] Analytics and reporting dashboard
- [ ] Mobile responsive improvements
- [ ] Real-time event updates
- [ ] Payment integration for paid events
- [ ] Certificate generation for winners
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for educational purposes as a DBMS Mini Project.

---

## 👨‍💻 Author

**SRINIVAS RAO AMMANGOD**
- GitHub: [@SRINIVASRAOAMMANGOD](https://github.com/SRINIVASRAOAMMANGOD)
- Repository: [TechFestDeployed](https://github.com/SRINIVASRAOAMMANGOD/TechFestDeployed)

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Framework
- Render Platform for hosting
- MySQL Community

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `/docs/` folder
- Review CSV_IMPORT_GUIDE.md for import help

---

**Last Updated:** October 2025  
**Version:** 2.0  
**Status:** ✅ Production Ready
