#!/usr/bin/env python3
"""
Diagnostic script to check for rendering issues
"""
import sys
import traceback

print("=" * 60)
print("HRMS DIAGNOSTICS")
print("=" * 60)

# Test 1: Check imports
print("\n[1] Testing imports...")
try:
    from nicegui import ui
    print("✓ NiceGUI import successful")
except Exception as e:
    print(f"✗ NiceGUI import failed: {e}")
    traceback.print_exc()

# Test 2: Check asset inventory module
print("\n[2] Testing asset_inventory module...")
try:
    from components.reports.asset_inventory import (
        create_asset_inventory_page,
        generate_asset_qr_code,
        show_barcode_generator,
        show_file_upload,
        handle_file_upload
    )
    print("✓ asset_inventory imports successful")
    print("  - create_asset_inventory_page: OK")
    print("  - generate_asset_qr_code: OK")
    print("  - show_barcode_generator: OK")
    print("  - show_file_upload: OK")
    print("  - handle_file_upload: OK")
except ImportError as e:
    print(f"✗ Import error: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    traceback.print_exc()

# Test 3: Check layout subpages
print("\n[3] Testing layout.subpages...")
try:
    from layout import subpages
    print("✓ layout.subpages import successful")
except Exception as e:
    print(f"✗ layout.subpages import failed: {e}")
    traceback.print_exc()

# Test 4: Check QR code generation
print("\n[4] Testing QR code generation...")
try:
    from components.reports.asset_inventory import generate_asset_qr_code
    qr = generate_asset_qr_code("TEST001")
    if qr and qr.startswith("data:image/png;base64,"):
        print(f"✓ QR code generation working (length: {len(qr)} chars)")
    else:
        print(f"✗ QR code generation returned unexpected format")
except Exception as e:
    print(f"✗ QR code generation failed: {e}")
    traceback.print_exc()

# Test 5: Syntax check asset_inventory.py
print("\n[5] Syntax check...")
try:
    import py_compile
    py_compile.compile('components/reports/asset_inventory.py', doraise=True)
    print("✓ asset_inventory.py syntax valid")
except py_compile.PyCompileError as e:
    print(f"✗ Syntax error in asset_inventory.py:")
    print(e)

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)
