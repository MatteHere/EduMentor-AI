import sqlite3
from pathlib import Path


DB_FOLDER = Path("data/database")
DB_PATH = DB_FOLDER / "edumentor.db"


def get_connection():
    DB_FOLDER.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workspaces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        university TEXT,
        stream TEXT,
        semester TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workspace_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_id INTEGER,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        extracted_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (unit_id) REFERENCES units(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_outputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        mode TEXT NOT NULL,
        output_text TEXT NOT NULL,
        provider TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id),
        UNIQUE(document_id, mode)
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# Workspace CRUD
# -------------------------

def create_workspace(name, university, stream, semester):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO workspaces (name, university, stream, semester)
        VALUES (?, ?, ?, ?)
        """,
        (name, university, stream, semester)
    )

    conn.commit()
    workspace_id = cursor.lastrowid
    conn.close()
    return workspace_id


def get_workspaces():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, university, stream, semester, created_at
    FROM workspaces
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_workspace(workspace_id, name, university, stream, semester):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE workspaces
        SET name = ?, university = ?, stream = ?, semester = ?
        WHERE id = ?
        """,
        (name, university, stream, semester, workspace_id)
    )

    conn.commit()
    conn.close()


def delete_workspace(workspace_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM ai_outputs
        WHERE document_id IN (
            SELECT documents.id
            FROM documents
            JOIN units ON documents.unit_id = units.id
            JOIN subjects ON units.subject_id = subjects.id
            WHERE subjects.workspace_id = ?
        )
    """, (workspace_id,))

    cursor.execute("""
        DELETE FROM documents
        WHERE unit_id IN (
            SELECT units.id
            FROM units
            JOIN subjects ON units.subject_id = subjects.id
            WHERE subjects.workspace_id = ?
        )
    """, (workspace_id,))

    cursor.execute("""
        DELETE FROM units
        WHERE subject_id IN (
            SELECT id FROM subjects WHERE workspace_id = ?
        )
    """, (workspace_id,))

    cursor.execute(
        "DELETE FROM subjects WHERE workspace_id = ?",
        (workspace_id,)
    )

    cursor.execute(
        "DELETE FROM workspaces WHERE id = ?",
        (workspace_id,)
    )

    conn.commit()
    conn.close()


# -------------------------
# Subject CRUD
# -------------------------

def create_subject(workspace_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO subjects (workspace_id, name)
        VALUES (?, ?)
        """,
        (workspace_id, name)
    )

    conn.commit()
    subject_id = cursor.lastrowid
    conn.close()
    return subject_id


def get_subjects(workspace_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, created_at
        FROM subjects
        WHERE workspace_id = ?
        ORDER BY created_at DESC
        """,
        (workspace_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_subject(subject_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE subjects
        SET name = ?
        WHERE id = ?
        """,
        (name, subject_id)
    )

    conn.commit()
    conn.close()


def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM ai_outputs
        WHERE document_id IN (
            SELECT documents.id
            FROM documents
            JOIN units ON documents.unit_id = units.id
            WHERE units.subject_id = ?
        )
    """, (subject_id,))

    cursor.execute("""
        DELETE FROM documents
        WHERE unit_id IN (
            SELECT id FROM units WHERE subject_id = ?
        )
    """, (subject_id,))

    cursor.execute(
        "DELETE FROM units WHERE subject_id = ?",
        (subject_id,)
    )

    cursor.execute(
        "DELETE FROM subjects WHERE id = ?",
        (subject_id,)
    )

    conn.commit()
    conn.close()


# -------------------------
# Unit CRUD
# -------------------------

def create_unit(subject_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO units (subject_id, name)
        VALUES (?, ?)
        """,
        (subject_id, name)
    )

    conn.commit()
    unit_id = cursor.lastrowid
    conn.close()
    return unit_id


def get_units(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, created_at
        FROM units
        WHERE subject_id = ?
        ORDER BY created_at DESC
        """,
        (subject_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def update_unit(unit_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE units
        SET name = ?
        WHERE id = ?
        """,
        (name, unit_id)
    )

    conn.commit()
    conn.close()


def delete_unit(unit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM ai_outputs
        WHERE document_id IN (
            SELECT id FROM documents WHERE unit_id = ?
        )
    """, (unit_id,))

    cursor.execute(
        "DELETE FROM documents WHERE unit_id = ?",
        (unit_id,)
    )

    cursor.execute(
        "DELETE FROM units WHERE id = ?",
        (unit_id,)
    )

    conn.commit()
    conn.close()


# -------------------------
# Document CRUD
# -------------------------

def save_document(unit_id, file_name, file_path, extracted_text):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO documents (unit_id, file_name, file_path, extracted_text)
        VALUES (?, ?, ?, ?)
        """,
        (unit_id, file_name, str(file_path), extracted_text)
    )

    conn.commit()
    document_id = cursor.lastrowid
    conn.close()
    return document_id


def get_documents(unit_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if unit_id:
        cursor.execute(
            """
            SELECT id, file_name, file_path, created_at
            FROM documents
            WHERE unit_id = ?
            ORDER BY created_at DESC
            """,
            (unit_id,)
        )
    else:
        cursor.execute("""
        SELECT id, file_name, file_path, created_at
        FROM documents
        ORDER BY created_at DESC
        """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_document_by_id(document_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, file_name, file_path, extracted_text, created_at
        FROM documents
        WHERE id = ?
        """,
        (document_id,)
    )

    row = cursor.fetchone()
    conn.close()
    return row


def update_document_name(document_id, file_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE documents
        SET file_name = ?
        WHERE id = ?
        """,
        (file_name, document_id)
    )

    conn.commit()
    conn.close()


def delete_document(document_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM ai_outputs WHERE document_id = ?",
        (document_id,)
    )

    cursor.execute(
        "DELETE FROM documents WHERE id = ?",
        (document_id,)
    )

    conn.commit()
    conn.close()


# -------------------------
# AI Output Cache
# -------------------------

def save_ai_output(document_id, mode, output_text, provider):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO ai_outputs (document_id, mode, output_text, provider)
        VALUES (?, ?, ?, ?)
        """,
        (document_id, mode, output_text, provider)
    )

    conn.commit()
    conn.close()


def get_ai_output(document_id, mode):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT output_text, provider, created_at
        FROM ai_outputs
        WHERE document_id = ? AND mode = ?
        """,
        (document_id, mode)
    )

    row = cursor.fetchone()
    conn.close()
    return row