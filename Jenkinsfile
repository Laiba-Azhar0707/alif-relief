pipeline {
    agent any
    stages {
        stage('Deploy App') {
            steps {
                // We removed the dash between docker and compose
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}
