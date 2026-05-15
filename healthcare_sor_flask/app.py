import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from flask import Flask, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "healthcare_records.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-healthcare-sor-change-me"


DEFAULT_FIELDS = [
    "patient_name",
    "patient_id",
    "dob",
    "patient_address",
    "patient_phone",
    "patient_email",
    "medical_condition",
    "doctor_name",
    "doctor_id",
    "doctor_notes",
]


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error: Optional[BaseException]) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_id TEXT NOT NULL UNIQUE,
            dob TEXT,
            patient_address TEXT,
            patient_phone TEXT,
            patient_email TEXT,
            medical_condition TEXT,
            doctor_name TEXT,
            doctor_id TEXT,
            doctor_notes TEXT,
            extra_fields TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    db.commit()


@app.before_request
def ensure_database() -> None:
    init_db()


def record_from_form() -> dict:
    return {field: request.form.get(field, "").strip() for field in DEFAULT_FIELDS}


def extras_from_form() -> dict:
    labels = request.form.getlist("extra_label[]")
    values = request.form.getlist("extra_value[]")
    extras = {}
    for label, value in zip(labels, values):
        label = label.strip()
        value = value.strip()
        if label:
            extras[label] = value
    return extras


def serialize_record(row: sqlite3.Row) -> dict:
    record = dict(row)
    record["extra_fields"] = json.loads(record.get("extra_fields") or "{}")
    return record


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    db = get_db()

    if query:
        like_query = f"%{query}%"
        rows = db.execute(
            """
            SELECT * FROM records
            WHERE patient_name LIKE ?
               OR patient_id LIKE ?
               OR patient_email LIKE ?
               OR doctor_name LIKE ?
               OR medical_condition LIKE ?
               OR extra_fields LIKE ?
            ORDER BY updated_at DESC
            """,
            (like_query, like_query, like_query, like_query, like_query, like_query),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM records ORDER BY updated_at DESC").fetchall()

    records = [serialize_record(row) for row in rows]
    return render_template("index.html", records=records, query=query)


@app.route("/records/new", methods=("GET", "POST"))
def create_record():
    if request.method == "POST":
        data = record_from_form()
        extras = extras_from_form()
        now = datetime.utcnow().isoformat(timespec="seconds")

        if not data["patient_name"] or not data["patient_id"]:
            flash("Patient name and patient ID are required.", "error")
            return render_template("record_form.html", record=data, extras=extras, mode="create")

        try:
            get_db().execute(
                """
                INSERT INTO records (
                    patient_name, patient_id, dob, patient_address, patient_phone,
                    patient_email, medical_condition, doctor_name, doctor_id,
                    doctor_notes, extra_fields, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["patient_name"],
                    data["patient_id"],
                    data["dob"],
                    data["patient_address"],
                    data["patient_phone"],
                    data["patient_email"],
                    data["medical_condition"],
                    data["doctor_name"],
                    data["doctor_id"],
                    data["doctor_notes"],
                    json.dumps(extras),
                    now,
                    now,
                ),
            )
            get_db().commit()
        except sqlite3.IntegrityError:
            flash("A record with that patient ID already exists.", "error")
            return render_template("record_form.html", record=data, extras=extras, mode="create")

        flash("Patient record created.", "success")
        return redirect(url_for("index"))

    empty_record = {field: "" for field in DEFAULT_FIELDS}
    return render_template("record_form.html", record=empty_record, extras={}, mode="create")


@app.route("/records/<int:record_id>")
def view_record(record_id: int):
    row = get_db().execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    if row is None:
        flash("Record not found.", "error")
        return redirect(url_for("index"))
    return render_template("record_detail.html", record=serialize_record(row))


@app.route("/records/<int:record_id>/edit", methods=("GET", "POST"))
def edit_record(record_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    if row is None:
        flash("Record not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        data = record_from_form()
        extras = extras_from_form()
        now = datetime.utcnow().isoformat(timespec="seconds")

        if not data["patient_name"] or not data["patient_id"]:
            flash("Patient name and patient ID are required.", "error")
            return render_template("record_form.html", record=data, extras=extras, mode="edit")

        try:
            db.execute(
                """
                UPDATE records
                SET patient_name = ?, patient_id = ?, dob = ?, patient_address = ?,
                    patient_phone = ?, patient_email = ?, medical_condition = ?,
                    doctor_name = ?, doctor_id = ?, doctor_notes = ?,
                    extra_fields = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    data["patient_name"],
                    data["patient_id"],
                    data["dob"],
                    data["patient_address"],
                    data["patient_phone"],
                    data["patient_email"],
                    data["medical_condition"],
                    data["doctor_name"],
                    data["doctor_id"],
                    data["doctor_notes"],
                    json.dumps(extras),
                    now,
                    record_id,
                ),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("A record with that patient ID already exists.", "error")
            return render_template("record_form.html", record=data, extras=extras, mode="edit")

        flash("Patient record updated.", "success")
        return redirect(url_for("view_record", record_id=record_id))

    record = serialize_record(row)
    return render_template(
        "record_form.html",
        record=record,
        extras=record["extra_fields"],
        mode="edit",
    )


@app.post("/records/<int:record_id>/delete")
def delete_record(record_id: int):
    db = get_db()
    db.execute("DELETE FROM records WHERE id = ?", (record_id,))
    db.commit()
    flash("Patient record deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
