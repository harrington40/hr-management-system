# Jenkins Pipeline Debugging Guide

## Problem Analysis
Your Jenkins pipeline is failing with "script returned exit code 1" but the specific failure stage is not clear from the logs. This indicates one of the pipeline stages is failing but error handling could be improved.

## Common Failure Points

### 1. Python Setup Issues
**Symptoms**: Pipeline fails early, Python not found
**Check**:
```bash
python3 --version
which python3
pip3 --version
```

**Fix**: Ensure Python 3.9+ is installed on Jenkins agent

### 2. Dependency Installation Issues
**Symptoms**: "ModuleNotFoundError" or pip install failures
**Check**:
```bash
ls -la requirement.txt
cat requirement.txt | head -10
pip3 install --dry-run -r requirement.txt
```

**Fix**: Ensure all dependencies are available and compatible

### 3. Database Connection Issues
**Symptoms**: Tests fail with connection errors
**Check**:
- PostgreSQL service running
- Database credentials configured
- Network connectivity

### 4. Docker Issues
**Symptoms**: Docker build fails
**Check**:
```bash
docker --version
docker ps
docker system info
```

**Fix**: Ensure Docker is installed and Jenkins user has permissions

### 5. Test Failures
**Symptoms**: Unit/integration tests fail
**Check**: Test output for specific failures
**Fix**: Run tests locally to debug

## Debugging Steps

### Step 1: Enable Verbose Logging
The updated Jenkinsfile now includes better logging. Re-run the pipeline to see detailed output.

### Step 2: Check Jenkins Agent Setup
Ensure your Jenkins agent has:

1. **Python 3.9+**
2. **pip**
3. **Docker** (with proper permissions)
4. **Git**
5. **Chrome/Chromium** (for Selenium tests)
6. **PostgreSQL** (for testing)

### Step 3: Test Individual Stages

#### Manual Testing Commands:
```bash
# Test Python setup
python3 --version
pip3 install --upgrade pip

# Test dependencies
pip3 install -r requirement.txt

# Test security scan
pip3 install bandit safety
bandit -r . -f json -o bandit-report.json

# Test unit tests
pip3 install pytest pytest-cov
python3 -m pytest tests/unit/ -v

# Test Docker
docker --version
docker build -t test-hrms .
```

### Step 4: Check Resource Constraints
Jenkins might be running out of:
- Memory
- Disk space
- CPU resources

Check Jenkins agent system resources.

## Quick Fixes

### Fix 1: Add Missing Dependencies
If dependencies fail to install, add them to `requirement.txt` or install system packages:

```bash
# For Ubuntu/Debian
apt-get update
apt-get install -y python3-dev build-essential libssl-dev libffi-dev

# For CentOS/RHEL
yum install -y python3-devel gcc openssl-devel libffi-devel
```

### Fix 2: Docker Permissions
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Or run Docker with sudo (less secure)
```

### Fix 3: Database Setup
Ensure PostgreSQL is running and accessible:
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo -u postgres createdb hrms_test
```

### Fix 4: Memory Issues
Increase Jenkins agent memory or add swap space.

## Updated Jenkinsfile Features

The updated Jenkinsfile includes:
- ✅ Better error messages and logging
- ✅ Explicit error handling with `exit 1`
- ✅ Process management for integration tests
- ✅ Docker error handling and diagnostics
- ✅ Stage-by-stage debugging output

## Troubleshooting Checklist

### Pre-Build Checks:
- [ ] Jenkins agent has Python 3.9+
- [ ] Docker is installed and accessible
- [ ] PostgreSQL is running
- [ ] Sufficient disk space (>5GB free)
- [ ] Network connectivity to GitHub and Docker Hub

### Build-Time Checks:
- [ ] Check console output for specific error messages
- [ ] Look for "exit code 1" or "ERROR" in logs
- [ ] Verify each stage completes successfully
- [ ] Check resource usage during build

### Post-Build Analysis:
- [ ] Review test reports if generated
- [ ] Check artifact creation
- [ ] Verify cleanup completed

## Emergency Fixes

### If Pipeline Keeps Failing:
1. **Disable problematic stages** temporarily:
   ```groovy
   stage('Problem Stage') {
       when { expression { false } }  // Skip this stage
       steps {
           // original steps
       }
   }
   ```

2. **Run simpler pipeline** for testing:
   ```groovy
   pipeline {
       agent any
       stages {
           stage('Test') {
               steps {
                   sh 'echo "Basic test"'
                   sh 'python3 --version'
               }
           }
       }
   }
   ```

3. **Check Jenkins system logs**:
   ```bash
   tail -f /var/log/jenkins/jenkins.log
   ```

## Getting More Debug Info

### Enable Debug Mode:
Add to Jenkinsfile environment:
```groovy
environment {
    // ... existing vars
    DEBUG = 'true'
}
```

### Add Debug Steps:
```groovy
stage('Debug Info') {
    steps {
        sh '''
            echo "=== System Info ==="
            uname -a
            df -h
            free -h
            echo "=== Python Info ==="
            python3 --version
            pip3 list
            echo "=== Docker Info ==="
            docker --version
            docker ps
        '''
    }
}
```

## Next Steps

1. **Re-run the pipeline** with updated Jenkinsfile
2. **Check the detailed logs** for specific failure points
3. **Apply the appropriate fix** from above
4. **Test individual components** locally if needed

The enhanced logging will now show exactly where the pipeline is failing!