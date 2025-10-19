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
                sh '''
                    echo "=== Setting up Python Environment ==="
                    python3 --version || echo "Python3 not found"

                    # Create virtual environment to avoid externally-managed-environment issues
                    python3 -m venv venv || echo "venv creation failed, trying alternative"

                    # Activate virtual environment
                    . venv/bin/activate || echo "venv activation failed"

                    # Upgrade pip within virtual environment
                    ./venv/bin/pip install --upgrade pip || pip3 install --upgrade pip --user

                    echo "Python environment setup completed"
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "=== Installing Dependencies ==="
                    ls -la requirement.txt || echo "requirement.txt not found"

                    # Try virtual environment first
                    if [ -d "venv" ]; then
                        echo "Using virtual environment"
                        . venv/bin/activate
                        ./venv/bin/pip install -r requirement.txt || exit 1
                    else
                        echo "Virtual environment not available, trying system pip"
                        pip3 install -r requirement.txt --user || exit 1
                    fi

                    echo "Dependencies installed successfully"
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    echo "=== Running Security Scan ==="

                    # Activate virtual environment if available
                    if [ -d "venv" ]; then
                        . venv/bin/activate
                        ./venv/bin/pip install bandit safety || exit 1
                        ./venv/bin/bandit -r . -f json -o bandit-report.json || true
                        ./venv/bin/safety check --output json > safety-report.json || true
                    else
                        pip3 install bandit safety --user || exit 1
                        bandit -r . -f json -o bandit-report.json || true
                        safety check --output json > safety-report.json || true
                    fi

                    echo "Security scan completed"
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
                    echo "=== Running Unit Tests ==="

                    # Activate virtual environment if available
                    if [ -d "venv" ]; then
                        . venv/bin/activate
                        ./venv/bin/pip install pytest pytest-cov || exit 1
                        ./venv/bin/python3 -m pytest tests/unit/ -v --cov=. --cov-report=xml --cov-report=html --cov-fail-under=80 || exit 1
                    else
                        pip3 install pytest pytest-cov --user || exit 1
                        python3 -m pytest tests/unit/ -v --cov=. --cov-report=xml --cov-report=html --cov-fail-under=80 || exit 1
                    fi

                    echo "Unit tests completed successfully"
                '''
            }
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
                    echo "=== Running Integration Tests ==="

                    # Activate virtual environment if available
                    if [ -d "venv" ]; then
                        . venv/bin/activate
                        ./venv/bin/pip install pytest pytest-html || exit 1
                        PYTHON_CMD="./venv/bin/python3"
                    else
                        pip3 install pytest pytest-html --user || exit 1
                        PYTHON_CMD="python3"
                    fi

                    echo "Starting application for integration tests..."

                    # Start application in background
                    $PYTHON_CMD run_dual_services.py &
                    APP_PID=$!
                    echo "Application started with PID: $APP_PID"

                    # Wait for app to start
                    sleep 30

                    # Check if app is running
                    if kill -0 $APP_PID 2>/dev/null; then
                        echo "Application is running"
                    else
                        echo "Application failed to start"
                        exit 1
                    fi

                    # Run integration tests
                    echo "Running integration tests..."
                    $PYTHON_CMD -m pytest tests/integration/ -v --tb=short --html=integration-report.html --self-contained-html || exit 1

                    # Cleanup
                    echo "Stopping application..."
                    kill $APP_PID || true
                    sleep 5
                    echo "Integration tests completed successfully"
                '''
            }
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
                    echo "=== Running Regression Tests ==="

                    # Install Chrome for Selenium tests
                    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
                    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
                    apt-get update
                    apt-get install -y google-chrome-stable

                    # Activate virtual environment if available
                    if [ -d "venv" ]; then
                        . venv/bin/activate
                        ./venv/bin/pip install pytest pytest-html selenium || exit 1
                        PYTHON_CMD="./venv/bin/python3"
                    else
                        pip3 install pytest pytest-html selenium --user || exit 1
                        PYTHON_CMD="python3"
                    fi

                    # Start application
                    $PYTHON_CMD run_dual_services.py &
                    APP_PID=$!
                    echo "Application started with PID: $APP_PID"
                    sleep 30

                    # Run regression tests
                    $PYTHON_CMD -m pytest tests/regression/ -v --tb=short --html=regression-report.html --self-contained-html || exit 1

                    # Cleanup
                    kill $APP_PID || true
                    echo "Regression tests completed"
                '''
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
                    try {
                        echo "=== Building Docker Image ==="
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                            echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                            def app = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                            echo "Pushing Docker image..."
                            app.push()
                            if (env.BRANCH_NAME == 'main') {
                                echo "Pushing latest tag for main branch"
                                app.push('latest')
                            }
                            echo "Docker build completed successfully"
                        }
                    } catch (Exception e) {
                        echo "Docker build failed: ${e.getMessage()}"
                        echo "Checking Docker installation..."
                        sh 'docker --version || echo "Docker not found"'
                        sh 'docker ps || echo "Docker daemon not running"'
                        throw e
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
                    echo "=== Building Windows Executable ==="

                    # Activate virtual environment if available
                    if [ -d "venv" ]; then
                        . venv/bin/activate
                        ./venv/bin/pip install pyinstaller || exit 1
                        PYINSTALLER_CMD="./venv/bin/pyinstaller"
                    else
                        pip3 install pyinstaller --user || exit 1
                        PYINSTALLER_CMD="pyinstaller"
                    fi

                    # Create executable
                    $PYINSTALLER_CMD --clean hrms.spec || exit 1

                    # Create installer if NSIS is available
                    if command -v makensis >/dev/null 2>&1; then
                        makensis installer.nsi || echo "NSIS installer creation failed"
                    else
                        echo "NSIS not available, skipping installer creation"
                    fi

                    echo "Windows executable build completed"
                '''
                archiveArtifacts artifacts: 'dist/HRMS_Application.exe, HRMS_Application_installer.exe',
                               allowEmptyArchive: true,
                               fingerprint: true
            }
        }
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