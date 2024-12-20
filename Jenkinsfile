pipeline {
    agent any

    environment {
        // AWS Credentials (can be configured in Jenkins as credentials)
        AWS_ACCESS_KEY_ID = credentials('AKIAVFIWI7H2KV4XOTUE') // AWS Access Key ID
        AWS_SECRET_ACCESS_KEY = credentials('2gSXo5eSpLIG2TyzEjuTwWVdEvUocVjceSrha53y') // AWS Secret Access Key
        AWS_REGION = 'us-east-1' // Specify your AWS region
        ECR_REPO_URI = '354918398452.dkr.ecr.us-east-1.amazonaws.com/healthsync' // Replace with your ECR URI
        EKS_CLUSTER_NAME = 'MyCluster' // Your EKS cluster name
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build Docker images for all microservices
                    sh """
                        docker build -t ${ECR_REPO_URI}/patient_record_service:latest ./patient_record_service
                        docker build -t ${ECR_REPO_URI}/doctor_service:latest ./doctor_service
                        docker build -t ${ECR_REPO_URI}/appointment_service:latest ./appointment_service
                        docker build -t ${ECR_REPO_URI}/notification_service:latest ./notification_service
                    """
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    // Login to AWS ECR
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}
                    """
                }
            }
        }

        stage('Push Docker Images to ECR') {
            steps {
                script {
                    // Push Docker images to ECR
                    sh """
                        docker push ${ECR_REPO_URI}/patient_record_service:latest
                        docker push ${ECR_REPO_URI}/doctor_service:latest
                        docker push ${ECR_REPO_URI}/appointment_service:latest
                        docker push ${ECR_REPO_URI}/notification_service:latest
                    """
                }
            }
        }

        stage('Update Kubernetes Config') {
            steps {
                script {
                    // Update the kubeconfig for EKS cluster
                    sh """
                        aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER_NAME}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Deploy the services to Kubernetes using kubectl
                    sh """
                        kubectl apply -f patient_record_service/deployment.yaml
                        kubectl apply -f doctor_service/deployment.yaml
                        kubectl apply -f appointment_service/deployment.yaml
                        kubectl apply -f notification_service/deployment.yaml
                    """
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    // Verify that the services are running
                    sh 'kubectl get pods'
                    sh 'kubectl get services'
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images
            sh 'docker system prune -f'
        }
    }
}
