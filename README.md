## 🧾 Flask User Form App

A simple CRUD-based Flask web application with secure user management using SQLAlchemy, Flask-Migrate, and WTForms. Users can register, update, and delete profiles. The app is fully containerized with Docker and integrated with Jenkins for automated CI/CD pipeline execution.

---

### 📁 Project Structure

```
Flask-App/
├── app.py                   # Main Flask application
├── config.py                # App configuration using environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-entrypoint.sh     # Container entrypoint script
├── start.sh                 # Local helper script for app setup
├── templates/               # HTML templates (index, update, error pages)
├── .env                     # Environment variables (excluded from VCS)
├── .gitignore               # Ignored files
└── Jenkinsfile              # Jenkins pipeline definition
```

---

## 🚀 Features

* User registration with email & password (bcrypt hashed)
* CSRF-protected forms via Flask-WTF
* Server-side validation with WTForms
* SQLite-backed database with migrations
* Clean HTML templates with Bootstrap 5
* Dockerized with health checks
* Jenkins CI/CD pipeline for automation

---

## 🧪 Tech Stack

* Python 3.10
* Flask, SQLAlchemy, Flask-Migrate
* WTForms, Flask-Bcrypt
* Docker
* Jenkins (Multibranch Pipeline)
* SQLite
* Bootstrap (via CDN)

---

## 📦 Setup & Run

### ▶️ Run Locally (Manual)

```bash
# Create virtual environment
python3 -m venv virtual-venv
source virtual-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Initialize DB
flask db init
flask db migrate -m "Initial"
flask db upgrade

# Run the app
flask run
```

### 🐳 Run with Docker

```bash
# Build the Docker image
docker build -t flask-app-image .

# Run the container
docker run -d -p 5000:5000 --name flask-app flask-app-image
```

---

## ⚙️ Jenkins CI/CD Pipeline

This project includes a `Jenkinsfile` for automating build and deployment using Jenkins.

### 🔁 Pipeline Stages

1. **Clone Repository**: Jenkins fetches your GitHub repo
2. **Build Docker Image**: Builds container from Dockerfile
3. **Run Container**: Starts Flask app in Docker
4. **Health Check**: Validates service is up
5. **Post Actions**: Cleans up Docker resources

### 🧾 Jenkinsfile

<details>
<summary>Click to view</summary>

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app-image'
        CONTAINER_NAME = 'flask-app'
        APP_PORT = '5000'
    }

    parameters {
        booleanParam(name: 'EXECUTE_TESTS', defaultValue: true, description: 'Run post-deployment tests?')
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo '[#] Cloning Repository'
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '[#] Building Docker Image'
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }

        stage('Run Container') {
            steps {
                echo '[#] Running Docker Container'
                sh """
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p $APP_PORT:5000 $DOCKER_IMAGE
                """
                sleep 10
            }
        }

        stage('Run Tests') {
            when {
                expression { return params.EXECUTE_TESTS == true }
            }
            steps {
                echo '[#] Running Health Check Test'
                script {
                    def result = sh(script: "curl -s -o /dev/null -w \"%{http_code}\" http://localhost:$APP_PORT/", returnStdout: true).trim()
                    if (result != '200') {
                        error "Health check failed with status: ${result}"
                    } else {
                        echo "Health check passed with status: ${result}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo '[#] Cleaning up Docker resources...'
            sh "docker stop $CONTAINER_NAME || true"
            sh "docker rm $CONTAINER_NAME || true"
        }

        success {
            echo '[+] Pipeline completed successfully.'
        }

        failure {
            echo '[!] Pipeline failed.'
        }
    }
}
```

</details>

---

## ✅ Requirements

* Python 3.10+
* Docker
* Jenkins (latest preferred)
* Git

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
