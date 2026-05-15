# CareRecord Flask App

A small Flask health care system of record for patient demographics, doctor details, medical condition, notes, and user-defined custom fields.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Then open `http://127.0.0.1:5000`.

Records are stored locally in `healthcare_records.db`, which is created automatically.
