pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'princerajendran/todo-backend'
        KUBE_CONFIG = '~/.kube/config'
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .'
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    sh 'docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}'
                }
            }
        }
        stage('Deploy with Terraform') {
            steps {
                script {
                    sh '''
                    terraform init
                    terraform apply -auto-approve -var="docker_image=${DOCKER_IMAGE}:${BUILD_NUMBER}"
                    '''
                }
            }
        }
    }
}