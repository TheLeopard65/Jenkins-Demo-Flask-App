#!/bin/bash
set -e

show_help() {
    cat << EOF
Basic Flask-app Usage Syntax: $0 [OPTIONS]

Options:
  -h    Shows this help message and exits the script
  -s    Start the app (Must be run after -e, -r and -i)
  -e    Create a Python virtual environment (virtual-venv)
  -r    Install required packages from requirements.txt
  -i    Initialize fresh flask database setup & migration
  -d    Builds a Docker image and runs a containerized app

Example: $0 -e -r -i -s
EOF
}

if [ $# -eq 0 ]; then
    echo "[#] ERROR: No arguments supplied. Run '$0 -h' for help."
    exit 1
fi

for arg in "$@"; do
    case $arg in
        -h)
            show_help
            exit 0
        ;;
        -e)
            echo "[#] Creating virtual environment"
            python3 -m venv virtual-venv
        ;;
        -r)
            echo "[#] Installing required packages"
            if [ ! -d virtual-venv ]; then
                echo "[!] ERROR: Virtual environment not found. Use -e first."
                exit 1
            fi
            source virtual-venv/bin/activate
            pip install -r requirements.txt
        ;;
        -i)
            echo "[#] Initializing database"
            source virtual-venv/bin/activate
            flask db init || true
            flask db migrate -m "Initial Migration"
            flask db upgrade
        ;;
        -s)
            echo "[#] Starting Flask Application"
            source virtual-venv/bin/activate
            flask run
        ;;
        -d)
            if ! command -v docker &> /dev/null; then
                echo "[!] ERROR: Docker is not installed or not in PATH."
                exit 1
            fi
            echo "[#] Building and running Docker container"
            docker build -t flask-app-image .
            docker run -it --rm -p 5000:5000 --name flask-app flask-app-image
        ;;
        *)
            echo "[#] ERROR: Unknown argument '$arg'. Run '$0 -h' for help."
            exit 1
        ;;
    esac
done
