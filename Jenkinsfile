pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'flask-app-image'
        CONTAINER_NAME = 'flask-app'
        APP_PORT = '5000'
    }
    parameters {
        booleanParam(name: 'EXECUTE_TESTS', defaultValue: true, description: 'Enable/disable the post-deployment tests.')
        booleanParam(name: 'KEEP_CONTAINER', defaultValue: true, description: 'Keep container running after pipeline?')
    }
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }
        stage('Run Container') {
            steps {
                sh """
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p $APP_PORT:5000 $DOCKER_IMAGE
                """
                sleep 10
            }
        }
        stage('Post-Deployment Tests') {
		    when {
		        expression { params.EXECUTE_TESTS }
		    }
		    steps {
		        echo '[#] Running post-deployment tests...'
		        sh """
		            STATUS=\$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$APP_PORT/)
		            echo "Received HTTP status: \$STATUS"
		            [ "\$STATUS" -eq 200 ]
		        """
		    }
		}
    }
    post {
        always {
            script {
                if (!params.KEEP_CONTAINER) {
                    sh "docker rm -f $CONTAINER_NAME || true"
                }
            }
        }
        success {
            echo '[+] Pipeline completed successfully.'
        }
        failure {
            echo '[!] Pipeline Process/Build Failed!!!'
        }
    }
}
