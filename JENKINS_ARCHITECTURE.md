# Jenkins CI/CD Pipeline Architecture

## 📊 Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DEVELOPER WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────┘

    Developer pushes code
            ↓
    ┌───────────────┐
    │  Git Branch   │
    └───────────────┘
            ↓
    ┌───────┬───────┬───────┐
    │       │       │       │
 develop   main   release   
    │       │       │       
    ↓       ↓       ↓       

┌─────────────────────────────────────────────────────────────────────┐
│                     THREE PIPELINE ENVIRONMENTS                      │
└─────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════╗
║                      🧪 TEST PIPELINE                              ║
║  Jenkinsfile.test                                                  ║
╠═══════════════════════════════════════════════════════════════════╣
║  Trigger: Auto on push to 'develop'                               ║
║  Port: 8081 | Database: hrms_test                                 ║
╠═══════════════════════════════════════════════════════════════════╣
║  1. 📋 Pipeline Info                                              ║
║  2. 🔄 Checkout Code                                              ║
║  3. 🔍 Validate Environment                                       ║
║  4. 🐍 Setup Python (venv + pip install)                         ║
║  5. 🧪 Run Unit Tests (pytest + coverage)                        ║
║  6. 🔒 Security Scan (safety + bandit)                           ║
║  7. 🏗️  Build Application                                         ║
║  8. 🐳 Build Docker Image (test-{BUILD})                         ║
║  9. 🔍 Docker Image Scan                                          ║
║  10. 📤 Push to Registry                                          ║
║  11. 🚀 Deploy to Test (uvicorn on 8081)                         ║
║  12. 🧪 Smoke Tests                                               ║
║  13. 📊 Generate Reports                                          ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✉️  Notify: dev-team@company.com                                ║
╚═══════════════════════════════════════════════════════════════════╝
                          ↓ (If all tests pass)
                          
╔═══════════════════════════════════════════════════════════════════╗
║                    🎯 STAGING PIPELINE                            ║
║  Jenkinsfile.staging                                              ║
╠═══════════════════════════════════════════════════════════════════╣
║  Trigger: Auto on merge to 'main'                                ║
║  Port: 8082 | Database: hrms_staging                             ║
╠═══════════════════════════════════════════════════════════════════╣
║  1. 📋 Pipeline Info                                             ║
║  2. 🔄 Checkout Code                                             ║
║  3. 🔍 Pre-deployment Validation                                 ║
║  4. 🐍 Setup Python Environment                                  ║
║  5. 🧪 Run Full Test Suite                                       ║
║  6. 🔒 Security & Compliance Scan                                ║
║  7. 🏗️  Build Application                                        ║
║  8. 🐳 Build & Tag Docker (staging-{BUILD})                     ║
║  9. 🔍 Container Security Scan (Trivy)                          ║
║  10. 📤 Push to Registry (multi-tag)                             ║
║  11. 💾 Backup Staging Database                                  ║
║  12. 🚀 Deploy to Staging (uvicorn on 8082)                     ║
║  13. 🧪 Integration Tests                                        ║
║  14. ⚡ Performance Tests (locust)                               ║
║  15. 📊 Generate Deployment Report                               ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✉️  Notify: qa-team@company.com, dev-leads@company.com         ║
╚═══════════════════════════════════════════════════════════════════╝
                          ↓ (Manual decision)
                          
╔═══════════════════════════════════════════════════════════════════╗
║                   🚀 PRODUCTION PIPELINE                          ║
║  Jenkinsfile.production                                           ║
╠═══════════════════════════════════════════════════════════════════╣
║  Trigger: MANUAL ONLY (requires approval)                        ║
║  Port: 8080 | Database: hrms_production                          ║
╠═══════════════════════════════════════════════════════════════════╣
║  1. 📋 Production Pipeline Info                                  ║
║  2. 🔐 MANUAL APPROVAL REQUIRED ⚠️                               ║
║  3. 🔄 Checkout Code                                             ║
║  4. 🔍 Pre-Production Validation                                 ║
║  5. 🐍 Setup Production Environment                              ║
║  6. 🧪 Pre-Deployment Tests                                      ║
║  7. 🔒 Security Final Check                                      ║
║  8. 💾 Create Production Backup ⚠️                               ║
║  9. 🏗️  Build Production Release                                ║
║  10. 🐳 Build Production Docker (prod-{BUILD})                   ║
║  11. 📤 Push Production Images                                    ║
║  12. 🚀 Deploy to Production (Rolling/Blue-Green/Canary)        ║
║  13. 🏥 Health Checks (retry logic)                              ║
║  14. 🧪 Production Smoke Tests                                   ║
║  15. 📊 Monitor Initial Metrics                                  ║
║  16. 📢 Notify Stakeholders                                      ║
╠═══════════════════════════════════════════════════════════════════╣
║  Parameters:                                                      ║
║  • DEPLOYMENT_TYPE (rolling/blue-green/canary)                   ║
║  • SKIP_TESTS (not recommended)                                  ║
║  • CREATE_BACKUP (recommended: true)                             ║
║  • ROLLBACK_VERSION (for rollbacks)                              ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✉️  Notify: engineering-leads@, devops@, cto@company.com       ║
╚═══════════════════════════════════════════════════════════════════╝


┌─────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT TARGETS                            │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   TEST SERVER    │    │  STAGING SERVER  │    │   PRODUCTION     │
│                  │    │                  │    │                  │
│ Port: 8081       │    │ Port: 8082       │    │ Port: 8080       │
│ DB: hrms_test    │    │ DB: hrms_staging │    │ DB: hrms_prod    │
│ Workers: 1       │    │ Workers: 2       │    │ Workers: 4       │
│ Log: DEBUG       │    │ Log: INFO        │    │ Log: WARNING     │
│                  │    │                  │    │                  │
│ Auto-deployed    │    │ Auto-deployed    │    │ Manual-only      │
└──────────────────┘    └──────────────────┘    └──────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                      DOCKER IMAGE FLOW                               │
└─────────────────────────────────────────────────────────────────────┘

                          ┌────────────┐
                          │  Build     │
                          │  Dockerfile│
                          └─────┬──────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ↓               ↓               ↓
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  TEST IMAGE  │ │ STAGING IMG  │ │  PROD IMAGE  │
        │              │ │              │ │              │
        │ test-{BUILD} │ │ staging-{#}  │ │ prod-{BUILD} │
        │ test-latest  │ │ staging-     │ │ production-  │
        │              │ │  latest      │ │  latest      │
        │              │ │ staging-     │ │ stable       │
        │              │ │  stable      │ │              │
        └──────────────┘ └──────────────┘ └──────────────┘
                │               │               │
                └───────────────┼───────────────┘
                                ↓
                        ┌──────────────┐
                        │ Docker Hub   │
                        │ Registry     │
                        │ harrington40/│
                        │  hrms-app    │
                        └──────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    GITHUB WEBHOOK INTEGRATION                        │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   GitHub     │
│  Repository  │
└──────┬───────┘
       │
       │  Push to 'develop' branch
       ├─────────────────────────────────► TEST Pipeline
       │
       │  Merge to 'main' branch  
       ├─────────────────────────────────► STAGING Pipeline
       │
       │  Manual trigger only
       └─────────────────────────────────► PRODUCTION Pipeline
                                            (Requires approval)


┌─────────────────────────────────────────────────────────────────────┐
│                    MONITORING & NOTIFICATIONS                        │
└─────────────────────────────────────────────────────────────────────┘

Each pipeline sends notifications:

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   SUCCESS   │     │   FAILURE   │     │  UNSTABLE   │
│     ✅      │     │     ❌      │     │     ⚠️      │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       ↓                   ↓                   ↓
┌──────────────────────────────────────────────────────┐
│           Email Notifications                        │
│  - Test: dev-team@company.com                       │
│  - Staging: qa-team@, dev-leads@company.com        │
│  - Production: engineering-leads@, devops@, cto@   │
└──────────────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────┐
│           Slack Notifications (optional)             │
│  - #hrms-test-deployments                           │
│  - #hrms-staging-deployments                        │
│  - #hrms-production-deployments                     │
└──────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                       ROLLBACK CAPABILITY                            │
└─────────────────────────────────────────────────────────────────────┘

Production Pipeline supports rollback:

1. Trigger Pipeline with Parameters
2. Set ROLLBACK_VERSION = "prod-123"
3. Approve rollback
4. Pipeline deploys previous version
5. Verify health checks
6. Notify team

┌──────────────────────────────────────────────────────────────────┐
│ Rollback Time: ~5-10 minutes                                    │
│ Data Restoration: From backup (if needed)                       │
│ Zero Downtime: Yes (using deployment strategies)                │
└──────────────────────────────────────────────────────────────────┘
```

## 🔐 Security Layers

Each pipeline includes multiple security checks:

```
┌─────────────────────────────────────────────────────┐
│  1. Code Security (Bandit)                         │
│     ↓                                              │
│  2. Dependency Vulnerabilities (Safety)            │
│     ↓                                              │
│  3. Container Scanning (Trivy)                     │
│     ↓                                              │
│  4. License Compliance                             │
│     ↓                                              │
│  5. Manual Approval (Production only)              │
└─────────────────────────────────────────────────────┘
```

## 📊 Reports Generated

Each pipeline generates:
- ✅ Test Results (JUnit XML)
- ✅ Code Coverage (HTML + XML)
- ✅ Security Reports (JSON)
- ✅ Deployment Reports (TXT)
- ✅ Build Metadata (JSON)

---

**Version**: 1.0.0  
**Last Updated**: December 31, 2025
