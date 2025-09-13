import sys
import sqlite3
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.datatypes.player import Player


dir = os.path.dirname(__file__)
filename = os.path.join(dir, "../database.db")


def add_student(student: Player) -> int | None:
    try:
        with sqlite3.connect(filename) as conn:
            sql = "INSERT INTO students(age) VALUES(?)"
            cur = conn.cursor()
            cur.execute(sql, (student.Age,))
            conn.commit()
            return cur.lastrowid
    except sqlite3.Error as e:
        print(e)
        return 0


def select_student():
    try:
        with sqlite3.connect(filename) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, age FROM students")
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except sqlite3.Error as e:
        print(e)


def select_max_id() -> int:
    try:
        with sqlite3.connect(filename) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM students")
            row = cur.fetchone()

            if row[0] is None:
                return 0

            return row[0]
    except sqlite3.Error as e:
        print(e)
        return 0


def select_students() -> list[Player]:
    try:
        with sqlite3.connect(filename) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, age FROM students ORDER BY RANDOM ()")
            
            users_list = []
            
            for u in cur.fetchall():
                p = Player(u[0], None, u[1], None, None, True)
                users_list.append(p)
                
            return users_list
    except sqlite3.Error as e:
        print(e)


def main():
    student = Player(1, "Teste", 22)
    student_id = add_student(student)
    print(f"Created a student with the id {student_id}")

    select_student()
    select_max_id()
    print(select_students())


if __name__ == "__main__":
    main()
