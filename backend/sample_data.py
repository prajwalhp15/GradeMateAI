from .models import create_assignment
import datetime

if __name__ == "__main__":
    tests = [
        {"input": "2\n3\n", "expected": "5\n"},
        {"input": "10\n20\n", "expected": "30\n"}
    ]
    deadline = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()
    aid = create_assignment("Add two numbers", "Read two ints and print their sum", tests, deadline)
    print("Created assignment id:", aid)
