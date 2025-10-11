import sqlite3

DB_NAME = "students.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()

        #Table for registered students
        cur.execute("""
        CREATE TABLE IF NOT EXISTS registered_students (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT NOT NULL,
            gender TEXT,
            birth_date TEXT,
            age INTEGER,
            contact TEXT,
            guardian_name TEXT,
            guardian_contact TEXT
        )
        """)

        #Table for enrolled students
        cur.execute("""
        CREATE TABLE IF NOT EXISTS enrolled_students (
            id TEXT PRIMARY KEY,
            grade_level TEXT NOT NULL,
            strand TEXT NOT NULL,
            FOREIGN KEY(id) REFERENCES registered_students(id) ON DELETE CASCADE
        )
        """)
        conn.commit()

#Generator for id and iterator for next id
def generate_next_id(table_name: str) -> str:

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()

        if row and row["id"]:
            last_id = str(row["id"])

            if last_id.startswith("S") and last_id[2:].isdigit():
                next_num = int(last_id[2:]) + 1
            else:
                next_num = 1
        else:
            next_num = 1


        new_id = f"S{next_num:06d}"
        return new_id
