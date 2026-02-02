from datetime import datetime

_scores: list[dict] = []

def add_score(score: tuple[int, int]) -> int:

    new_id = len(_scores) + 1
    score_entry = {
        "id": new_id,
        "score": score[0],
        "student_id": score[1],
        "date_match": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _scores.append(score_entry)
    return new_id

def get_scores() -> list[dict]:
    
    return list(_scores)

def reset_scores():
  
    _scores.clear()


if __name__ == "__main__":
    score_id = add_score((3, 1))
    print(f"Created a score with the id {score_id}")
    print(get_scores())
