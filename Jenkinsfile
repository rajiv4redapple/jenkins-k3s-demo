pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "rajivdocker10/demo-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')
        GITHUB_TOKEN = credentials('github-token')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh """
                    cd app
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo "📤 Pushing to Docker Hub..."
                sh """
                    echo ${DOCKERHUB_CREDS_PSW} | \
                    docker login -u ${DOCKERHUB_CREDS_USR} --password-stdin
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                """
            }
        }
        
stage('Update K8s Manifest') {
            steps {
                echo "📝 Updating Kubernetes manifest..."
                sh """
                    sed -i 's|image:.*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g' k8s/deployment.yaml
                    echo "Updated manifest:"
                    cat k8s/deployment.yaml
                """
            }
        }
        
        stage('Push Manifest to GitHub') {
            steps {
                echo "📤 Pushing updated manifest to GitHub..."
                sh """
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins"
                    git checkout main || git checkout -b main origin/main
                    sed -i 's|image:.*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g' k8s/deployment.yaml
                    git add k8s/deployment.yaml
                    git diff --cached --quiet || git commit -m "ci: update image to ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    git push https://\${GITHUB_TOKEN}@github.com/rajiv4redapple/jenkins-k3s-demo.git HEAD:main
                """
            }
        }
        
