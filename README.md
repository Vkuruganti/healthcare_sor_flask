# CareRecord Flask Health Care System of Record

CareRecord is a lightweight Flask web application for maintaining a local health care system of record. It captures core patient demographics, provider information, medical condition details, doctor notes, and user-defined custom fields in a simple browser-based interface.

The application is intentionally small and easy to run locally. It uses Flask for the web server, SQLite for local persistence, Jinja templates for server-rendered pages, and plain CSS/JavaScript for the user interface.

## What This Application Does

CareRecord lets users create, search, view, update, and delete patient records. Each record includes the required system-of-record fields requested for the application:

- Patient name
- Patient ID
- Date of birth
- Patient address
- Patient phone
- Patient email
- Medical condition
- Doctor name
- Doctor ID
- Doctor notes

Users can also add additional custom fields while creating or editing a record. For example, a clinic could add fields such as insurance provider, emergency contact, preferred pharmacy, blood type, visit type, or referral source without changing the database schema.

## Key Features

- Create patient records through a structured form
- Store records locally in SQLite
- Search records by patient name, patient ID, email, doctor name, medical condition, or custom fields
- View a detailed patient record page
- Edit existing records
- Delete records
- Add custom fields dynamically from the UI
- Keep runtime artifacts out of Git with `.gitignore`
- Run fully locally without requiring an external database

## Project Structure

```text
.
├── README.md
├── healthcare_sor_flask/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   ├── static/
│   │   ├── app.js
│   │   └── styles.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── record_detail.html
│       └── record_form.html
└── .gitignore
```

## Design Details

The UI was designed in the spirit of Google’s homepage: clean, direct, uncluttered, and focused around search. The main screen puts search at the center of the workflow so a user can quickly look up a patient record by name, ID, condition, doctor, email, or custom field.

Visual choices include:

- A bright white base with light gray section backgrounds
- A Google-inspired multicolor CareRecord wordmark
- A large rounded search input as the primary interaction
- Minimal navigation at the top of the page
- Simple record cards for fast scanning
- Restrained blue primary actions
- Compact forms with grouped patient, care team, and custom-field sections
- Responsive layouts that work on desktop and smaller screens

The application does not use a frontend framework. The interface is built with server-rendered Flask/Jinja templates, CSS, and a small JavaScript file for adding and removing custom fields dynamically.

## Data Storage

CareRecord uses SQLite. The database file is created automatically at:

```text
healthcare_sor_flask/healthcare_records.db
```

The database is ignored by Git because it is local runtime data. Each developer or user running the application locally gets their own SQLite database.

The main table is `records`, which stores the standard health care fields as columns. Custom fields are stored as JSON in the `extra_fields` column.

## Important Note

This is a local demo/training application. It is not production-ready for real protected health information. A production health care system would need security, authentication, authorization, audit logging, encryption, backup strategy, compliance review, deployment hardening, and HIPAA-related controls.

## Prerequisites

Install Python before running the app.

- Python 3.9 or newer
- Git
- A terminal application

Recommended:

- macOS: Terminal or iTerm2
- Windows: PowerShell or Windows Terminal

## Run Locally on macOS

From the directory where you want the project:

```bash
git clone https://github.com/Vkuruganti/healthcare_sor_flask.git
cd healthcare_sor_flask/healthcare_sor_flask
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask development server:

```bash
flask --app app run --debug
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

To stop the server, press `Ctrl+C` in the terminal.

## Run Locally on Windows

From PowerShell or Windows Terminal, clone the repository:

```powershell
git clone https://github.com/Vkuruganti/healthcare_sor_flask.git
cd healthcare_sor_flask\healthcare_sor_flask
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, run this command for the current terminal session and then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the Flask development server:

```powershell
flask --app app run --debug
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

To stop the server, press `Ctrl+C` in the terminal.

## Common Commands

Run the app:

```bash
flask --app app run --debug
```

Run on a different port:

```bash
flask --app app run --debug --port 5001
```

Deactivate the virtual environment:

```bash
deactivate
```

Remove local data and start with an empty database:

```bash
rm healthcare_records.db
```

On Windows PowerShell:

```powershell
Remove-Item healthcare_records.db
```

The database will be recreated automatically the next time the app starts.

## How to Use the App

1. Open `http://127.0.0.1:5000`.
2. Select `New record`.
3. Enter the patient and doctor information.
4. Add optional custom fields with the `Add field` button.
5. Save the record.
6. Use the home-page search box to find records.
7. Open a record to view details, edit it, or delete it.

## Application Routes

- `/` - record search and list page
- `/records/new` - create a new patient record
- `/records/<record_id>` - view a patient record
- `/records/<record_id>/edit` - edit a patient record
- `/records/<record_id>/delete` - delete a patient record

## Technology Stack

- Python
- Flask
- SQLite
- Jinja2 templates
- HTML
- CSS
- JavaScript

## Troubleshooting

If `flask` is not recognized, make sure the virtual environment is activated and dependencies are installed.

If port `5000` is already in use, run the app on another port:

```bash
flask --app app run --debug --port 5001
```

If the page loads but no records appear, that usually means the local SQLite database is empty. Create a new patient record from the UI.

If you want to reset all local records, delete `healthcare_records.db` from the `healthcare_sor_flask/` folder and restart the app.
