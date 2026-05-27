pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo "Code checked out from GitHub!"
                sh 'ls -la'
            }
        }
        stage('Build') {
            steps {
                echo "Building the app..."
                sh 'echo "Build number: ${BUILD_NUMBER}"'
            }
        }
        stage('Test') {
            steps {
                echo "Running tests..."
                sh 'echo "All tests passed!"'
            }
        }
        stage('Done') {
            steps {
                echo "Pipeline finished for branch: ${GIT_BRANCH}"
            }
        }
    }
    post {
        success {
            echo "✅ Build SUCCESS!"
        }
        failure {
            echo "❌ Build FAILED!"
        }
    }
}
