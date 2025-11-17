from flask import Flask, request, jsonify
from flask_cors import CORS
from .models import create_user, find_user_by_email, verify_password, create_assignment, get_assignment, save_submission
from .grader import run_tests_on_submission
from .plagiarism import similarity, is_plagiarized
from .mailer import send_email
from .db import submissions, plag_reports, assignments, users
from .config import RUN_TIMEOUT
import datetime
import json
from bson import ObjectId
import bcrypt

app = Flask(__name__)
CORS(app)

# --- Auth endpoints (very basic for demo) ---
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "student")
    extra = data.get("extra", {})
    if find_user_by_email(email):
        return jsonify({"ok": False, "error": "User exists"}), 400
    _id = create_user(email, username, password, role=role, extra=extra)
    return jsonify({"ok": True, "id": str(_id)})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    u = find_user_by_email(email)
    if not u:
        return jsonify({"ok": False, "error": "User not found"}), 404
    if bcrypt.checkpw(password.encode(), u["password"]):
        # return simple user info (no JWT in this demo)
        return jsonify({"ok": True, "user": {"email": u["email"], "username": u["username"], "role": u["role"]}})
    return jsonify({"ok": False, "error": "Bad credentials"}), 401

# --- Assignments (lecturer) ---
@app.route("/api/assignments", methods=["POST"])
def create_assign():
    data = request.json
    title = data.get("title")
    description = data.get("description", "")
    tests = data.get("tests", [])
    deadline = data.get("deadline")  # expect ISO string
    deadline_dt = datetime.datetime.fromisoformat(deadline) if deadline else None
    aid = create_assignment(title, description, tests, deadline_dt)
    # Optionally email all students (skipped here)
    return jsonify({"ok": True, "assignment_id": str(aid)})

@app.route("/api/assignments/<aid>", methods=["GET"])
def get_assign(aid):
    a = get_assignment(aid)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    # convert ObjectId and datetime for JSON
    a["_id"] = str(a["_id"])
    if a.get("deadline"):
        a["deadline"] = a["deadline"].isoformat()
    return jsonify({"ok": True, "assignment": a})

# --- Submit code endpoint ---
@app.route("/api/submit", methods=["POST"])
def submit_code():
    """
    Expects JSON:
    {
      "student_email": "...",
      "assignment_id": "...",
      "language": "python",
      "code": "print(input())"
    }
    """
    data = request.json
    student_email = data.get("student_email")
    assignment_id = data.get("assignment_id")
    language = data.get("language", "python")
    code = data.get("code", "")

    # Basic validation
    a = get_assignment(assignment_id)
    if not a:
        return jsonify({"ok": False, "error": "Assignment not found"}), 404

    # 1) AI grading
    result = run_tests_on_submission(code, a.get("tests", []))

    # 2) Plagiarism check: compare with previous submissions for same assignment
    plag_scores = []
    for prev in submissions.find({"assignment_id": a["_id"]}):
        prev_code = prev.get("code", "")
        score = similarity(code, prev_code)
        plag_scores.append({"other_submission_id": str(prev["_id"]), "score": score})
    # Find max similarity
    max_sim = max([p["score"] for p in plag_scores], default=0.0)
    flagged = is_plagiarized(max_sim)

    # Save submission
    sub_id = save_submission(student_email, assignment_id, language, code, result)

    # Save plag report if flagged or keep record
    plag_doc = {
        "submission_id": sub_id,
        "student_email": student_email,
        "assignment_id": a["_id"],
        "max_similarity": max_sim,
        "flagged": flagged,
        "details": plag_scores,
        "created_at": datetime.datetime.utcnow()
    }
    plag_reports.insert_one(plag_doc)

    # Send email notification to student
    try:
        subject = f"Submission received: {a['title']}"
        content = f"Your submission for '{a['title']}' has been received.\nScore: {result['score']}%\nPlagiarism similarity: {max_sim:.2f}%\n"
        send_email(student_email, subject, content)
    except Exception as e:
        print("Email failed:", e)

    return jsonify({
        "ok": True,
        "submission_id": str(sub_id),
        "result": result,
        "plagiarism": {"max_similarity": max_sim, "flagged": flagged}
    })

# --- Search / reports (simplified) ---
@app.route("/api/submissions/<assignment_id>", methods=["GET"])
def list_submissions_for_assignment(assignment_id):
    a = get_assignment(assignment_id)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    docs = []
    for s in submissions.find({"assignment_id": a["_id"]}):
        docs.append({
            "_id": str(s["_id"]),
            "student_email": s["student_email"],
            "score": s["result"]["score"],
            "created_at": s["created_at"].isoformat()
        })
    return jsonify({"ok": True, "submissions": docs})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
