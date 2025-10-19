pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        DOCKER_IMAGE = 'harrington40/hrms-app'
        DOCKER_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python3 --version'
                sh 'pip3 install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirement.txt'
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    pip3 install bandit safety
                    bandit -r . -f json -o bandit-report.json || true
                    safety check --output json > safety-report.json || true
                '''
                publishHTML target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'bandit-report.json,safety-report.json',
                    reportName: 'Security Scan Reports'
                ]
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    pip3 install pytest pytest-cov
                    python3 -m pytest tests/unit/ -v --cov=. --cov-report=xml --cov-report=html --cov-fail-under=80
                '''
            }
            post {
                always {
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                    publishHTML target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Unit Test Coverage Report'
                    ]
                }
            }
        }

        stage('Integration Tests') {
            steps {
                sh '''
                    pip3 install pytest pytest-html
                    # Start application in background for testing
                    python3 run_dual_services.py &
                    APP_PID=$!
                    sleep 30

                    # Run integration tests
                    python3 -m pytest tests/integration/ -v --tb=short --html=integration-report.html --self-contained-html

                    # Cleanup
                    kill $APP_PID || true
                '''
            }
            post {
                always {
                    publishHTML target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'integration-report.html',
                        reportName: 'Integration Test Report'
                    ]
                }
            }
        }

        stage('Regression Tests') {
            steps {
                sh '''
                    pip3 install pytest pytest-html selenium
                    # Install Chrome for Selenium tests
                    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
                    apt-get update
                    apt-get install -y google-chrome-stable

                    # Start application
                    python3 run_dual_services.py &
                    APP_PID=$!
                    sleep 30

                    # Run regression tests
                    python3 -m pytest tests/regression/ -v --tb=short --html=regression-report.html --self-contained-html

                    # Cleanup
                    kill $APP_PID || true
                '''
            }
            post {
                always {
                    publishHTML target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'regression-report.html',
                        reportName: 'Regression Test Report'
                    ]
                }
            }
        }

        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'dev'
                }
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def app = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        app.push()
                        if (env.BRANCH_NAME == 'main') {
                            app.push('latest')
                        }
                    }
                }
            }
        }

        stage('Build Windows Executable') {
            when {
                anyOf {
                    branch 'main'
                    branch 'dev'
                }
            }
            steps {
                sh '''
                    pip3 install pyinstaller

                    # Create executable
                    pyinstaller --clean hrms.spec

                    # Create installer if NSIS is available
                    if command -v makensis >/dev/null 2>&1; then
                        makensis installer.nsi
                    fi
                '''
                archiveArtifacts artifacts: 'dist/HRMS_Application.exe, HRMS_Application_installer.exe',
                               allowEmptyArchive: true,
                               fingerprint: true
            }
        }

        stage('Deploy to Test') {
            when {
                branch 'dev'
            }
            steps {
                echo 'Deploying to test environment...'
                // Add your test deployment commands here
                sh '''
                    echo "Test deployment commands go here"
                    # Example: kubectl apply -f k8s/test/ or docker-compose up -d
                '''
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to staging environment...'
                // Add your staging deployment commands here
                sh '''
                    echo "Staging deployment commands go here"
                '''
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to Production?',
                      ok: 'Deploy'
                echo 'Deploying to production environment...'
                // Add your production deployment commands here
                sh '''
                    echo "Production deployment commands go here"
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
            // Cleanup steps
            sh '''
                # Kill any remaining processes
                pkill -f "python3 run_dual_services.py" || true
                pkill -f "uvicorn" || true
            '''
        }
        success {
            echo 'Pipeline succeeded!'
            // Send success notifications
        }
        failure {
            echo 'Pipeline failed!'
            // Send failure notifications
        }
    }

    options {
        timeout(time: 2, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        // Poll SCM every 5 minutes for changes
        pollSCM('H/5 * * * *')
    }
}