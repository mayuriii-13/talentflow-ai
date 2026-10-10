# 🚀 TalentFlow AI — Recruitment & Talent Management Platform

A cloud-hosted recruitment application demo built with **Python, SQLite, Docker, and AWS**. TalentFlow AI allows candidates to submit their applications through a simple web form, with application details stored in a SQLite database.

## ✨ Features

- 📝 **Candidate Application Form** — Collects candidate name, email, job title, and skills.
- ⚙️ **Python Backend** — Handles HTTP requests and processes application submissions.
- 🗄️ **SQLite Database** — Stores submitted candidate applications.
- 🐳 **Docker Containerization** — Packages the application into a Docker image.
- ☁️ **AWS EC2 Deployment** — Runs the container on an Amazon Linux EC2 instance.
- 🔄 **CI/CD Automation** — Uses GitHub Actions to build and push Docker images to Docker Hub.
- 🔐 **Secure Remote Access** — Uses AWS Systems Manager Session Manager and port forwarding without opening a public inbound application port.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Containerization | Docker |
| Cloud Platform | AWS EC2 |
| CI/CD | GitHub Actions |
| Container Registry | Docker Hub |
| Remote Access | AWS Systems Manager (SSM) |
| Version Control | Git & GitHub |

## 🏗️ Architecture

```text
👤 Candidate
     |
     v
🌐 Web Browser
     |
     v
📝 Candidate Application Form
     |
     v
⚙️ Python HTTP Server
     |
     v
🗄️ SQLite Database
     |
     v
✅ Application Saved
```

### ☁️ Deployment Workflow

```text
💻 Source Code (GitHub)
         |
         v
🔄 GitHub Actions
         |
         v
🐳 Docker Build
         |
         v
📦 Docker Hub
         |
         v
☁️ AWS EC2
         |
         v
🚀 Running Application Container
```

## 🚀 Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/mayuriii-13/talentflow-ai.git
cd talentflow-ai
```

### 2. Build the Docker Image

Run this command from the directory containing the `Dockerfile` and `app.py`:

```bash
docker build -t talentflow-ai .
```

### 3. Run the Container

```bash
docker run -d \
  --name talentflow-ai \
  -p 127.0.0.1:8000:8000 \
  talentflow-ai
```

### 4. Open the Application

Visit the following address on the same computer running Docker:

```text
http://127.0.0.1:8000
```

> 💡 The local Docker commands above are for local testing. The AWS deployment uses Docker on EC2 and AWS Systems Manager port forwarding for private access.

## 🧪 Testing

The following functionality has been tested in the AWS environment:

- ✅ Application page returns an HTTP `200 OK` response.
- ✅ Candidate details can be submitted through the web form.
- ✅ The backend validates required fields.
- ✅ Application records are stored in SQLite.
- ✅ The application runs inside a Docker container on AWS EC2.
- ✅ GitHub Actions successfully builds and pushes the Docker image.
- ✅ AWS Systems Manager port forwarding provides browser access without exposing port 8000 publicly.

## 🔐 Security Considerations

- 🔒 The EC2 security group does not require a public inbound rule for application port 8000.
- 🔑 AWS Systems Manager is used for remote access.
- 🛡️ AWS credentials and Docker Hub access tokens should be stored securely, never committed to GitHub.
- 🧪 Use fictional candidate information for testing this demo.

## 📌 Current Project Status

**Status: Working cloud deployment demo**

Implemented:
- Candidate application form
- Python HTTP backend
- SQLite application storage
- Docker container deployment on AWS EC2
- GitHub Actions Docker build-and-push workflow
- Private access through AWS Systems Manager port forwarding

Planned improvements:
- 🤖 AI-powered candidate matching and ranking
- 🗄️ Managed database integration, such as Amazon RDS
- 🔐 HTTPS and production-grade security
- 📈 Monitoring, logging, and improved error handling
- ☁️ Further deployment automation and scalability

*Note: AI-based candidate ranking, managed database integration, and production-grade scalability are planned features, not currently implemented.*

## 🎯 Learning Objectives

This project demonstrates practical learning in:

- AWS cloud infrastructure
- Linux and Docker container management
- Python web application development
- CI/CD with GitHub Actions
- Docker image publishing
- AWS Systems Manager remote access
- Database integration and application testing

## 👩‍💻 Author

**Mayuri Ambare**

- GitHub: [@mayuriii-13](https://github.com/mayuriii-13)
- Project Repository: [TalentFlow AI](https://github.com/mayuriii-13/talentflow-ai)

---

⭐ If you find this project useful, feel free to explore the repository!
