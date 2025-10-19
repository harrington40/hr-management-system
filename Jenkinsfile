/*
 * HRMS CI/CD Pipeline (hardened)
 */

pipeline {
  agent any

  options {
    timeout(time: 2, unit: 'HOURS')
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timestamps()
  }

  environment {
    PYTHON_VERSION = '3.11'                 // You can pin to 3.9 if required
    DOCKER_IMAGE   = 'harrington40/hrms-app'
    DOCKER_TAG     = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    APP_HOST       = '127.0.0.1'
    APP_PORT       = '8000'                 // adjust to whatever run_dual_services.py exposes
  }

  triggers {
    // Prefer GitHub webhook:
    // githubPush()
    // Fallback polling (comment out if using webhooks):
    // pollSCM('H/5 * * * *')
  }

  stages {

    stage('Pipeline Info') {
      steps {
        echo "=== Pipeline Information ==="
        echo "Branch: ${env.BRANCH_NAME}"
        echo "Build Number: ${env.BUILD_NUMBER}"
        echo "Job Name: ${env.JOB_NAME}"
        echo "Node: ${env.NODE_NAME}"
        echo "Workspace: ${env.WORKSPACE}"
        sh '''
          set -euxo pipefail
          pwd
          ls -la
        '''
      }
    }

    stage('Checkout') {
      steps {
        echo "=== Starting Checkout ==="
        checkout scm
        echo "=== Checkout Completed ==="
        sh '''
          set -euxo pipefail
          ls -la
          git branch
          git log --oneline -5
        '''
      }
    }

    stage('Validate Environment') {
      steps {
        sh '''
          set -euxo pipefail
          echo "=== Environment Validation ==="
          which python3
          python3 --version

          # If you use 'requirements.txt', update the filename below.
          test -f requirement.txt || (echo "ERROR: requirement.txt not found" && exit 1)
          test -f main.py || (echo "ERROR: main.py not found" && exit 1)

          df -h .
          echo "Environment validation completed successfully"
        '''
      }
    }

    stage('Quick Test') {
      steps {
        sh '''
          set -euxo pipefail
          echo "=== Running Quick Test ==="
          python3 - <<'PY'
print('Python execution works!')
PY
          ls -la
        '''
      }
    }

    stage('Security Scan') {
      steps {
        sh '''
          set -euxo pipefail
          echo "=== Running Security Scan ==="

          # Optional venv
          if [ -d "venv" ]; then
            . venv/bin/activate
            PIP="python3 -m pip"
            PY="python3"
          else
            PIP="python3 -m pip"
            PY="python3"
          fi

          $PIP install --upgrade pip
          # Try bandit + safety; if safety fails (requires key in newer versions), fall back to pip-audit
          $PIP install bandit || true
          $PIP install safety || true
          $PIP install pip-audit || true

          if command -v bandit >/dev/null 2>&1 || [ -x "./venv/bin/bandit" ]; then
            bandit -r . -f html -o bandit-report.html || true
          fi

          if command -v safety >/dev/null 2>&1 || [ -x "./venv/bin/safety" ]; then
            # safety outputs JSON/HTML depending on flags; use HTML for publishHTML
            safety check --full-report --output html > safety-report.html || true
          else
            # fallback: pip-audit with HTML via --format markdown then convert simple page
            pip-audit -r requirement.txt -f json > pip-audit.json || true
            python3 - <<'PY'
import json, sys, pathlib
p = pathlib.Path('pip-audit.json')
h = pathlib.Path('pip-audit.html')
if p.exists():
    data = json.loads(p.read_text())
    rows = ''.join(f"<tr><td>{v.get('name')}</td><td>{v.get('version')}</td><td>{', '.join(a.get('id','') for a in v.get('vulns',[]))}</td></tr>" for v in data.get('dependencies',[]))
    h.write_text(f"<html><body><h1>pip-audit</h1><table border=1><tr><th>package</th><th>version</th><th>vulns</th></tr>{rows}</table></body></html>")
PY
          fi

          echo "Security scan completed"
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'bandit-report.html,safety-report.html,pip-audit.*', allowEmptyArchive: true
          publishHTML target: [
            allowMissing: true,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: '.',
            reportFiles: 'bandit-report.html,safety-report.html,pip-audit.html',
            reportName: 'Security Reports'
          ]
        }
      }
    }

    stage('Unit Tests') {
      steps {
        sh '''
          set -euxo pipefail
          echo "=== Running Unit Tests ==="

          if [ -d "venv" ]; then . venv/bin/activate; fi
          python3 -m pip install --upgrade pip
          python3 -m pip install -r requirement.txt
          python3 -m pip install pytest pytest-cov

          python3 -m pytest tests/unit/ -v \
            --cov=. --cov-report=xml:coverage.xml --cov-report=html:htmlcov \
            --cov-fail-under=80
        '''
      }
      post {
        always {
          publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
          publishHTML target: [
            allowMissing: true,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'htmlcov',
            reportFiles: 'index.html',
            reportName: 'Unit Test Coverage'
          ]
        }
      }
    }

    stage('Integration Tests') {
      steps {
        sh '''
          set -euxo pipefail
          echo "=== Running Integration Tests ==="

          if [ -d "venv" ]; then . venv/bin/activate; fi
          python3 -m pip install -r requirement.txt
          python3 -m pip install pytest pytest-html

          python3 run_dual_services.py &
          APP_PID=$!
          echo "App PID: $APP_PID"

          # Readiness loop (30s max)
          for i in $(seq 1 30); do
            if curl -fsS "http://${APP_HOST}:${APP_PORT}/health" >/dev/null 2>&1 || curl -fsS "http://${APP_HOST}:${APP_PORT}" >/dev/null 2>&1; then
              echo "App is ready"
              break
            fi
            sleep 1
          done

          # Ensure still running
          kill -0 $APP_PID

          python3 -m pytest tests/integration/ -v --tb=short \
            --html=integration-report.html --self-contained-html

          kill $APP_PID || true
          wait || true
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
          set -euxo pipefail
          echo "=== Running Regression Tests ==="

          if [ -d "venv" ]; then . venv/bin/activate; fi
          python3 -m pip install -r requirement.txt
          python3 -m pip install pytest pytest-html selenium webdriver-manager

          # Start app
          python3 run_dual_services.py &
          APP_PID=$!
          echo "App PID: $APP_PID"

          # Readiness loop
          for i in $(seq 1 30); do
            if curl -fsS "http://${APP_HOST}:${APP_PORT}/health" >/dev/null 2>&1 || curl -fsS "http://${APP_HOST}:${APP_PORT}" >/dev/null 2>&1; then
              echo "App is ready"
              break
            fi
            sleep 1
          done

          # Run regression (Selenium will download a driver via webdriver-manager; runs headless by default if your tests set it)
          python3 -m pytest tests/regression/ -v --tb=short \
            --html=regression-report.html --self-contained-html || (kill $APP_PID || true; exit 1)

          kill $APP_PID || true
          wait || true
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
      when { anyOf { branch 'main'; branch 'dev' } }
      steps {
        script {
          try {
            echo "=== Building Docker Image ==="
            docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
              def app = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
              app.push()
              if (env.BRANCH_NAME == 'main') {
                app.push('latest')
              }
            }
            echo "Docker build completed successfully"
          } catch (Exception e) {
            echo "Docker build failed: ${e.getMessage()}"
            sh '''
              set +e
              docker --version || echo "Docker not found"
              docker ps || echo "Docker daemon not running"
              exit 1
            '''
          }
        }
      }
    }

    stage('Build Windows Executable') {
      when { anyOf { branch 'main'; branch 'dev' } }
      agent { label 'windows' }   // requires a Windows node; otherwise this stage is skipped
      steps {
        bat '''
          @echo on
          echo === Building Windows Executable ===
          py -3 -m pip install --upgrade pip
          IF EXIST requirement.txt (py -3 -m pip install -r requirement.txt)

          py -3 -m pip install pyinstaller
          py -3 -m PyInstaller --clean hrms.spec

          IF EXIST installer.nsi (
            where makensis && makensis installer.nsi
          )

          echo Build done
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'dist/**/*.exe,*.exe', allowEmptyArchive: true, fingerprint: true
        }
      }
    }

    stage('Deploy to Test') {
      when { branch 'dev' }
      steps {
        sh '''
          set -euxo pipefail
          echo "Deploying to test environment..."
          # Example:
          # kubectl apply -f k8s/test/
          # or: docker compose -f docker-compose.test.yml up -d --pull always
        '''
      }
    }

    stage('Deploy to Staging') {
      when { branch 'main' }
      steps {
        sh '''
          set -euxo pipefail
          echo "Deploying to staging environment..."
          # Example:
          # kubectl apply -f k8s/staging/
          # or: ssh + docker compose on remote host
        '''
      }
    }

    stage('Final Validation') {
      steps {
        sh '''
          set -euxo pipefail
          echo "All stages completed successfully!"
        '''
      }
    }
  }

  post {
    always {
      echo "=== Pipeline Post Actions ==="
      sh '''
        set +e
        pkill -f "python3 run_dual_services.py" || true
        pkill -f "uvicorn" || true
        echo "Cleanup completed"
      '''
    }
    success {
      echo "🎉 PIPELINE SUCCEEDED!"
    }
    failure {
      echo "❌ PIPELINE FAILED! See the logs above."
      sh '''
        set +e
        echo "Failure diagnostics:"
        echo "CWD: $(pwd)"
        df -h .
        ps aux | head -100
      '''
    }
  }
}
