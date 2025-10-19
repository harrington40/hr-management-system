# Jenkins Integration Guide for HRMS

This guide explains how to integrate Jenkins CI/CD with your HRMS application.

## Jenkins Server Information
- **URL**: https://jenkins.transtechologies.com:18084/
- **Pipeline**: Declarative pipeline using Jenkinsfile

## Integration Options

### Option 1: Replace GitHub Actions with Jenkins
- Use Jenkins as the primary CI/CD system
- Disable GitHub Actions workflows
- All builds, tests, and deployments run through Jenkins

### Option 2: Jenkins + GitHub Actions Hybrid
- Keep GitHub Actions for basic CI
- Use Jenkins for complex deployments and specific environments
- Best of both worlds approach

### Option 3: Jenkins for Specific Tasks
- Use Jenkins for Windows builds only
- Use Jenkins for production deployments
- Keep GitHub Actions for other tasks

## Setup Instructions

### 1. Access Jenkins Server
1. Open https://jenkins.transtechologies.com:18084/
2. Login with your credentials

### 2. Create New Pipeline Job
1. Click "New Item"
2. Enter job name: "HRMS-CI-CD"
3. Select "Pipeline"
4. Click "OK"

### 3. Configure Pipeline
1. In the pipeline configuration:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: https://github.com/harrington40/hr-management-system.git
   - **Branch**: `*/dev` or `*/main`
   - **Script Path**: `Jenkinsfile`

### 4. Configure Credentials
Add the following credentials in Jenkins:

#### Docker Hub Credentials
- **Type**: Username with password
- **ID**: `dockerhub-credentials`
- **Username**: Your Docker Hub username
- **Password**: Docker Hub password/token

#### GitHub Credentials (if using SSH)
- **Type**: SSH Username with private key
- **ID**: `github-ssh-key`
- **Username**: git
- **Private Key**: Your GitHub SSH private key

### 5. Install Required Jenkins Plugins
Ensure these plugins are installed:
- **Pipeline**
- **Pipeline: GitHub Groovy Libraries**
- **Git**
- **Docker Pipeline**
- **Cobertura Plugin** (for coverage reports)
- **HTML Publisher** (for test reports)
- **SSH Agent**

### 6. Configure Build Triggers

#### Option A: Webhook (Recommended)
1. In GitHub repository settings:
   - Go to Settings → Webhooks
   - Add webhook: `https://jenkins.transtechologies.com:18084/github-webhook/`
   - Content type: `application/json`
   - Events: Push, Pull requests

2. In Jenkins job configuration:
   - Check "GitHub hook trigger for GITScm polling"

#### Option B: Poll SCM
- Already configured in Jenkinsfile: `pollSCM('H/5 * * * *')`
- Jenkins checks for changes every 5 minutes

### 7. Environment Setup
Ensure Jenkins agent has:
- **Docker** installed and running
- **Python 3.9+** installed
- **Git** installed
- **Chrome/Chromium** for Selenium tests
- **NSIS** for Windows installer (optional)

## Pipeline Stages

### 1. Security Scan
- Bandit (Python security)
- Safety (dependency vulnerabilities)

### 2. Unit Tests
- pytest with coverage
- HTML and Cobertura reports

### 3. Integration Tests
- API endpoint testing
- Service integration validation

### 4. Regression Tests
- Selenium UI testing
- Cross-browser validation

### 5. Docker Build
- Multi-stage Docker build
- Push to Docker Hub

### 6. Windows Executable Build
- PyInstaller executable creation
- NSIS installer generation

### 7. Deployments
- Test environment (dev branch)
- Staging environment (main branch)
- Production environment (manual approval)

## Monitoring and Notifications

### Build Status
- Jenkins dashboard shows build status
- Email notifications can be configured
- Slack/Teams integration available

### Test Reports
- HTML reports published in Jenkins
- Coverage reports with trends
- Security scan results

## Troubleshooting

### Common Issues

#### Docker Permission Denied
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### Python Dependencies
```bash
# Ensure all dependencies are available
pip3 install -r requirement.txt
```

#### Chrome/Selenium Issues
```bash
# Install Chrome dependencies
apt-get update
apt-get install -y wget gnupg
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable
```

#### Git Authentication
- Use SSH keys for private repositories
- Configure credentials in Jenkins

## Advanced Configuration

### Parallel Stages
```groovy
parallel {
    stage('Unit Tests') {
        // unit test commands
    }
    stage('Integration Tests') {
        // integration test commands
    }
}
```

### Conditional Deployments
```groovy
when {
    allOf {
        branch 'main'
        expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
    }
}
```

### Environment-Specific Variables
```groovy
environment {
    TEST_DB_URL = credentials('test-db-url')
    PROD_DB_URL = credentials('prod-db-url')
}
```

## Security Considerations

### Credentials Management
- Store all secrets in Jenkins credentials store
- Use different credentials for different environments
- Rotate credentials regularly

### Access Control
- Configure job permissions
- Use role-based access control
- Enable audit logging

### Network Security
- Use HTTPS for Jenkins access
- Configure firewall rules
- Use VPN for internal access

## Maintenance

### Regular Tasks
- Update Jenkins and plugins monthly
- Clean up old builds and artifacts
- Monitor disk space usage
- Review and update pipelines

### Backup
- Backup Jenkins configuration
- Export job configurations
- Document custom configurations

## Support

For Jenkins-related issues:
1. Check Jenkins logs: `/var/log/jenkins/jenkins.log`
2. Review build console output
3. Check plugin compatibility
4. Consult Jenkins documentation

## Migration from GitHub Actions

If migrating from GitHub Actions:

1. **Disable GitHub Actions** (optional)
2. **Configure Jenkins webhooks**
3. **Test pipeline thoroughly**
4. **Update documentation**
5. **Train team on Jenkins usage**

## Performance Optimization

### Build Speed
- Use faster build agents
- Cache dependencies
- Parallel test execution
- Optimize Docker layers

### Resource Usage
- Configure appropriate timeouts
- Set resource limits
- Monitor memory usage
- Clean up after builds