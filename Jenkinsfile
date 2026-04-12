pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Laiba-Azhar0707/alif-relief.git'
            }
        }
        stage('Build & Run') {
            steps {
                // This stops any old version and starts the new one
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }
}
