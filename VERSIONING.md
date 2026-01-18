# HRMS Version and Package Management

## Version Management

The HRMS application uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Current Version
```
1.0.0
```

### Updating Version

#### Using the bump-version script (Linux/Mac):
```bash
# Bump patch version (1.0.0 -> 1.0.1)
./bump-version.sh patch

# Bump minor version (1.0.0 -> 1.1.0)
./bump-version.sh minor

# Bump major version (1.0.0 -> 2.0.0)
./bump-version.sh major
```

#### Manual update:
1. Edit `VERSION` file
2. Update `__version__` in `__init__.py`
3. Commit changes
4. Tag the release: `git tag -a v1.0.1 -m "Release 1.0.1"`

## Package Naming Convention

### Test Environment
- **Format**: `hrms-{VERSION}-test.{BUILD_NUMBER}.tar.gz`
- **Example**: `hrms-1.0.0-test.42.tar.gz`
- **Purpose**: Development and testing builds

### Staging Environment
- **Format**: `hrms-{VERSION}-staging.{BUILD_NUMBER}.tar.gz`
- **Example**: `hrms-1.0.0-staging.15.tar.gz`
- **Purpose**: Pre-production validation

### Production Environment
- **Format**: `hrms-{VERSION}.tar.gz`
- **Example**: `hrms-1.0.0.tar.gz`
- **Also Creates**: `hrms-{VERSION}-prod.{BUILD_NUMBER}.tar.gz`
- **Purpose**: Production releases

## Jenkins Build Versions

Each environment generates version-tagged packages:

| Environment | Version Format | Example | Docker Tag |
|------------|----------------|---------|------------|
| **Test** | `{VERSION}-test.{BUILD}` | `1.0.0-test.42` | `1.0.0-test.42` |
| **Staging** | `{VERSION}-staging.{BUILD}` | `1.0.0-staging.15` | `1.0.0-staging.15` |
| **Production** | `{VERSION}` | `1.0.0` | `1.0.0` |

## Package Contents

Each package includes:
- ✅ Application source code
- ✅ Configuration templates
- ✅ Requirements.txt
- ✅ Build metadata (build-info.json)
- ✅ Checksums (SHA256, MD5)
- ✅ Release notes
- ✅ Deployment manifest

## Test Coverage Requirements

### Test Environment
- **Minimum Coverage**: 60%
- **Reports Generated**:
  - HTML Coverage Report
  - XML Coverage Report (for CI/CD)
  - JSON Coverage Report
  - Terminal Summary
  - Markdown Summary

### Staging Environment
- **Minimum Coverage**: 70%
- **Additional Checks**:
  - Security scans
  - License compliance
  - Performance tests

### Production Environment
- **Requirement**: Must pass all staging tests
- **Additional Validation**:
  - Pre-deployment test suite
  - Security final check
  - Database backup verification

## Accessing Build Artifacts

### In Jenkins
1. Navigate to the build
2. Click "Build Artifacts"
3. Download:
   - `packages/{environment}/*.tar.gz` - Application package
   - `build-info.json` - Build metadata
   - `coverage.xml` - Coverage report
   - `htmlcov/` - HTML coverage report

### Package Structure
```
hrms-1.0.0.tar.gz
├── main.py
├── requirements.txt
├── config/
├── components/
├── services/
├── build-info.json
└── ...
```

## Deployment Process

### 1. Test Environment (Automatic)
- Triggered on push to `develop` or `test` branch
- Runs full test suite with coverage
- Creates test package: `hrms-{VERSION}-test.{BUILD}.tar.gz`
- Deploys to test server

### 2. Staging Environment (Automatic)
- Triggered on merge to `main` or `staging` branch
- Runs comprehensive tests
- Creates staging package: `hrms-{VERSION}-staging.{BUILD}.tar.gz`
- Deploys to staging server

### 3. Production Environment (Manual Approval)
- Triggered manually after staging validation
- Requires manual approval
- Creates production release: `hrms-{VERSION}.tar.gz`
- Deploys with chosen strategy (rolling/blue-green/canary)

## Version History Tracking

All versions are tracked in:
- Git tags (`v1.0.0`, `v1.0.1`, etc.)
- Jenkins build artifacts
- Package names
- Docker image tags

## Best Practices

1. **Always test in Test environment first**
2. **Validate in Staging before Production**
3. **Keep VERSION file updated**
4. **Tag releases in Git**
5. **Maintain changelog**
6. **Archive production packages**
7. **Monitor test coverage trends**

## Coverage Report Access

### HTML Reports
- Available in Jenkins: Build → Coverage Report
- Local: Open `htmlcov/index.html`

### CI/CD Integration
- XML format for SonarQube, Codecov
- JSON format for custom dashboards
- JUnit XML for test results

## Troubleshooting

### Package not created
- Check Jenkins console output
- Verify VERSION file exists
- Check disk space

### Low coverage warning
- Review coverage report
- Add missing tests
- Update .coveragerc exclusions

### Deployment fails
- Verify package checksums
- Check server resources
- Review deployment logs
