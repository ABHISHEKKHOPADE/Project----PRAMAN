import sqlite3
import os

DB_PATH = "database/praman.db"

os.makedirs("database", exist_ok=True)


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_table()

    ####################################################

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS verifications(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            dob TEXT,

            gender TEXT,

            aadhaar TEXT,

            confidence INTEGER,

            similarity REAL,

            quality TEXT,

            tampering TEXT,

            status TEXT,

            report TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.conn.commit()

    ####################################################

    def insert(self, report):

        aadhaar = report["aadhaar"]

        face = report["face"]

        quality = report["image_quality"]

        tampering = report["tampering"]

        self.cursor.execute("""

        INSERT INTO verifications(

            name,

            dob,

            gender,

            aadhaar,

            confidence,

            similarity,

            quality,

            tampering,

            status,

            report

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

        """,

        (

            aadhaar.get("name"),

            aadhaar.get("dob"),

            aadhaar.get("gender"),

            aadhaar.get("aadhaar_number"),

            report["confidence"],

            face["similarity"],

            quality["status"],

            str(tampering["tampered"]),

            report["status"],

            report["pdf_report"]

        )

        )

        self.conn.commit()

    ####################################################

    def all(self):

        self.cursor.execute("""

        SELECT *

        FROM verifications

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    ####################################################

    def delete(self, id):

        self.cursor.execute(

            "DELETE FROM verifications WHERE id=?",

            (id,)

        )

        self.conn.commit()

    ####################################################

    def close(self):

        self.conn.close()