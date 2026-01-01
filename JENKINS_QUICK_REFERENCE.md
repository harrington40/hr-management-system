# Jenkins CI/CD Quick Reference

## 🚀 Three Pipeline Overview

### 1. **TEST Environment** (`Jenkinsfile.test`)
- **Trigger**: Automatic on push to `develop` branch
- **Port**: 8081
- **Database**: `hrms_test`
- **Purpose**: Continuous testing and development
- **Notifications**: dev-team@company.com

**Stages:**
```
Pipeline Info → Checkout → Validate → Setup Python → 
Unit Tests → Security Scan → Build → Docker Build → 
Push Image → Deploy Test → Smoke Tests → Reports
```

### 2. **STAGING Environment** (`Jenkinsfile.staging`)
- **Trigger**: Automatic on merge to `main` branch
- **Port**: 8082
- **Database**: `hrms_staging`
- **Purpose**: Pre-production validation and QA
- **Notifications**: qa-team@company.com, dev-leads@company.com

**Stages:**
```
Pipeline Info → Checkout → Validation → Setup Python → 
Full Test Suite → Security & Compliance → Build → 
Docker Build → Container Scan → Push Registry → 
Backup DB → Deploy Staging → Integration Tests → 
Performance Tests → Reports
```

### 3. **PRODUCTION Environment** (`Jenkinsfile.production`)
- **Trigger**: **MANUAL ONLY** (requires approval)
- **Port**: 8080
- **Database**: `hrms_production`
- **Purpose**: Live production deployment
- **Notifications**: engineering-leads@company.com, devops@company.com, cto@company.com

**Stages:**
```
Pipeline Info → Manual Approval → Checkout → 
Pre-Production Validation → Setup Python → 
Pre-Deployment Tests → Security Check → 
Backup Production DB → Build Release → 
Docker Build → Push Registry → Deploy Production → 
Health Checks → Smoke Tests → Monitor Metrics → 
Notify Stakeholders
```

## 📋 Quick Commands

### Manual Pipeline Trigger
```bash
# Trigger via Jenkins CLI (if installed)
java -jar jenkins-cli.jar -s http://jenkins-url/ build HRMS-Test-Pipeline

# Or use curl
curl -X POST http://jenkins-url/job/HRMS-Test-Pipeline/build \
  --user username:token
```

### Check Pipeline Status
```bash
# Check running pipelines
curl http://jenkins-url/api/json | jq '.jobs[] | {name: .name, color: .color}'
```

### Manual Deployment (Bypassing Jenkins)
```bash
# Test Environment
./scripts/deploy-test.sh

# Staging Environment
./scripts/deploy-staging.sh

# Production Environment
./scripts/deploy-production.sh
```

## 🔄 Git Workflow

### For Test Deployment
```bash
git checkout develop
git add .
git commit -m "feat: add new feature"
git push origin develop
# ✅ Automatically triggers Test pipeline
```

### For Staging Deployment
```bash
git checkout main
git merge develop
git push origin main
# ✅ Automatically triggers Staging pipeline
```

### For Production Deployment
```bash
# 1. Ensure staging is stable
# 2. Go to Jenkins → HRMS-Production-Pipeline
# 3. Click "Build with Parameters"
# 4. Select deployment type
# 5. Approve deployment
# 6. Monitor deployment progress
```

## 🔧 Environment Variables

Each environment uses different configs:

### Test (`config/test.env`)
```env
ENVIRONMENT=test
APP_PORT=8081
ORIENTDB_DATABASE=hrms_test
LOG_LEVEL=DEBUG
```

### Staging (`config/staging.env`)
```env
ENVIRONMENT=staging
APP_PORT=8082
ORIENTDB_DATABASE=hrms_staging
LOG_LEVEL=INFO
```

### Production (`config/production.env`)
```env
ENVIRONMENT=production
APP_PORT=8080
ORIENTDB_DATABASE=hrms_production
LOG_LEVEL=WARNING
MONITORING_ENABLED=true
```

## 🐳 Docker Tags

Each environment uses specific tags:

### Test
- `harrington40/hrms-app:test-{BUILD_NUMBER}`
- `harrington40/hrms-app:test-latest`

### Staging
- `harrington40/hrms-app:staging-{BUILD_NUMBER}`
- `harrington40/hrms-app:staging-latest`
- `harrington40/hrms-app:staging-stable`

### Production
- `harrington40/hrms-app:prod-{BUILD_NUMBER}`
- `harrington40/hrms-app:production-latest`
- `harrington40/hrms-app:stable`

## 📊 Monitoring Deployment

### Check Application Status
```bash
# Test
curl http://test-hrms.company.local:8081/health

# Staging
curl http://staging-hrms.company.local:8082/health

# Production
curl https://hrms.company.com/health
```

### View Application Logs
```bash
# Test
tail -f logs/test.log

# Staging
tail -f logs/staging.log

# Production
tail -f logs/production.log
```

### Check Running Processes
```bash
# View all uvicorn instances
ps aux | grep uvicorn

# Test (port 8081)
ps aux | grep "uvicorn.*8081"

# Staging (port 8082)
ps aux | grep "uvicorn.*8082"

# Production (port 8080)
ps aux | grep "uvicorn.*8080"
```

## 🔄 Rollback Procedures

### Test Environment
```bash
# Stop and redeploy previous version
pkill -f "uvicorn.*8081"
git checkout <previous-commit>
./scripts/deploy-test.sh
```

### Staging Environment
```bash
# Trigger new build with previous commit
git checkout main
git reset --hard <previous-commit>
git push --force origin main
# Or manually deploy previous Docker image
```

### Production Environment
```bash
# Use Jenkins rollback parameter
# 1. Go to HRMS-Production-Pipeline
# 2. Build with Parameters
# 3. Set ROLLBACK_VERSION to previous version
# 4. Approve and deploy
```

## 🚨 Emergency Stop

### Stop All Environments
```bash
# Stop all HRMS instances
pkill -f "uvicorn main:app"

# Or stop individually
pkill -f "uvicorn.*8081"  # Test
pkill -f "uvicorn.*8082"  # Staging
pkill -f "uvicorn.*8080"  # Production
```

## 📧 Notification Channels

### Test Failures
- **Email**: dev-team@company.com
- **Slack**: #hrms-test-deployments

### Staging Issues
- **Email**: qa-team@company.com, dev-leads@company.com
- **Slack**: #hrms-staging-deployments

### Production Alerts
- **Email**: engineering-leads@company.com, devops@company.com, cto@company.com
- **Slack**: #hrms-production-deployments
- **PagerDuty**: (Configure if available)

## 🔐 Security Notes

### Required Credentials
- `dockerhub-credentials`: Docker Hub access
- `github-credentials`: GitHub repository access
- `datadog-api-key`: Monitoring (optional)

### Access Control
- **Test**: All developers
- **Staging**: QA team + Senior developers
- **Production**: DevOps + Engineering leads only

## 📈 Success Metrics

Monitor these after deployment:

✅ Health check responds (200 OK)
✅ Application logs show no errors
✅ CPU/Memory usage is normal
✅ Database connections stable
✅ Response times < 500ms
✅ No error spike in monitoring

## 🆘 Troubleshooting

### Pipeline Won't Trigger
- Check GitHub webhook configuration
- Verify branch names match
- Check Jenkins system log

### Tests Failing
- Review test output in Jenkins
- Run tests locally: `pytest tests/`
- Check dependencies: `pip list`

### Deployment Failed
- Check port availability: `netstat -tlnp | grep 808`
- Verify database connectivity
- Review application logs
- Check disk space: `df -h`

### Docker Build Issues
- Verify Dockerfile syntax
- Check Docker daemon: `docker ps`
- Review Docker build logs

---

**Quick Help**: See full documentation in `JENKINS_MULTI_ENV_SETUP.md`
