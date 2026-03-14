import sqlite3
import os

DB_PATH = r"C:\ContabilitateAuto\data\contabilitate.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initializeaza_baza_de_date():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS societati (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        cui             TEXT UNIQUE NOT NULL,
        denumire        TEXT NOT NULL,
        folder_spv      TEXT,
        folder_declaratii TEXT,
        status_anaf     TEXT DEFAULT 'Activa',
        tva_la_incasare INTEGER DEFAULT 0,
        data_ultima_verificare DATETIME,
        activa          INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS vector_fiscal (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER NOT NULL REFERENCES societati(id),
        semnificatie    TEXT NOT NULL,
        declaratie      TEXT,
        periodicitate   TEXT,
        data_inceput    DATE,
        data_sfarsit    DATE,
        versiune        INTEGER DEFAULT 1,
        sursa_pdf       TEXT,
        data_import     DATETIME DEFAULT CURRENT_TIMESTAMP,
        aprobat         INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS vector_istoric (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER NOT NULL REFERENCES societati(id),
        semnificatie    TEXT,
        modificare_tip  TEXT,
        valoare_veche   TEXT,
        valoare_noua    TEXT,
        data_modificare DATETIME DEFAULT CURRENT_TIMESTAMP,
        aprobat_de_user INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS declaratii (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER NOT NULL REFERENCES societati(id),
        tip_declaratie  TEXT NOT NULL,
        perioada        TEXT NOT NULL,
        index_incarcare TEXT,
        status          TEXT DEFAULT 'Depusa',
        suma_declarata  REAL,
        cale_fisier     TEXT,
        data_depunere   DATE,
        mesaj_recipisa  TEXT,
        data_import     DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tipuri_datorii (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        cod_intern      TEXT UNIQUE,
        denumire_standard TEXT,
        declaratie_asociata TEXT
    );

    CREATE TABLE IF NOT EXISTS fisa_platitor (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER NOT NULL REFERENCES societati(id),
        denumire_datorie TEXT NOT NULL,
        tip_datorie_id  INTEGER REFERENCES tipuri_datorii(id),
        suma_datorata   REAL DEFAULT 0,
        suma_achitata   REAL DEFAULT 0,
        sold            REAL DEFAULT 0,
        data_fisa       DATE,
        cale_fisier     TEXT,
        data_import     DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS mapping_datorii (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        text_din_pdf    TEXT UNIQUE NOT NULL,
        tip_datorie_id  INTEGER REFERENCES tipuri_datorii(id),
        adaugat_de_user INTEGER DEFAULT 1,
        data_adaugare   DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS documente_diverse (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER REFERENCES societati(id),
        tip_document    TEXT,
        rezumat         TEXT,
        cale_fisier_original TEXT,
        cale_fisier_redenumit TEXT,
        trimis_telegram INTEGER DEFAULT 0,
        data_identificare DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS termene (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER NOT NULL REFERENCES societati(id),
        tip_declaratie  TEXT NOT NULL,
        perioada        TEXT NOT NULL,
        data_scadenta   DATE NOT NULL,
        status          TEXT DEFAULT 'In_asteptare',
        declaratie_id   INTEGER REFERENCES declaratii(id)
    );

    CREATE TABLE IF NOT EXISTS notificari (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        societate_id    INTEGER REFERENCES societati(id),
        tip             TEXT,
        mesaj           TEXT,
        citita          INTEGER DEFAULT 0,
        data_trimitere  DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    """)

    conn.commit()
    conn.close()
    print("✅ Baza de date a fost creată cu succes!")

if __name__ == "__main__":
    initializeaza_baza_de_date()
