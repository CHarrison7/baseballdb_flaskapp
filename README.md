# Baseball Database Flask Project

This repository contains a Python Flask project originally developed for a databases course. Follow the instructions below to get started.

## Features
- [Briefly describe your project's features.]

## Prerequisites
Make sure you have the following installed:
- Python 3.6 or later
- pip (Python package manager)

## Setup

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/CHarrison7/baseballdb_flaskapp.git
cd repository
```

### Step 2: Create a Virtual Environment
Create a virtual environment to isolate dependencies:
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Step 4: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 5: Setup environment variables

Sample ".env" file:
```
DB_ROOT_PASSWORD=defnotroot
DB_USER_PASSWORD=defnotuser
```

Sample ".flaskenv" file:
```
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=development
SECRET_KEY=<your bcrypt private key here>
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database>
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@<host>:<port>/<database>
DB_ROOT_PASSWORD=<root user password for database>
```

### Step 6: Run sqlite database via docker-compose file
* You can change the environment variables for the database's properties/credentials in the docker-compose.yml file, if desired

```bash
docker-compose up
```

### Step 7: Run the Application
Run the main Python script:
```bash
python src/app.py
```

