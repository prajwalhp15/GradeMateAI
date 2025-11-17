const API_BASE = "http://localhost:5000/api";

const runBtn = document.getElementById("runBtn");
const submitBtn = document.getElementById("submitBtn");
const codeEditor = document.getElementById("codeEditor");
const stdin = document.getElementById("stdin");
const output = document.getElementById("output");
const assignmentIdInput = document.getElementById("assignmentId");
const studentEmailInput = document.getElementById("studentEmail");
const resultSection = document.getElementById("resultSection");
const resultJson = document.getElementById("resultJson");

runBtn.addEventListener("click", async () => {
  output.textContent = "Running...";
  try {
    const payload = {
      student_email: studentEmailInput.value || "demo@example.com",
      assignment_id: assignmentIdInput.value || "",
      language: "python",
      code: codeEditor.value,
      run: true,
      stdin: stdin.value || ""
    };
    // We'll call the submit endpoint for run as well but with run-only flag
    const res = await fetch(API_BASE + "/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const j = await res.json();
    if (j.ok) {
      // show first test output as run output (for quick demo)
      const details = j.result.test_details || [];
      let txt = `Score: ${j.result.score}%\n\n`;
      details.forEach(d => {
        txt += `Test ${d.test_number}: ${d.passed ? "PASS" : "FAIL"}\n`;
        txt += `Output:\n${d.output}\n`;
        if (d.reason) txt += `Reason: ${d.reason}\n`;
        txt += `---\n`;
      });
      output.textContent = txt;
      resultSection.style.display = "block";
      resultJson.innerText = JSON.stringify(j, null, 2);
    } else {
      output.textContent = "Error: " + (j.error || JSON.stringify(j));
    }
  } catch (e) {
    output.textContent = "Error: " + e.toString();
  }
});

submitBtn.addEventListener("click", async () => {
  output.textContent = "Submitting...";
  try {
    const payload = {
      student_email: studentEmailInput.value || "demo@example.com",
      assignment_id: assignmentIdInput.value,
      language: "python",
      code: codeEditor.value
    };
    const res = await fetch(API_BASE + "/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const j = await res.json();
    if (j.ok) {
      output.textContent = `Submitted. Score: ${j.result.score}%. Plagiarism: ${j.plagiarism.max_similarity.toFixed(2)}% ${j.plagiarism.flagged ? "(FLAGGED)" : ""}`;
      resultSection.style.display = "block";
      resultJson.innerText = JSON.stringify(j, null, 2);
    } else {
      output.textContent = "Error: " + (j.error || JSON.stringify(j));
    }
  } catch (e) {
    output.textContent = "Error: " + e.toString();
  }
});
