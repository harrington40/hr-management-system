# Jenkins Job Configuration Fix

## Problem
Jenkins job "HRMS-CI-CD" is failing because:
- SCM is not configured (using NullSCM)
- Repository not checked out
- Jenkinsfile not found in workspace

## Solution: Complete Job Reconfiguration

### Step 1: Access Jenkins
1. Go to: https://jenkins.transtechologies.com:18084/
2. Login with your credentials

### Step 2: Configure the Job
1. Click on "HRMS-CI-CD" job
2. Click "Configure" on the left menu

### Step 3: Set Up Source Code Management
In the "Source Code Management" section:

1. **Select "Git"**
2. **Repository URL**: `https://github.com/harrington40/hr-management-system.git`
3. **Credentials**: Click "Add" → "Jenkins"
   - **Kind**: Username with password
   - **Username**: Your GitHub username
   - **Password**: Your GitHub Personal Access Token (PAT)
   - **ID**: `github-pat`
   - **Description**: GitHub PAT for HRMS repo
4. **Branch Specifier**: `*/dev` (or `*/main` if you want to use main branch)
5. **Repository browser**: (Optional) GitHub
   - URL: `https://github.com/harrington40/hr-management-system`

### Step 4: Configure Build Triggers
In the "Build Triggers" section:

1. Check "Poll SCM"
2. Schedule: `H/5 * * * *` (check every 5 minutes)

**OR** (Recommended for better performance):

1. Check "GitHub hook trigger for GITScm polling"

### Step 5: Configure Pipeline
In the "Pipeline" section:

1. **Definition**: `Pipeline script from SCM`
2. **SCM**: `Git` (should be auto-selected from step 3)
3. **Script Path**: `Jenkinsfile` (this should be default)

### Step 6: Save and Test
1. Click "Save"
2. Click "Build Now" to test the configuration

## Alternative: Quick Fix for Existing Job

If you want to keep the existing job structure:

1. Go to job configuration
2. In "Pipeline" section:
   - Change "Definition" to: `Pipeline script from SCM`
   - Select "Git" in SCM
   - Enter repository URL and credentials as above
   - Script Path: `Jenkinsfile`

## GitHub Webhook Setup (Recommended)

For automatic builds on Git push:

### In GitHub:
1. Go to repository Settings → Webhooks
2. Click "Add webhook"
3. **Payload URL**: `https://jenkins.transtechologies.com:18084/github-webhook/`
4. **Content type**: `application/json`
5. **Secret**: (leave empty for now)
6. **Events**: Select "Just the push event"
7. Click "Add webhook"

### In Jenkins:
1. Install "GitHub Integration Plugin" if not installed
2. In job configuration, check "GitHub hook trigger for GITScm polling"

## Verification Steps

After configuration:

1. **Check Repository Connection**:
   - In job configuration, click "Save" then go back to config
   - Look for "Repository URL" - there should be a ✅ if connection works

2. **Test Build**:
   - Click "Build Now"
   - Check console output for successful checkout

3. **Verify Jenkinsfile Detection**:
   - Console should show: "Checking out Git repository..."
   - Then: "Obtained Jenkinsfile from [commit hash]"

## Troubleshooting

### If Still Getting Errors:

1. **Check Credentials**:
   ```bash
   # Test GitHub PAT
   curl -H "Authorization: token YOUR_PAT" https://api.github.com/user
   ```

2. **Test Repository Access**:
   ```bash
   git clone https://YOUR_USERNAME:YOUR_PAT@github.com/harrington40/hr-management-system.git
   ```

3. **Check Jenkins Logs**:
   - Go to Jenkins logs: `/var/log/jenkins/jenkins.log`
   - Look for Git or SCM related errors

4. **Verify Branch**:
   - Make sure the branch you specified exists
   - Jenkinsfile must be in the root of that branch

### Common Issues:

- **"Repository not found"**: Check repository URL and credentials
- **"Branch not found"**: Verify branch name (dev vs main)
- **"Jenkinsfile not found"**: Ensure file exists in repository root
- **Permission denied**: Check GitHub PAT permissions

## Expected Successful Output

After proper configuration, you should see in build console:

```
Started by user [your username]
Checking out Git repository...
Cloning repository https://github.com/harrington40/hr-management-system.git
 > git init /var/lib/jenkins/workspace/HRMS-CI-CD
 > git fetch --tags --force --progress -- https://github.com/harrington40/hr-management-system.git +refs/heads/*:refs/remotes/origin/*
 > git config remote.origin.url https://github.com/harrington40/hr-management-system.git
 > git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/*
 > git checkout -b dev remotes/origin/dev
Obtained Jenkinsfile from [commit hash]
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
...
```

## Next Steps

Once the job is working:

1. **Run a test build** to verify all stages work
2. **Configure webhooks** for automatic triggering
3. **Set up notifications** (email, Slack, etc.)
4. **Add build parameters** if needed for different environments

The Jenkinsfile is ready and comprehensive - it includes all the stages we configured in GitHub Actions!