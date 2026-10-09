# TalentFlow AI — Recruitment & Talent Management Platform

TalentFlow AI is a cloud-focused recruitment application demo developed as part of a Week 11 DevOps project at Davine Technology. It provides a candidate application form and stores submitted applications in an SQLite database.

The project is being developed incrementally to explore containerization, cloud deployment, and DevOps practices using AWS.

## Current Features

- Candidate application form
- Input validation for required fields
- Python HTTP server
- SQLite database for storing applications
- JSON-based application submission endpoint
- Dockerfile for container image creation
- AWS EC2 deployment with access through AWS Systems Manager Session Manager
- Private Amazon S3 storage for the application source file

## Technology Stack

- **Language:** Python
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python HTTP server
- **Database:** SQLite
- **Cloud:** Amazon Web Services (AWS)
- **Compute:** Amazon EC2
- **Storage:** Amazon S3
- **Secure administration:** AWS Systems Manager Session Manager
- **Containerization:** Docker
- **Image registry:** Docker Hub
- **Source control and CI/CD:** GitHub and GitHub Actions (planned)

## Project Structure

```text
talentflow-ai/
├── app.py
├── Dockerfile
├── README.md
└── .github/
    └── workflows/
        └── docker-build.yml
```

The GitHub Actions workflow will be added when the cloud build pipeline is configured.

## Run Locally

**Requirements:** Python 3.9 or later.

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd talentflow-ai
   ```

2. Start the application:

   ```bash
   python app.py
   ```

3. Open your browser at:

   http://127.0.0.1:8000

4. Enter fictional candidate information and submit the form.

The application creates `talentflow.db` in the same directory as `app.py` when it starts.

## Docker

The project includes a Dockerfile for packaging the application.

The intended workflow is:

1. Build the Docker image using a cloud build environment.
2. Publish the image to a private Docker Hub repository.
3. Deploy the container to a suitable runtime environment.
4. Configure persistent storage for application records.

Docker image publishing and container deployment are still in progress.

## AWS Deployment Status

The initial application demo has been tested on an Amazon EC2 instance in the Mumbai region (`ap-south-1`). The application was accessed using AWS Systems Manager Session Manager port forwarding, and a test application was successfully saved to SQLite.

The following components from the proposed architecture are planned or under development, not yet confirmed as implemented:

- Automated Docker image build and publishing
- Managed database using Amazon RDS
- Application Load Balancer and HTTPS
- Auto Scaling
- AI-based candidate ranking and resume analysis
- Production authentication and authorization
- Centralized monitoring and alerting

## Security Notes

- Do not commit AWS credentials, private keys, passwords, or candidate databases.
- Keep the Docker Hub repository private while the image is under development.
- Use fictional candidate data for testing.
- Do not expose the current demo publicly without adding authentication, appropriate input protections, and secure deployment configuration.
- Configure persistent storage before relying on container-based database records.

## Learning Objectives

- Understand cloud-based application deployment
- Practice AWS EC2 and S3
- Learn Docker image creation and container deployment
- Explore CI/CD automation using GitHub Actions
- Understand database persistence and cloud security fundamentals

## Project Status

**Status:** Working application demo; container build and automated deployment in progress.

This is an educational project and is not yet a production-ready recruitment platform.

## Author

Mayuri Ambare

Cloud & DevOps Engineering — AWS
