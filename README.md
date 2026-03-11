Fantasy Name Forge 
A professional web application built with Django 5.2 that generates unique fantasy names for various RPG races using a custom linguistic algorithm.

Key Features
Dynamic Generation: Uses prefix-root-suffix logic to create thousands of unique names for Elves, Orcs, Dwarves, and more.

User Accounts: Secure registration and login system for saving personal favorites.

History Management: Automatically keeps only the last 50 generated names to optimize database performance.

Interactive UI: Smooth name generation and filtering using AJAX (JavaScript).

REST API: Integrated Django Rest Framework (DRF) endpoint for external data access.

Professional Admin Panel: Customized dashboard with advanced filters and search capabilities.

Tech Stack
Backend: Python 3.10+, Django 5.2

Database: SQLite (Development)

API: Django Rest Framework

Frontend: HTML5, CSS3, Vanilla JavaScript (AJAX)

Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/fantasy-name-forge.git
cd fantasy-name-forge
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Run migrations:

Bash
python manage.py migrate
Start the server:

Bash
python manage.py runserver
Open http://127.0.0.1:8000 in your browser.

API Documentation
You can access the latest generated names via the built-in API:

Endpoint: /api/recent/

Method: GET

Response: JSON list of name objects.
