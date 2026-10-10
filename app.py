
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "talentflow.db"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TalentFlow AI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 750px;
            margin: 40px auto;
            padding: 20px;
            background: #f4f7fb;
            color: #222;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        h1 { color: #2457a7; }
        input, textarea, button {
            display: block;
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            margin: 12px 0;
        }
        button {
            background: #2457a7;
            color: white;
            border: 0;
            border-radius: 6px;
            cursor: pointer;
        }
        #result { font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>TalentFlow AI</h1>
        <p>Recruitment and Talent Management Platform</p>
        <h2>Candidate Application</h2>

        <form id="application">
            <input name="name" placeholder="Candidate name"
                   maxlength="100" required>
            <input name="email" type="email" placeholder="Email address"
                   maxlength="254" required>
            <input name="job" placeholder="Job title"
                   maxlength="150" required>
            <textarea name="skills" placeholder="Describe your skills"
                      maxlength="3000" required></textarea>
            <button type="submit">Submit Application</button>
        </form>

        <p id="result" role="status"></p>
        <small>Learning demo. Use fictional candidate data.</small>
    </div>

    <script>
        const form = document.getElementById("application");
        const result = document.getElementById("result");

        form.addEventListener("submit", async function(event) {
            event.preventDefault();
            result.textContent = "Saving application...";

            const data = Object.fromEntries(new FormData(form).entries());

            try {
                const response = await fetch("/apply", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });

                const answer = await response.json();

                if (!response.ok) {
                    throw new Error(answer.error || "Submission failed.");
                }

                result.textContent =
                    "Application saved successfully. ID: " + answer.id;
                form.reset();
            } catch (error) {
                result.textContent = "Error: " + error.message;
            }
        });
    </script>
</body>
</html>
"""


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                job TEXT NOT NULL,
                skills TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Page not found")
            return

        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/apply":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16000:
                self.send_json(400, {"error": "Invalid request size"})
                return

            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Invalid application data")

            name = str(payload.get("name", "")).strip()
            email = str(payload.get("email", "")).strip()
            job = str(payload.get("job", "")).strip()
            skills = str(payload.get("skills", "")).strip()

            if not all([name, email, job, skills]):
                self.send_json(400, {"error": "Please complete all fields"})
                return

            if (len(name) > 100 or len(email) > 254 or
                    len(job) > 150 or len(skills) > 3000 or
                    "@" not in email):
                self.send_json(400, {"error": "Please check your input"})
                return

            with sqlite3.connect(DB_PATH) as connection:
                cursor = connection.execute(
                    """INSERT INTO applications (name, email, job, skills)
                       VALUES (?, ?, ?, ?)""",
                    (name, email, job, skills)
                )
                application_id = cursor.lastrowid

            self.send_json(201, {
                "message": "Application saved",
                "id": application_id
            })

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "Invalid application data"})
        except sqlite3.Error:
            self.send_json(500, {"error": "Database error; application not saved"})
        except Exception:
            self.send_json(500, {"error": "Unexpected server error"})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    initialize_database()
    HTTPServer(("0.0.0.0", 8000), Handler)
    print("TalentFlow AI running at http://127.0.0.1:8000")
    print(f"SQLite database: {DB_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
