# Jenkins Multi-Environment CI/CD Setup Guide

This guide explains how to set up three separate Jenkins pipelines for Test, Staging, and Production environments.

## 📋 Overview

Three independent Jenkins pipelines have been created:
- **Jenkinsfile.test** - Test environment (auto-deploy on push)
- **Jenkinsfile.staging** - Staging environment (auto-deploy on merge)
- **Jenkinsfile.production** - Production environment (manual approval required)

## 🚀 Quick Setup

### Step 1: Create Jenkins Jobs

Create three separate **Pipeline** jobs in Jenkins:

1. **HRMS-Test-Pipeline**
2. **HRMS-Staging-Pipeline**
3. **HRMS-Production-Pipeline**

### Step 2: Configure Each Pipeline

For each job, configure the following:

#### A. General Settings
- ✅ GitHub project URL: `https://github.com/yourusername/hr`
- ✅ Discard old builds: Keep last 30 builds (Test), 50 (Staging), 100 (Production)

#### B. Build Triggers

**Test Pipeline:**
- ✅ GitHub hook trigger for GITScm polling
- ✅ Poll SCM: `H/5 * * * *` (every 5 minutes as fallback)
- Branch to build: `develop` or `test`

**Staging Pipeline:**
- ✅ GitHub hook trigger for GITScm polling
- ✅ Poll SCM: `H/10 * * * *` (every 10 minutes)
- Branch to build: `main` or `staging`

**Production Pipeline:**
- ✅ Manual trigger only (no automatic triggers)
- Branch to build: `main` or `release/*`

#### C. Pipeline Configuration

For each job, select **Pipeline script from SCM**:

- **Test Pipeline:**
  - SCM: Git
  - Repository URL: Your Git URL
  - Branch: `*/develop`
  - Script Path: `Jenkinsfile.test`

- **Staging Pipeline:**
  - SCM: Git
  - Repository URL: Your Git URL
  - Branch: `*/main`
  - Script Path: `Jenkinsfile.staging`

- **Production Pipeline:**
  - SCM: Git
  - Repository URL: Your Git URL
  - Branch: `*/main`
  - Script Path: `Jenkinsfile.production`

## 🔧 Required Jenkins Plugins

Install these plugins via Jenkins → Manage Jenkins → Plugin Manager:

```
- Pipeline
- Git
- GitHub Integration
- Docker Pipeline
- Email Extension
- HTML Publisher
- JUnit
- Workspace Cleanup
- Timestamper
- Build Timeout
```

## 🔐 Configure Credentials

Add the following credentials in Jenkins → Manage Jenkins → Credentials:

1. **dockerhub-credentials** (Username with password)
   - ID: `dockerhub-credentials`
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password/token

2. **github-credentials** (SSH key or Personal Access Token)
   - For GitHub access

3. **datadog-api-key** (Secret text) - Optional
   - For monitoring integration

## 🎯 GitHub Webhook Configuration

### Enable Automatic Triggers on Push/Merge

1. Go to your GitHub repository → Settings → Webhooks
2. Click **Add webhook**
3. Configure:
   ```
   Payload URL: http://your-jenkins-url/github-webhook/
   Content type: application/json
   Events: 
     ✅ Pushes
     ✅ Pull requests
   Active: ✅ Yes
   ```

4. Click **Add webhook**

## 📊 Pipeline Flow

### Test Environment (Automatic)
```
Push to develop → GitHub Webhook → Jenkins Test Pipeline
↓
Checkout → Setup Env → Run Tests → Build → Deploy to Test
↓
Smoke Tests → Notify Team
```

### Staging Environment (Automatic on Merge)
```
Merge to main → GitHub Webhook → Jenkins Staging Pipeline
↓
Checkout → Full Test Suite → Security Scan → Build
↓
Deploy to Staging → Integration Tests → Performance Tests
↓
Notify QA Team
```

### Production Environment (Manual)
```
Manual Trigger → Manual Approval Required
↓
Pre-deployment Checks → Backup Production DB
↓
Build Production Release → Deploy (Rolling/Blue-Green/Canary)
↓
Health Checks → Smoke Tests → Monitor Metrics
↓
Notify Stakeholders
```

## 🌍 Environment Configuration

### Port Assignments
- **Test**: Port 8081
- **Staging**: Port 8082
- **Production**: Port 8080

### Database Configuration
Each environment uses a separate database:
- **Test**: `hrms_test`
- **Staging**: `hrms_staging`
- **Production**: `hrms_production`

## 📧 Email Notifications

Configure email notifications in Jenkins → Manage Jenkins → System:

1. Extended E-mail Notification
   - SMTP server: `smtp.gmail.com`
   - SMTP Port: `587`
   - Use SSL/TLS: ✅
   - Credentials: Add your email credentials

2. Configure recipient lists:
   - Test: `dev-team@company.com`
   - Staging: `qa-team@company.com, dev-leads@company.com`
   - Production: `engineering-leads@company.com, devops@company.com, cto@company.com`

## 🔒 Security & Permissions

### Access Control

Configure Jenkins security to restrict production deployments:

1. Go to Manage Jenkins → Security
2. Set up Matrix-based security or Role-based security
3. Restrict production pipeline access:
   - Only senior engineers can approve production deployments
   - Create `prod-deploy-group` with appropriate members

## 🚀 Deployment Strategies

### Production supports three strategies:

1. **Rolling Deployment** (Default)
   - Gradually replace old instances with new ones
   - Zero downtime
   - Easy rollback

2. **Blue-Green Deployment**
   - Deploy to inactive environment
   - Switch traffic after validation
   - Instant rollback capability

3. **Canary Deployment**
   - Deploy to subset of instances
   - Monitor metrics
   - Gradual rollout

Select strategy via pipeline parameters when triggering production build.

## 📋 Pipeline Parameters (Production)

When triggering production pipeline:

- **DEPLOYMENT_TYPE**: Choose deployment strategy
- **SKIP_TESTS**: Skip pre-deployment tests (not recommended)
- **CREATE_BACKUP**: Create database backup (recommended: ✅)
- **ROLLBACK_VERSION**: Specify version for rollback (leave empty for normal deployment)

## 🔄 Rollback Procedure

To rollback production:

1. Trigger Production Pipeline
2. Set **ROLLBACK_VERSION** parameter to previous stable version
3. Approve deployment
4. Pipeline will deploy the specified version

## 📊 Monitoring & Reports

Each pipeline generates:
- ✅ Test results (JUnit XML)
- ✅ Code coverage reports (HTML)
- ✅ Security scan reports (JSON)
- ✅ Deployment reports (TXT)

Access reports via Jenkins job → Build → Test Results / HTML Reports

## 🐛 Troubleshooting

### Pipeline Fails to Start
- Check GitHub webhook is configured
- Verify Jenkins has access to repository
- Check branch names match configuration

### Docker Build Fails
- Verify Docker is installed on Jenkins node
- Check Docker Hub credentials are configured
- Ensure Dockerfile exists in repository

### Tests Fail
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Review test logs in Jenkins console

### Deployment Fails
- Check port availability
- Verify database connectivity
- Review application logs
- Check disk space and system resources

## 📞 Support

For issues with the CI/CD pipeline:
1. Check Jenkins console output
2. Review pipeline logs
3. Contact DevOps team: `devops@company.com`

## 📚 Additional Resources

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Docker Pipeline Plugin](https://plugins.jenkins.io/docker-workflow/)
- [GitHub Integration](https://plugins.jenkins.io/github/)

---

**Last Updated**: December 31, 2025
**Version**: 1.0.0
