# Capstone Student Portal by Jarib Ali

## Description

Capstone Student Portal is a simple web application built with Python and Flask that allows students to submit their personal information and upload profile pictures for admission processing. The application also provides an administrative dashboard for viewing, searching, and managing student records and admission statuses.

## Features

- Student registration portal
- Student profile image upload
- Admission status management
- Student record search functionality
- Administrative dashboard
- MySQL database integration
- Form validation and error handling

## Technology Stack

- Python
- Flask
- MySQL
- PyMySQL
- HTML/CSS
- Jinja2 Templates

## Installation

### Prerequisites

Before installing the application, ensure the following software is installed:

- Python 3.10 or later
- MySQL Server
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd capstoneStudentPortal
```

### Step 2: Create a Virtual Environment (in this project, flaskSP)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Run the `requirements.txt` file containing the required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL

Log in to MySQL and create the database:

```sql
CREATE DATABASE students;
```

Update the database configuration in `app.py` if necessary:

```python
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pswd'
app.config['MYSQL_DATABASE_DB'] = 'students'
```

### Step 5: Create the Student Table

Run the following SQL script:

```sql
CREATE TABLE student_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    dob DATE,
    gender VARCHAR(50),
    phone_number VARCHAR(50),
    address TEXT,
    region_of_origin VARCHAR(100),
    district_of_origin VARCHAR(100),
    next_of_kin VARCHAR(255),
    wassce_aggregate INT,
    status VARCHAR(50),
    photo_id VARCHAR(255)
);
```

### Step 6: Create Image Upload Directory

Ensure the following directory exists:

```text
static/images/
```

## How to Run the Application

Activate your virtual environment and start the Flask application:

```bash
python app.py
```

The application will start in development mode and be available at:

```text
http://127.0.0.1:5000
```

To stop the application, press:

```text
CTRL + C
```

## API Endpoints

### Home Page

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/` | GET, POST | Displays the main portal landing page |

### Student Portal

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/student/portal` | GET, POST | Displays the student application form |

### Student Details Submission

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/add_details` | POST | Saves student details to the database |

#### Request Example

```json
{
  "firstName": "John",
  "middleName": "K",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "dob": "2000-01-01",
  "gender": "Male",
  "phoneNumber": "0241234567",
  "address": "Kumasi",
  "regionOfOrigin": "Ashanti",
  "districtOfOrigin": "Kumasi Metropolitan",
  "nextOfKin": "Jane Doe",
  "wassceAggregate": "24",
  "status": "pending",
  "photoId": "abc123"
}
```

#### Success Response

```json
{
  "status": "success",
  "message": "Data saved successfully"
}
```

#### Error Response

```json
{
  "status": "error",
  "message": "Email is invalid"
}
```

### Image Upload

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/add_image` | POST | Uploads a student profile image |

#### Request

Multipart form-data:

```text
file=<image-file>
```

#### Success Response

```json
{
  "status": "success",
  "message": "Image uploaded successfully",
  "photo_id": "generated_photo_id"
}
```

### View Student Profile

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/student/<id>/view` | GET | Displays a student's profile |

#### Example

```http
GET /student/1/view
```

### Update Student Status

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/student/edit` | POST | Updates admission status |

#### Request Example

```json
{
  "id": 1,
  "status": "admitted"
}
```

#### Allowed Status Values

- admitted
- pending
- rejected

### Admin Dashboard

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/admin/dashboard` | GET | Displays all student records |

### Student Search

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/admin/<source>/<key>/search` | GET | Searches student records |

#### Supported Search Sources

| Source | Description |
|----------|-------------|
| name | Search by first or last name |
| status | Search by admission status |
| gender | Search by gender |
| agg | Search by WASSCE aggregate |

#### Examples

```http
GET /admin/name/John
```

```http
GET /admin/status/pending
```

```http
GET /admin/gender/Male
```

```http
GET /admin/agg/24
```

## Example Usage

### Start the Application

```bash
python app.py
```

### Submit Student Information

```bash
curl -X POST http://127.0.0.1:5000/add_details \
-H "Content-Type: application/json" \
-d '{
    "firstName":"John",
    "middleName":"K",
    "lastName":"Doe",
    "email":"john.doe@example.com",
    "dob":"2000-01-01",
    "gender":"Male",
    "phoneNumber":"0241234567",
    "address":"Kumasi",
    "regionOfOrigin":"Ashanti",
    "districtOfOrigin":"Kumasi Metropolitan",
    "nextOfKin":"Jane Doe",
    "wassceAggregate":"24",
    "status":"pending",
    "photoId":"abc123"
}'
```

### Upload a Profile Picture

```bash
curl -X POST http://127.0.0.1:5000/add_image \
-F "file=@student_photo.png"
```

### View Student Record

```bash
curl http://127.0.0.1:5000/student/1/view
```

### Update Admission Status

```bash
curl -X POST http://127.0.0.1:5000/student/edit \
-H "Content-Type: application/json" \
-d '{
    "id":1,
    "status":"admitted"
}'
```

## Requirements

```text
blinker==1.9.0
click==8.4.1
colorama==0.4.6
Flask==3.1.3
Flask-MySQL==1.6.0
Flask-MySQLdb==2.0.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
mysqlclient==2.2.8
PyMySQL==1.2.0
Werkzeug==3.1.8
```

## Project Structure

```text
capstoneStudentPortal/
│
├── app.py
├── requirements.txt
├── static/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── student-form.html
│   ├── students-index.html
│
└── README.md
```

## Walkthrough
Watch the walkthrough video for a full glimps of the portal.
│ capstoneBackendWalkthrough.mp4

## Author

**Jarib Ali**

Capstone Student Portal Project
