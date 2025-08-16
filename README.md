# Tech Fest Managemnt (DBMS Mini Project)
```
A web-based platform built using Django to manage Tech Fest activities.  
The system allows departments to create events, students to register, organizers to manage, and winners to be recorded.  
It demonstrates DBMS concepts with MySQL integration and CRUD operations.

```
## Deployed link https://dbmsdeplaoylive.onrender.com/
## Features
```
- Department Management (Add / Edit / Delete Departments)
- Student Management (with Department mapping)
- Venue Management
- Event Management (linked to Department & Venue)
- Student Event Registrations
- Winner Management (store event positions)
- Organizer Assignment to Events
- Admin & Normal User Authentication

```
## Tech Stack
```
- Python 3.13
- Django 5.2.3
- MySQL (preferred) / SQLite (for local testing)
- HTML5, CSS3, Bootstrap 4+
- Render / Localhost for deployment
```
## Project Structure
```
techfest/
├── techfest/         # Project settings
├── festapp/          # Core app with models, views, forms
├── templates/festapp # HTML templates
├── static/           # CSS, JS, Images
├── requirements.txt
└── README.md

```

##  Installation (For Local Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/techfest-management.git
cd techfest-management

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database in settings.py (MySQL or SQLite)

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver

```
## Database (MySQL Setup Example)
```
CREATE DATABASE techfest_db;
CREATE USER 'festuser'@'localhost' IDENTIFIED BY 'festpass';
GRANT ALL PRIVILEGES ON techfest_db.* TO 'festuser'@'localhost';
FLUSH PRIVILEGES;

```
## Update settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'techfest_db',
        'USER': 'festuser',
        'PASSWORD': 'festpass',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```


## Deployment on Render
```
- DEBUG=False
- SECRET_KEY=your_django_secret
- DATABASE_URL=mysql://festuser:festpass@host:3306/techfest_db

```
