import sqlite3
import csv
from flask import Blueprint, send_file
import os

export = Blueprint("export", __name__)

DATABASE = "database/database.db"


@export.route("/admin/export/csv")
def export_csv():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               username,
               news,
               prediction
        FROM history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    os.makedirs("exports", exist_ok=True)

    filename = "exports/prediction_history.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Username",
            "News",
            "Prediction"
        ])

        for row in rows:
            writer.writerow(row)

    return send_file(
        filename,
        as_attachment=True,
        download_name="prediction_history.csv"
    )
