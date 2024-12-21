pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = 'AKIAVFIWI7H2KV4XOTUE'
        AWS_SECRET_ACCESS_KEY = '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'
        AWS_DEFAULT_REGION = 'us-east-1'
        CLUSTER_NAME = 'MyCluster'
        IMAGE_TAG = 'latest'

        // ECR Repositories for Microservices
        PATIENT_RECORD_SERVICE_REPO = '354918398452.dkr.ecr.us-east-1.amazonaws.com/healthsync/patient_record_service'
        //APPOINTMENT_SERVICE_REPO = '354918398452.dkr.ecr.us-east-1.amazonaws.com/healthsync/appointment_service'
        //DOCTOR_SERVICE_REPO = '354918398452.dkr.ecr.us-east-1.amazonaws.com/healthsync/doctor_service'
        //BILLING_SERVICE_REPO = '354918398452.dkr.ecr.us-east-1.amazonaws.com/healthsync/billing_service'

        // YAML file paths
        //APPOINTMENT_SERVICE_YAML = './appointment_service/deployment.yaml'
        PATIENT_RECORD_SERVICE_YAML = './patient_record_service/deployment.yaml'
        //DOCTOR_SERVICE_YAML = './doctor_service/deployment.yaml'
        //BILLING_SERVICE_YAML = './billing_service/deployment.yaml'
    }

    stages {
        stage('Build Docker Images') {
            steps {
                echo "Building Docker images for all microservices..."
                script {
                    sh '''
                    # Build patient_record_service
                    docker build -t ${PATIENT_RECORD_SERVICE_REPO}:${IMAGE_TAG} ./patient_record_service

                    # Build appointment_service
                    #docker build -t ${APPOINTMENT_SERVICE_REPO}:${IMAGE_TAG} ./appointment_service

                    # Build doctor_service
                    #docker build -t ${DOCTOR_SERVICE_REPO}:${IMAGE_TAG} ./doctor_service

                    # Build billing_service
                    #docker build -t ${BILLING_SERVICE_REPO}:${IMAGE_TAG} ./billing_service
                    '''
                }
            }
        }

        stage('Push Docker Images to ECR') {
            steps {
                echo "Pushing Docker images to AWS ECR..."
                script {
                    sh '''
                    # Authenticate with ECR
                    aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${PATIENT_RECORD_SERVICE_REPO}

                    # Push patient_record_service
                    docker push ${PATIENT_RECORD_SERVICE_REPO}:${IMAGE_TAG}

                    # Push appointment_service
                    #docker push ${APPOINTMENT_SERVICE_REPO}:${IMAGE_TAG}

                    # Push doctor_service
                    #docker push ${DOCTOR_SERVICE_REPO}:${IMAGE_TAG}

                    # Push billing_service
                    #docker push ${BILLING_SERVICE_REPO}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Update kubeconfig') {
            steps {
                echo "Configuring kubectl for EKS cluster..."
                script {
                    sh '''
                    aws eks --region ${AWS_DEFAULT_REGION} update-kubeconfig --name ${CLUSTER_NAME}
                    '''
                }
            }
        }

        stage('Deploy Microservices') {
            steps {
                echo "Deploying microservices to EKS cluster..."
                script {
                    sh '''
                    # Deploy patient_record_service
                    kubectl apply -f /home/ubuntu/patient_record_service/deployment.yaml

                    # Deploy appointment_service
                    #kubectl apply -f ${APPOINTMENT_SERVICE_YAML}

                    # Deploy doctor_service
                    #kubectl apply -f ${DOCTOR_SERVICE_YAML}

                    # Deploy billing_service
                    #kubectl apply -f ${BILLING_SERVICE_YAML}
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "Verifying application deployment..."
                script {
                    sh '''
                    kubectl get pods
                    kubectl get services
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed."
        }
        success {
            echo "All microservices deployed successfully!"
        }
        failure {
            echo "Deployment failed. Please check the logs."
        }
    }
}
