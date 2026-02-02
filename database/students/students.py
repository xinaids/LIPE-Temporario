from src.datatypes.player import Player


_students: list[Player] = []

def add_student(student: Player) -> int:
    
    new_id = len(_students) + 1
    student.Id = new_id
    _students.append(student)
    return new_id

def select_student():
   
    for s in _students:
        print(s)

def select_max_id() -> int:
    
    return len(_students)

def select_students() -> list[Player]:

    return list(_students) 

def reset_students():
   
    _students.clear()


if __name__ == "__main__":
    s1 = Player(0, "Teste1")
    s2 = Player(0, "Teste2")
    add_student(s1)
    add_student(s2)
    select_student()
    print(select_max_id())
    print(select_students())
