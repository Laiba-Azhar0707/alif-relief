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
                sh 'sleep 10'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    docker build -f tests/Dockerfile.test -t alif-relief-tests ./tests
                    docker run --rm \
                        --network host \
                        -v $(pwd)/tests:/tests \
                        alif-relief-tests
                '''
            }
        }
    }
    post {
        always {
            emailext(
                subject: "Jenkins Build ${currentBuild.result}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build Result: ${currentBuild.result}</h2>
                    <p>Job: ${env.JOB_NAME}</p>
                    <p>Build Number: ${env.BUILD_NUMBER}</p>
                    <p>Check console: ${env.BUILD_URL}</p>
                """,
                recipientProviders: [[$class: 'RequesterRecipientProvider'], [$class: 'CulpritsRecipientProvider']],
                to: 'qasimalik@gmail.com',
                from: 'laibaazhar2190@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}
