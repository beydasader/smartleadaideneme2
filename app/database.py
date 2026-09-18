import sqlite3
from flask import current_app


def get_db():
    database_url = current_app.config["DATABASE_URL"]

    connection = sqlite3.connect(database_url)
    connection.row_factory = sqlite3.Row

    return connection


def init_db(app):
    with app.app_context():

        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()
        db.close()


def lead_ekle(isim, telefon, mesaj):
    db = get_db()

    db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    db.commit()
    db.close()


def tum_leadler():
    db = get_db()

    leads = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

    db.close()

    return leads