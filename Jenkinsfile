pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Laiba-Azhar0707/alif-relief.git'
            }
        }
        stage('Deploy App') {
            steps {
                sh 'docker compose -f docker-compose.pipeline.yml down || true'
                sh 'docker compose -f docker-compose.pipeline.yml up -d --build'
            }
        }
    }
}
