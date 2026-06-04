pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "rajivdocker10/demo-app"
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {

        stage('Check Commit') {
            steps {
                script {
                    def commitMsg = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()
                    echo "Commit message: ${commitMsg}"
                    if (commitMsg.startsWith('ci:')) {
                        echo "⏭️ Skipping build — commit made by Jenkins CI"
                        currentBuild.result = 'NOT_BUILT'
                        error('Skipping CI commit')
                    }
                }
            }
        }

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
                    docker logout
                '''
            }
        }

        stage('Update and Push Manifest') {
            steps {
                echo "📝 Updating Kubernetes manifest and pushing to GitHub..."
                sh '''
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins"
                    git config pull.rebase false
                    git fetch origin main
                    git reset --hard origin/main
                    sed -i "s|image:.*|image: rajivdocker10/demo-app:${BUILD_NUMBER}|g" k8s/deployment.yaml
                    echo "--- Updated manifest ---"
                    cat k8s/deployment.yaml
                    echo "------------------------"
                    git add k8s/deployment.yaml
                    git diff --cached --quiet || git commit -m "ci: update image to rajivdocker10/demo-app:${BUILD_NUMBER}"
                    git push https://$GITHUB_TOKEN@github.com/rajiv4redapple/jenkins-k3s-demo.git HEAD:main
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline SUCCESS! ArgoCD will detect and deploy shortly..."
        }
        failure {
            echo "❌ Pipeline FAILED! Check console output above."
        }
        always {
            echo "🏁 Pipeline finished - Build #${BUILD_NUMBER}"
        }
    }
}
