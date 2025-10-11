from typing import List, Optional, Dict, Any
import sqlite3
from app.core.db import get_connection, generate_next_id
from app.items.models import RegisteredStudent, EnrolledStudent

# Custom exceptions
class DeletionBlockedError(Exception):
    pass

class RepositoryError(Exception):
    pass

class RegisteredStudentRepo:
    """Repository for registered students CRUD operations"""

    @classmethod
    def add(cls, student: RegisteredStudent) -> str:
        # Add a new student
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                new_id = student.id or generate_next_id("registered_students")
                cur.execute("""
                    INSERT INTO registered_students
                    (id, first_name, middle_name, last_name, gender, birth_date, age, contact, guardian_name, guardian_contact)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_id,
                    student.first_name.strip(),
                    student.middle_name.strip() if student.middle_name else None,
                    student.last_name.strip(),
                    student.gender.strip(),
                    student.birth_date,
                    student.age,
                    student.contact.strip() if student.contact else None,
                    student.guardian_name.strip() if student.guardian_name else None,
                    student.guardian_contact.strip() if student.guardian_contact else None
                ))
                conn.commit()
                return new_id
        except sqlite3.IntegrityError as e:
            raise RepositoryError("A database constraint failed (possibly duplicate ID).") from e
        except sqlite3.Error as e:
            raise RepositoryError(f"Database error while adding student: {e}") from e

    @classmethod
    def get_all(cls) -> List[RegisteredStudent]:
        # Fetch all registered students
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM registered_students ORDER BY id")
            rows = cur.fetchall()
            return [RegisteredStudent(**dict(r)) for r in rows]

    @classmethod
    def get(cls, sid: str) -> Optional[RegisteredStudent]:
        # Get a student by ID
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM registered_students WHERE id=?", (sid,))
            row = cur.fetchone()
            return RegisteredStudent(**dict(row)) if row else None

    @classmethod
    def update(cls, sid: str, student: RegisteredStudent) -> bool:
        # Update student info
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE registered_students SET
                    first_name=?, middle_name=?, last_name=?, gender=?,
                    birth_date=?, age=?, contact=?, guardian_name=?, guardian_contact=?
                    WHERE id=?
                """, (
                    student.first_name.strip(),
                    student.middle_name.strip() if student.middle_name else None,
                    student.last_name.strip(),
                    student.gender.strip(),
                    student.birth_date,
                    student.age,
                    student.contact.strip() if student.contact else None,
                    student.guardian_name.strip() if student.guardian_name else None,
                    student.guardian_contact.strip() if student.guardian_contact else None,
                    sid
                ))
                conn.commit()
                return cur.rowcount > 0
        except sqlite3.Error as e:
            raise RepositoryError(f"Database error while updating student: {e}") from e

    @classmethod
    def delete(cls, sid: str) -> bool:
        # Delete student if not enrolled
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM enrolled_students WHERE id=? LIMIT 1", (sid,))
            if cur.fetchone():
                raise DeletionBlockedError("Student is currently enrolled.")
            cur.execute("DELETE FROM registered_students WHERE id=?", (sid,))
            conn.commit()
            return cur.rowcount > 0

    @classmethod
    def search(cls, query: str) -> List[RegisteredStudent]:
        # Search students by ID, name, contact, or guardian
        like = f"%{query}%"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, first_name, middle_name, last_name, gender, birth_date, age,
                       contact, guardian_name, guardian_contact
                FROM registered_students
                WHERE id LIKE ? OR first_name LIKE ? OR middle_name LIKE ? OR last_name LIKE ?
                      OR contact LIKE ? OR guardian_name LIKE ? OR guardian_contact LIKE ?
                ORDER BY id
            """, (like, like, like, like, like, like, like))
            rows = cur.fetchall()
            return [RegisteredStudent(**dict(r)) for r in rows]

# ------------------- Enrolled Students -------------------
class EnrolledStudentRepo:
    """Repository for enrolled students operations"""

    @staticmethod
    def enroll(enrollment: EnrolledStudent) -> str:
        # Enroll a registered student
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM registered_students WHERE id=? LIMIT 1", (enrollment.id,))
            if not cur.fetchone():
                raise RepositoryError(f"Registered student id {enrollment.id} not found.")
            cur.execute("INSERT INTO enrolled_students (id, grade_level, strand) VALUES (?, ?, ?)",
                        (enrollment.id, enrollment.grade_level, enrollment.strand))
            conn.commit()
            return enrollment.id

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        # List all enrolled students with names
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT e.id, r.first_name, r.middle_name, r.last_name,
                       e.grade_level, e.strand
                FROM enrolled_students e
                JOIN registered_students r ON e.id = r.id
                ORDER BY e.id
            """)
            rows = cur.fetchall()
            result = []
            for row in rows:
                full_name = f"{row['first_name']} {row['middle_name'] or ''} {row['last_name']}".replace("  ", " ").strip()
                result.append({
                    "id": row["id"],
                    "full_name": full_name,
                    "grade_level": row["grade_level"],
                    "strand": row["strand"]
                })
            return result

    @staticmethod
    def update(eid: str, grade: str, strand: str) -> bool:
        # Update grade or strand
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE enrolled_students SET grade_level=?, strand=? WHERE id=?", (grade, strand, eid))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def delete(eid: str) -> bool:
        # Delete enrollment
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM enrolled_students WHERE id=?", (eid,))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def filter(grade_level: str = None, strand: str = None):
        # Filter enrolled students by grade and/or strand
        with get_connection() as conn:
            cur = conn.cursor()
            sql = """
                SELECT e.id, r.first_name, r.middle_name, r.last_name,
                       e.grade_level, e.strand
                FROM enrolled_students e
                JOIN registered_students r ON e.id = r.id
            """
            params = []
            conditions = []

            if grade_level and grade_level != "All":
                conditions.append("e.grade_level = ?")
                params.append(grade_level)
            if strand and strand != "All":
                conditions.append("e.strand = ?")
                params.append(strand)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            sql += " ORDER BY e.id"
            cur.execute(sql, params)
            return cur.fetchall()
