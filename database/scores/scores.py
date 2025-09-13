import sqlite3
from pathlib import Path
import os
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../database.db')

def add_score(score)->int | None:
    try:
        with sqlite3.connect(filename) as conn:
            sql = "INSERT INTO scores(score, student_id, date_match) VALUES(?, ?, datetime())"
            cur = conn.cursor()
            cur.execute(sql, (score))
            conn.commit()
            return cur.lastrowid
    except sqlite3.Error as e:
        print(e)
        return 0


def main():
    score = (3, 1)
    score_id = add_score(score)
    print(f"Created a score with the id {score_id}")

if __name__ == "__main__":
    main()
