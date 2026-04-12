pipeline {
    agent any
    stages {
        stage('Deploy App') {
            steps {
                // This builds and runs your containerized app
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }
}
