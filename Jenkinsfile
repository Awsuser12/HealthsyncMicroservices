pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'your-docker-registry-url'
        DOCKER_CREDENTIALS_ID = 'docker-credentials-id'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-credentials-id'
        KUBERNETES_NAMESPACE = 'healthsync-namespace'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images for all microservices...'
                script {
                    def services = ['patient_record_service', 'appointment_service', 'notification_service', 'aggregator_service']
                    for (service in services) {
                        sh """
                            docker build -t ${DOCKER_REGISTRY}/${service}:latest -f ${service}/Dockerfile ${service}
                        """
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                echo 'Pushing Docker images to registry...'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        def services = ['patient_record_service', 'appointment_service', 'notification_service', 'aggregator_service']
                        for (service in services) {
                            sh """
                                docker push ${DOCKER_REGISTRY}/${service}:latest
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying services to Kubernetes cluster...'
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl --kubeconfig=$KUBECONFIG apply -f kubernetes/deployment.yaml -n ${KUBERNETES_NAMESPACE}
                        kubectl --kubeconfig=$KUBECONFIG apply -f kubernetes/service.yaml -n ${KUBERNETES_NAMESPACE}
                    """
                }
            }
        }

        stage('Run Integration Tests') {
            steps {
                echo 'Running integration tests...'
                sh """
                    pytest tests/integration_tests
                """
            }
        }

        stage('Post-Deployment Validation') {
            steps {
                echo 'Validating deployment...'
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl --kubeconfig=$KUBECONFIG get pods -n ${KUBERNETES_NAMESPACE}
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker images...'
            sh """
                docker image prune -f
            """
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
