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
                sh '''
                    cd app
                    docker build -t rajivdocker10/demo-app:${BUILD_NUMBER} .
                    docker tag rajivdocker10/demo-app:${BUILD_NUMBER} rajivdocker10/demo-app:latest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "📤 Pushing to Docker Hub..."
                sh '''
                    echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                    docker push rajivdocker10/demo-app:${BUILD_NUMBER}
                    docker push rajivdocker10/demo-app:latest
                '''
            }
        }

        stage('Update K8s Manifest') {
            steps {
                echo "📝 Updating Kubernetes manifest..."
                sh '''
                    git checkout main || git checkout -b main origin/main
                    sed -i "s|image:.*|image: rajivdocker10/demo-app:${BUILD_NUMBER}|g" k8s/deployment.yaml
                    echo "Updated manifest:"
                    cat k8s/deployment.yaml
                '''
            }
        }

        stage('Push Manifest to GitHub') {
            steps {
                echo "📤 Pushing updated manifest to GitHub..."
                sh '''
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins"
                    git checkout main
                    git pull https://$GITHUB_TOKEN@github.com/rajiv4redapple/jenkins-k3s-demo.git main
                    sed -i "s|image:.*|image: rajivdocker10/demo-app:${BUILD_NUMBER}|g" k8s/deployment.yaml
                    git add k8s/deployment.yaml
                    git diff --cached --quiet || git commit -m "ci: update image to rajivdocker10/demo-app:${BUILD_NUMBER}"
                    git push https://$GITHUB_TOKEN@github.com/rajiv4redapple/jenkins-k3s-demo.git HEAD:main
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline SUCCESS! ArgoCD will deploy shortly..."
        }
        failure {
            echo "❌ Pipeline FAILED!"
        }
    }
}
