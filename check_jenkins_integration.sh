#!/bin/bash

# Jenkins-HRMS Integration Diagnostic Report
# ==========================================

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        Jenkins-HRMS Integration Diagnostic Report              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Jenkins Configuration
JENKINS_URL="https://jenkins.transtechologies.com:18084/"

echo "📋 Test 1: Jenkins Server Connectivity"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Jenkins URL: $JENKINS_URL"
echo ""

# Test DNS resolution
echo -n "DNS Resolution: "
if host jenkins.transtechologies.com >/dev/null 2>&1; then
    IP=$(host jenkins.transtechologies.com | grep "has address" | awk '{print $4}' | head -n1)
    echo -e "${GREEN}✓ Success${NC} - Resolved to: $IP"
else
    echo -e "${RED}✗ Failed${NC} - Cannot resolve hostname"
fi

# Test connectivity
echo -n "Port 18084 Connectivity: "
if timeout 5 bash -c "</dev/tcp/jenkins.transtechologies.com/18084" 2>/dev/null; then
    echo -e "${GREEN}✓ Success${NC} - Port is open"
else
    echo -e "${RED}✗ Failed${NC} - Cannot connect to port 18084"
fi

# Test HTTPS endpoint
echo -n "HTTPS Endpoint: "
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" -m 10 "$JENKINS_URL" 2>/dev/null)
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 403 ] || [ "$HTTP_CODE" -eq 401 ]; then
    echo -e "${GREEN}✓ Success${NC} - HTTP Status: $HTTP_CODE"
else
    echo -e "${RED}✗ Failed${NC} - HTTP Status: ${HTTP_CODE:-timeout/error}"
fi

echo ""
echo "📋 Test 2: Local HRMS Application Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if application is running
echo -n "Application Status: "
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
    
    # Get health check data
    HEALTH_DATA=$(curl -s http://localhost:8000/health)
    echo "Health Check Response:"
    echo "$HEALTH_DATA" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_DATA"
else
    echo -e "${RED}✗ Not Running${NC}"
    echo ""
    echo "To start the application, run:"
    echo "  python3 run_dual_services.py"
    echo "  or"
    echo "  python3 main.py"
fi

echo ""
echo "📋 Test 3: Application Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if health endpoint is defined
echo -n "Health Endpoint in Code: "
if grep -q "/health" main.py 2>/dev/null; then
    echo -e "${GREEN}✓ Defined${NC} (in main.py)"
else
    echo -e "${YELLOW}⚠ Not found in main.py${NC}"
fi

# Check Jenkinsfile
echo -n "Jenkinsfile Present: "
if [ -f "Jenkinsfile" ]; then
    echo -e "${GREEN}✓ Yes${NC}"
    echo "   Pipeline stages: $(grep -c "stage(" Jenkinsfile) stages"
else
    echo -e "${RED}✗ No${NC}"
fi

# Check Jenkins documentation
echo -n "Jenkins Documentation: "
if [ -f "JENKINS_README.md" ]; then
    echo -e "${GREEN}✓ Yes${NC}"
else
    echo -e "${YELLOW}⚠ No${NC}"
fi

echo ""
echo "📋 Test 4: CI/CD Integration Points"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for Jenkins-related files
echo "Jenkins-related files:"
for file in Jenkinsfile* jenkins-*.sh jenkins-*.xml JENKINS_*.md; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    fi
done

# Check for test files
echo ""
echo -n "Test Files: "
TEST_COUNT=$(find tests/ -name "test_*.py" 2>/dev/null | wc -l)
if [ "$TEST_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Found $TEST_COUNT test files${NC}"
else
    echo -e "${YELLOW}⚠ No test files found${NC}"
fi

# Check requirements.txt
echo -n "Dependencies File: "
if [ -f "requirements.txt" ]; then
    DEP_COUNT=$(wc -l < requirements.txt)
    echo -e "${GREEN}✓ requirements.txt${NC} ($DEP_COUNT dependencies)"
else
    echo -e "${RED}✗ requirements.txt missing${NC}"
fi

echo ""
echo "📋 Test 5: Network Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if port 8000 is available
echo -n "Port 8000 Status: "
if netstat -tuln 2>/dev/null | grep -q ":8000 " || ss -tuln 2>/dev/null | grep -q ":8000 "; then
    echo -e "${GREEN}✓ In use (app running)${NC}"
else
    echo -e "${YELLOW}⚠ Available (app not running)${NC}"
fi

# Check internet connectivity
echo -n "Internet Connectivity: "
if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Connected${NC}"
else
    echo -e "${RED}✗ No connection${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "                          SUMMARY                              "
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 403 ] || [ "$HTTP_CODE" -eq 401 ]; then
    echo -e "${GREEN}✓ Jenkins Server:${NC} Reachable"
else
    echo -e "${RED}✗ Jenkins Server:${NC} Connection timeout or network issue"
    echo ""
    echo "  Possible reasons:"
    echo "  1. Firewall blocking port 18084"
    echo "  2. Jenkins server is down"
    echo "  3. Network connectivity issues"
    echo "  4. VPN or proxy configuration needed"
fi

if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✓ HRMS Application:${NC} Running and responding"
    echo ""
    echo "  The app is ready for Jenkins CI/CD operations"
else
    echo -e "${YELLOW}⚠ HRMS Application:${NC} Not currently running"
    echo ""
    echo "  Start the application with:"
    echo "  $ python3 run_dual_services.py"
fi

echo ""
echo "📚 Additional Information:"
echo "   - Jenkins pipelines are configured in Jenkinsfile"
echo "   - Health endpoint: http://localhost:8000/health"
echo "   - Jenkins performs smoke tests via the /health endpoint"
echo "   - See JENKINS_README.md for detailed integration guide"
echo ""
