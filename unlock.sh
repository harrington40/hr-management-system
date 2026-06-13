#!/bin/bash
# =============================================================================
# HRMS Unlock Script — Run on the target machine after git pull
# Enables the license YAML flag so the app runs without a signed license file.
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LICENSE_YAML="$SCRIPT_DIR/config/license.yaml"

echo "🔓 HRMS License Unlock"
echo ""

if [ ! -f "$LICENSE_YAML" ]; then
    echo "❌ config/license.yaml not found. Is this run from the project root?"
    exit 1
fi

# Check if already active
if grep -q "active: true" "$LICENSE_YAML"; then
    echo "✅ License already active — no changes needed."
    exit 0
fi

# Enable the YAML fallback license
echo "📝 Enabling license (YAML fallback mode)..."
python3 -c "
import yaml
from pathlib import Path

path = Path('$LICENSE_YAML')
data = yaml.safe_load(path.read_text())
data['license']['active'] = True
data['license']['plan'] = 'Dev/Demo'
data['license']['seats'] = 999
path.write_text(yaml.dump(data, default_flow_style=False))
print('  ✅ license.active → True')
print('  ✅ plan → Dev/Demo')
print('  ✅ seats → 999')
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ License unlocked! The app will now run in dev/demo mode."
echo "  ▶️  Start the app:  ./start.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
