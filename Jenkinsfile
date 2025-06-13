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
