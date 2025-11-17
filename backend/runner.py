import subprocess, tempfile, os, sys, shutil
from .config import RUN_TIMEOUT, MAX_OUTPUT_SIZE

def run_python_code(source_code: str, stdin_data: str = "", timeout: int = RUN_TIMEOUT):
    """
    Runs Python code in a temporary dir with timeout.
    Returns (returncode, stdout, stderr).
    WARNING: not secure for untrusted code. Use proper sandbox in production.
    """
    tmpdir = tempfile.mkdtemp(prefix="ai_grader_")
    fname = os.path.join(tmpdir, "solution.py")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(source_code)

    try:
        proc = subprocess.run(
            [sys.executable, fname],
            input=stdin_data.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=tmpdir
        )
        stdout = proc.stdout.decode(errors="replace")
        stderr = proc.stderr.decode(errors="replace")
        if len(stdout) > MAX_OUTPUT_SIZE:
            stdout = stdout[:MAX_OUTPUT_SIZE] + "\n...output truncated..."
        if len(stderr) > MAX_OUTPUT_SIZE:
            stderr = stderr[:MAX_OUTPUT_SIZE] + "\n...error truncated..."
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired as e:
        return -1, "", f"TimeoutExpired: execution exceeded {timeout} seconds"
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass
