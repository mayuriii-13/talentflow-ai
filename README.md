# 🚀 TalentFlow AI — Recruitment & Talent Management Platform

A recruitment management demo built with **Python, SQLite, HTML, CSS, and JavaScript**. TalentFlow AI provides a local web interface for managing candidate applications and job postings, with skill-based matching to compare candidate skills against job requirements.

This repository contains my own implementation and modifications, along with selected starting materials adapted from Davine Technologies project materials provided during my internship.

## ✨ Features

- 📊 **Dashboard** — View summary counts and recent application activity.
- 📝 **Candidate Management** — Save candidate details, including name, email, applied-for role, and skills.
- 🔍 **Application Management** — View, search, and filter saved applications.
- 💼 **Job Management** — Create, view, edit, and delete job postings with required skills.
- 🤖 **Skill-Based Candidate Matching** — Compare candidate skills against a selected job's requirements.
- 📈 **Match Explanation** — Display matched skills, missing skills, and the calculated match percentage.
- 🗄️ **SQLite Database** — Store candidate applications and job records locally.
- 🐳 **Docker Support** — Optional container testing, subject to verification of the Docker configuration.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python 3 |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Matching Logic | Rule-based skill matching |
| Containerization | Docker (optional) |
| Version Control | Git & GitHub |

## 🏗️ Architecture

```text
👤 Candidate / Recruiter
          |
          v
🌐 Web Browser
          |
          v
🖥️ TalentFlow AI Web Interface
          |
          v
⚙️ Python HTTP Server
          |
          +--------------------+
          |                    |
          v                    v
📝 Candidate Applications   💼 Job Postings
          |                    |
          +---------+----------+
                    |
                    v
             🗄️ SQLite Database
                    |
                    v
          🤖 Skill Matching Logic
                    |
                    v
       📈 Matched Skills & Missing Skills
                    |
                    v
             📊 Match Percentage
```

*This diagram represents the application's logical workflow; it does not imply that every component is deployed on AWS.*

## 🤖 How Candidate Matching Works

The current matching feature uses **rule-based skill matching**. It is not a trained machine-learning model or a generative-AI candidate-ranking system.

The matching process:

1. 📋 Reads the required skills for a selected job.
2. 🔎 Compares them with the candidate's saved skills.
3. ✅ Identifies matched skills.
4. ❌ Identifies missing skills.
5. 📊 Calculates a match percentage.

**Formula:**

`Match Score = (Matched Required Skills / Total Required Skills) × 100`

**Example:**

Suppose a Cloud Engineer job requires AWS, Linux, and Networking. A candidate has AWS and Linux skills.

- 📌 Total required skills: 3
- ✅ Matched skills: 2
- ❌ Missing skills: Networking
- 📈 Match score: 2 / 3 × 100 = **67%**

The score represents skill overlap only. It does not independently measure experience, proficiency, or overall candidate suitability.

## 💻 How to Run the Project Locally

### 📋 Prerequisites

- Python 3
- A web browser
- Git (optional)

### 🚀 Steps

**1. Clone the repository**

```bash
git clone https://github.com/mayuriii-13/talentflow-ai.git
cd talentflow-ai
```

**2. Start the application**

From the repository root, run:

```bash
python app/app.py
```

**3. Open the application**

Visit:

```text
http://127.0.0.1:8000
```

Keep the terminal open while using the application.

> 💡 Verify the application path and startup command against the files in your repository. The application uses a local SQLite database; use fictional candidate information for testing.

## 🐳 Docker (Optional)

If your repository contains a working Dockerfile in the current directory, build the image with:

```bash
docker build -t talentflow-ai .
```

Run the container:

```bash
docker run --rm -p 8000:8000 talentflow-ai
```

Then visit:

```text
http://127.0.0.1:8000
```

> ⚠️ Confirm the Dockerfile location, application startup command, and database path before using these commands. Database persistence must be configured separately if records need to survive container removal.

## 🧪 Testing Checklist

- ✅ Start the application and open the local URL.
- ✅ Add a fictional candidate and verify the saved record.
- ✅ Create a job posting with required skills.
- ✅ Edit and delete a test job posting.
- ✅ Run candidate matching and review matched and missing skills.
- ✅ Verify the calculated match percentage.
- ✅ Restart the application and check whether records persist in SQLite.
- 🐳 If using Docker, test the image build, application access, and database persistence separately.

*Mark each item complete only after verifying it against the current version of your repository.*

## 📌 Current Project Status

**Status: Recruitment management demo with skill-based matching**

### ✅ Implemented in the modified local version

- Candidate and application management workflows.
- Job posting management.
- SQLite-based local data storage.
- Rule-based skill comparison.
- Matched skills, missing skills, and explainable match percentage.

### 🚧 Planned Improvements

- 🤖 More advanced AI-assisted candidate matching and ranking.
- ☁️ Verified AWS deployment and deployment automation.
- 🗄️ Managed database integration, such as Amazon RDS.
- 🔐 Authentication, access control, and HTTPS.
- 📈 Improved monitoring, logging, and error handling.
- 📦 Verified CI/CD integration and container registry workflow.
- 📊 Further scalability and production-readiness improvements.

*Note: Planned improvements are not claimed as completed features. AWS EC2 deployment, GitHub Actions, Docker Hub publishing, and AWS Systems Manager access should be listed as completed only if you have verified those workflows in the current repository and environment.*

## 🔐 Security Considerations

- 🔒 Do not expose application ports publicly unless required and properly secured.
- 🔑 Never commit AWS credentials, access keys, or Docker Hub tokens to GitHub.
- 🛡️ Configure appropriate access controls before handling real candidate information.
- 🧪 Use fictional candidate data during development and testing.
- ⚠️ This demo does not claim production-grade security or compliance.

## 🎯 Learning Objectives

This project supports practical learning in:

- 🐍 Python web application development.
- 🗄️ SQLite database integration.
- 🌐 Frontend and backend integration.
- 🐳 Docker containerization fundamentals.
- ☁️ AWS cloud deployment concepts.
- 🔄 Git and GitHub workflows.
- 🤖 Rule-based skill matching and result explanation.
- 🧪 Application testing and troubleshooting.

## 👩‍💻 Author

**Mayuri Ambare**

- 🐙 GitHub: [@mayuriii-13](https://github.com/mayuriii-13)
- 📂 Project Repository: [TalentFlow AI](https://github.com/mayuriii-13/talentflow-ai)

## 🙌 Attribution

This repository contains my own implementation and modifications, together with selected starting materials adapted from the Davine Technologies project materials provided during my internship.

This README describes the modified version of the project and does not claim that every feature from the original materials or proposed architecture has been implemented or deployed.

---

⭐ If you find this project useful, feel free to explore the repository!

