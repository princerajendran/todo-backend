pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t princerajendran/todo-backend:${BUILD_NUMBER} .'
            }
        }
        stage('Push') {
            steps {
                sh 'docker push princerajendran/todo-backend:${BUILD_NUMBER}'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl set image deployment/todo-backend todo-backend=princerajendran/todo-backend:${BUILD_NUMBER}'
            }
        }
    }
}