# HRMS CI/CD Pipeline

This document describes the comprehensive CI/CD pipeline implemented for the HRMS (Human Resource Management System) application.

## Overview

The CI/CD pipeline provides automated testing, building, and deployment across three environments:
- **Test**: Automated testing and validation
- **Staging**: Pre-production environment with integration testing
- **Production**: Live production environment

## Pipeline Structure

### 1. Security & Quality Scan
- **Bandit**: Python security vulnerability scanner
- **Safety**: Dependency vulnerability checker
- Runs on every push and pull request

### 2. Unit Tests
- Comprehensive unit test coverage (>80%)
- PostgreSQL test database
- Coverage reporting with HTML and XML outputs
- Runs pytest with coverage analysis

### 3. Integration Tests
- End-to-end API testing
- Application startup validation
- Database connectivity tests
- Service integration verification

### 4. Regression Tests
- Selenium-based UI regression testing
- Cross-browser compatibility
- Performance regression checks
- Responsive design validation

### 5. Docker Build
- Multi-stage Docker build
- Automated tagging (branch, PR, SHA)
- Docker Hub integration

### 6. Environment Deployments
- **Test**: Automated deployment on dev branch pushes
- **Staging**: Deployed on main branch pushes
- **Production**: Manual deployment approval required

## File Structure

```
.github/
├── workflows/
│   └── cicd-pipeline.yml          # Main CI/CD workflow

config/
├── test.env                       # Test environment config
├── staging.env                    # Staging environment config
└── production.env                 # Production environment config

k8s/
├── test/                          # Test environment K8s manifests
├── staging/                       # Staging environment K8s manifests
└── production/
    └── deployment.yml             # Production K8s deployment

tests/
├── unit/                          # Unit tests
│   └── test_components.py
├── integration/                   # Integration tests
│   └── test_application.py
└── regression/                    # Regression tests
    └── test_ui_regression.py

Dockerfile                         # Multi-stage Docker build
docker-compose.yml                 # Local development setup
pytest.ini                        # Pytest configuration
.dockerignore                      # Docker build exclusions
```

## Environment Variables

### Required Secrets (GitHub Repository Secrets)

#### Docker Hub
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/token

#### Test Environment
- `TEST_URL`: Test environment URL for smoke tests

#### Staging Environment
- `STAGING_URL`: Staging environment URL
- `SMTP_USERNAME`: Email service username
- `SMTP_PASSWORD`: Email service password
- `SENTRY_DSN_STAGING`: Sentry DSN for staging
- `NEW_RELIC_LICENSE_KEY_STAGING`: New Relic license for staging

#### Production Environment
- `PRODUCTION_URL`: Production environment URL
- `PRODUCTION_SECRET_KEY`: Application secret key
- `PRODUCTION_JWT_SECRET_KEY`: JWT secret key
- `SMTP_USERNAME`: Email service username
- `SMTP_PASSWORD`: Email service password
- `SENTRY_DSN_PRODUCTION`: Sentry DSN for production
- `NEW_RELIC_LICENSE_KEY_PRODUCTION`: New Relic license for production

## Local Development

### Running Tests Locally

```bash
# Install dependencies
pip install -r requirement.txt

# Run unit tests
pytest tests/unit/ -v --cov=. --cov-report=html

# Run integration tests
pytest tests/integration/ -v

# Run regression tests (requires Chrome)
pytest tests/regression/ -v

# Run all tests
pytest tests/ -v --cov=. --cov-report=html
```

### Docker Development

```bash
# Build and run with docker-compose
docker-compose up --build

# Run tests in Docker
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Deployment Instructions

### Test Environment
- Automatically deployed on pushes to `dev` branch
- No manual intervention required
- Used for automated testing validation

### Staging Environment
- Automatically deployed on pushes to `main` branch
- Includes integration and performance testing
- Accessible for user acceptance testing

### Production Environment
- Manual deployment via GitHub Actions workflow dispatch
- Requires approval from designated reviewers
- Includes full regression testing before deployment

## Monitoring and Alerts

### Health Checks
- Application health endpoint: `/health`
- Database connectivity monitoring
- Service dependency checks

### Logging
- Structured logging with environment-specific levels
- Centralized log aggregation (recommended: ELK stack)
- Error tracking with Sentry integration

### Metrics
- Application Performance Monitoring (APM) with New Relic
- Custom business metrics tracking
- Infrastructure monitoring

## Security Considerations

### Code Security
- Automated dependency vulnerability scanning
- Static application security testing (SAST)
- Container image vulnerability scanning

### Infrastructure Security
- Non-root container execution
- Secret management with Kubernetes secrets
- Network policies and security contexts

### Access Control
- Environment-specific secrets management
- Branch protection rules
- Required reviews for production deployments

## Troubleshooting

### Common Issues

1. **Test Failures**
   - Check database connectivity
   - Verify test data setup
   - Review application logs

2. **Docker Build Failures**
   - Check Dockerfile syntax
   - Verify base image availability
   - Review build logs for dependency issues

3. **Deployment Failures**
   - Check environment-specific configurations
   - Verify secrets are properly set
   - Review Kubernetes cluster status

### Debugging Commands

```bash
# Check pipeline status
gh run list --workflow=cicd-pipeline.yml

# View detailed logs
gh run view <run-id> --log

# Check deployment status
kubectl get pods -n hrms-production
kubectl logs -f deployment/hrms-app -n hrms-production
```

## Contributing

### Adding New Tests
1. Create test files in appropriate directories (`tests/unit/`, `tests/integration/`, `tests/regression/`)
2. Follow naming convention: `test_*.py`
3. Add test markers for categorization
4. Update this documentation

### Modifying Pipeline
1. Edit `.github/workflows/cicd-pipeline.yml`
2. Test changes on feature branch
3. Update documentation
4. Create pull request for review

## Support

For pipeline-related issues:
1. Check GitHub Actions logs
2. Review deployment manifests
3. Contact DevOps team
4. Create issue in project repository