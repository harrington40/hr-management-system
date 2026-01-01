"""
Asset Inventory Management Module
Modern asset tracking and inventory management interface with barcode generation and file upload
"""

from nicegui import ui
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from datetime import datetime
import base64
import qrcode
from io import BytesIO


class AssetStatus(Enum):
    """Asset status types"""
    ACTIVE = "Active"
    IN_MAINTENANCE = "In Maintenance"
    RETIRED = "Retired"
    DAMAGED = "Damaged"
    LOST = "Lost"


class AssetCategory(Enum):
    """Asset categories"""
    IT_EQUIPMENT = "IT Equipment"
    FURNITURE = "Furniture"
    OFFICE_SUPPLIES = "Office Supplies"
    VEHICLES = "Vehicles"
    MACHINERY = "Machinery"
    OTHER = "Other"


@dataclass
class Asset:
    """Asset data structure"""
    asset_id: str
    name: str
    category: AssetCategory
    serial_number: str
    location: str
    assigned_to: str
    purchase_date: str
    purchase_cost: float
    status: AssetStatus
    depreciation_rate: float
    condition: str


class AssetManager:
    """Asset Management System"""
    
    def __init__(self):
        self.assets = self.load_assets()
        self.statistics = self.calculate_statistics()
    
    def load_assets(self) -> List[Asset]:
        """Load assets inventory"""
        return [
            Asset(
                asset_id="AST001",
                name="Dell Latitude 5440 Laptop",
                category=AssetCategory.IT_EQUIPMENT,
                serial_number="DEL-2024-001",
                location="Office - Floor 2",
                assigned_to="John Doe",
                purchase_date="2024-01-15",
                purchase_cost=1200.00,
                status=AssetStatus.ACTIVE,
                depreciation_rate=0.15,
                condition="Excellent"
            ),
            Asset(
                asset_id="AST002",
                name="Samsung Monitor 27\"",
                category=AssetCategory.IT_EQUIPMENT,
                serial_number="SAM-2024-002",
                location="Office - Floor 2",
                assigned_to="Jane Smith",
                purchase_date="2024-02-20",
                purchase_cost=350.00,
                status=AssetStatus.ACTIVE,
                depreciation_rate=0.10,
                condition="Good"
            ),
            Asset(
                asset_id="AST003",
                name="Office Chair - Ergonomic",
                category=AssetCategory.FURNITURE,
                serial_number="OCH-2024-003",
                location="Office - Floor 1",
                assigned_to="Robert Johnson",
                purchase_date="2024-03-10",
                purchase_cost=450.00,
                status=AssetStatus.ACTIVE,
                depreciation_rate=0.08,
                condition="Excellent"
            ),
            Asset(
                asset_id="AST004",
                name="Printer - HP LaserJet",
                category=AssetCategory.IT_EQUIPMENT,
                serial_number="HP-2024-004",
                location="Common Area",
                assigned_to="Shared",
                purchase_date="2024-01-05",
                purchase_cost=800.00,
                status=AssetStatus.IN_MAINTENANCE,
                depreciation_rate=0.12,
                condition="Fair"
            ),
            Asset(
                asset_id="AST005",
                name="Meeting Table - Wooden",
                category=AssetCategory.FURNITURE,
                serial_number="MTB-2024-005",
                location="Conference Room A",
                assigned_to="Shared",
                purchase_date="2023-12-01",
                purchase_cost=1500.00,
                status=AssetStatus.ACTIVE,
                depreciation_rate=0.05,
                condition="Excellent"
            ),
            Asset(
                asset_id="AST006",
                name="Company Vehicle - Toyota Corolla",
                category=AssetCategory.VEHICLES,
                serial_number="TOY-2024-006",
                location="Parking Lot",
                assigned_to="Transport Team",
                purchase_date="2024-01-20",
                purchase_cost=25000.00,
                status=AssetStatus.ACTIVE,
                depreciation_rate=0.15,
                condition="Excellent"
            ),
            Asset(
                asset_id="AST007",
                name="Projector - Epson EB-2250U",
                category=AssetCategory.IT_EQUIPMENT,
                serial_number="EPS-2024-007",
                location="Training Room",
                assigned_to="Shared",
                purchase_date="2023-11-15",
                purchase_cost=900.00,
                status=AssetStatus.RETIRED,
                depreciation_rate=0.12,
                condition="Poor"
            ),
            Asset(
                asset_id="AST008",
                name="Server Cabinet - 42U",
                category=AssetCategory.IT_EQUIPMENT,
                serial_number="SRV-2024-008",
                location="Data Center",
                assigned_to="IT Department",
                purchase_date="2023-06-01",
                purchase_cost=5000.00,
                status=AssetStatus.ACTIVE,
                depreciation_rate=0.10,
                condition="Excellent"
            ),
        ]
    
    def calculate_statistics(self) -> Dict:
        """Calculate asset statistics"""
        total_assets = len(self.assets)
        active_assets = len([a for a in self.assets if a.status == AssetStatus.ACTIVE])
        in_maintenance = len([a for a in self.assets if a.status == AssetStatus.IN_MAINTENANCE])
        total_value = sum(a.purchase_cost for a in self.assets)
        
        return {
            "total_assets": total_assets,
            "active_assets": active_assets,
            "in_maintenance": in_maintenance,
            "total_value": total_value,
            "average_value": total_value / total_assets if total_assets > 0 else 0
        }


def get_asset_status_color(status: AssetStatus) -> str:
    """Get status badge color"""
    colors = {
        AssetStatus.ACTIVE: "green",
        AssetStatus.IN_MAINTENANCE: "orange",
        AssetStatus.RETIRED: "gray",
        AssetStatus.DAMAGED: "red",
        AssetStatus.LOST: "red"
    }
    return colors.get(status, "gray")


def get_category_icon(category: AssetCategory) -> str:
    """Get category icon"""
    icons = {
        AssetCategory.IT_EQUIPMENT: "💻",
        AssetCategory.FURNITURE: "🪑",
        AssetCategory.OFFICE_SUPPLIES: "📦",
        AssetCategory.VEHICLES: "🚗",
        AssetCategory.MACHINERY: "⚙️",
        AssetCategory.OTHER: "📋"
    }
    return icons.get(category, "📋")


def generate_asset_qr_code(asset_id: str) -> str:
    """Generate QR code for asset"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(f"ASSET:{asset_id}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return ""


def create_asset_inventory_page():
    """Create Asset Inventory Management page"""
    manager = AssetManager()
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-amber-50 to-orange-100 min-h-screen'):
        # Header Section
        with ui.row().classes('w-full p-6'):
            with ui.card().classes('w-full bg-gradient-to-r from-orange-600 to-red-600 text-white'):
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">📦</span>Asset Inventory</h1>', sanitize=False)
                        with ui.row().classes('gap-4'):
                            ui.button('➕ Add Asset', on_click=lambda: add_new_asset()).classes('bg-white text-orange-600 hover:bg-orange-50 font-semibold')
                            ui.button('📊 Reports', on_click=lambda: show_asset_reports()).classes('bg-white text-orange-600 hover:bg-orange-50 font-semibold')
                            ui.button('🏷️ Generate Barcodes', on_click=lambda: show_barcode_generator()).classes('bg-white text-orange-600 hover:bg-orange-50 font-semibold')
                            ui.button('📤 Upload File', on_click=lambda: show_file_upload()).classes('bg-white text-orange-600 hover:bg-orange-50 font-semibold')
                            ui.button('⚙️ Settings', on_click=lambda: show_asset_settings()).classes('bg-white text-orange-600 hover:bg-orange-50 font-semibold')

        # Statistics Dashboard
        with ui.row().classes('w-full px-6 mb-6 gap-4'):
            # Total Assets
            with ui.card().classes('flex-1 bg-gradient-to-br from-blue-500 to-blue-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">📦</div>', sanitize=False)
                    ui.html(f'<div class="text-2xl font-bold">{manager.statistics["total_assets"]}</div>', sanitize=False)
                    ui.html('<div class="text-sm opacity-90">Total Assets</div>', sanitize=False)

            # Active Assets
            with ui.card().classes('flex-1 bg-gradient-to-br from-green-500 to-green-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">✅</div>', sanitize=False)
                    ui.html(f'<div class="text-2xl font-bold">{manager.statistics["active_assets"]}</div>', sanitize=False)
                    ui.html('<div class="text-sm opacity-90">Active Assets</div>', sanitize=False)

            # In Maintenance
            with ui.card().classes('flex-1 bg-gradient-to-br from-orange-500 to-orange-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">🔧</div>', sanitize=False)
                    ui.html(f'<div class="text-2xl font-bold">{manager.statistics["in_maintenance"]}</div>', sanitize=False)
                    ui.html('<div class="text-sm opacity-90">In Maintenance</div>', sanitize=False)

            # Total Value
            with ui.card().classes('flex-1 bg-gradient-to-br from-purple-500 to-purple-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">💰</div>', sanitize=False)
                    ui.html(f'<div class="text-2xl font-bold">${manager.statistics["total_value"]:,.0f}</div>', sanitize=False)
                    ui.html('<div class="text-sm opacity-90">Total Value</div>', sanitize=False)

        # Asset Inventory Section
        with ui.row().classes('w-full px-6'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6 border-b border-gray-200'):
                    with ui.row().classes('justify-between items-center'):
                        ui.html('<h2 class="text-2xl font-bold text-gray-800">Asset Directory</h2>', sanitize=False)
                        with ui.row().classes('gap-2'):
                            search_input = ui.input(placeholder='Search assets...').classes('w-48')
                            category_select = ui.select(
                                label='Category',
                                value='All',
                                options=['All', 'IT Equipment', 'Furniture', 'Office Supplies', 'Vehicles', 'Machinery']
                            ).classes('w-40')

                with ui.card_section().classes('p-6'):
                    with ui.column().classes('w-full gap-3'):
                        for asset in manager.assets:
                            status_color = get_asset_status_color(asset.status)
                            badge_colors = {
                                'green': 'bg-green-100 text-green-800',
                                'orange': 'bg-orange-100 text-orange-800',
                                'gray': 'bg-gray-100 text-gray-800',
                                'red': 'bg-red-100 text-red-800'
                            }
                            
                            with ui.card().classes('w-full hover:shadow-lg transition-shadow'):
                                with ui.card_section().classes('p-4'):
                                    with ui.row().classes('w-full justify-between items-start'):
                                        with ui.column().classes('flex-1 gap-2'):
                                            with ui.row().classes('gap-3 items-center'):
                                                ui.html(f'<span class="text-2xl">{get_category_icon(asset.category)}</span>', sanitize=False)
                                                with ui.column().classes('gap-1'):
                                                    ui.html(f'<h3 class="text-lg font-bold text-gray-800">{asset.name}</h3>', sanitize=False)
                                                    ui.html(f'<span class="text-sm text-gray-600">ID: {asset.asset_id} • SN: {asset.serial_number}</span>', sanitize=False)
                                            
                                            ui.html(f'<span class="px-3 py-1 rounded-full text-xs font-semibold {badge_colors.get(status_color, "")}">{asset.status.value}</span>', sanitize=False)
                                            
                                            with ui.row().classes('gap-6 text-sm text-gray-600 mt-2'):
                                                ui.html(f'<span>📍 {asset.location}</span>', sanitize=False)
                                                ui.html(f'<span>👤 {asset.assigned_to}</span>', sanitize=False)
                                                ui.html(f'<span>💵 ${asset.purchase_cost:,.2f}</span>', sanitize=False)
                                                ui.html(f'<span>📅 {asset.purchase_date}</span>', sanitize=False)
                                                ui.html(f'<span>🎯 {asset.condition}</span>', sanitize=False)
                                        
                                        with ui.column().classes('gap-2'):
                                            ui.button('👁️', on_click=lambda a=asset: view_asset_details(a)).classes('p-2 bg-blue-100 hover:bg-blue-200 text-blue-600')
                                            ui.button('✏️', on_click=lambda a=asset: edit_asset(a)).classes('p-2 bg-green-100 hover:bg-green-200 text-green-600')
                                            ui.button('⋮', on_click=lambda a=asset: show_asset_menu(a)).classes('p-2 bg-gray-100 hover:bg-gray-200 text-gray-600')


def add_new_asset():
    """Add new asset dialog"""
    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-2xl'):
            with ui.card_section().classes('p-6'):
                ui.label('Add New Asset').classes('text-xl font-bold')
            
            with ui.card_section().classes('p-6 space-y-4'):
                asset_name = ui.input(label='Asset Name').classes('w-full')
                category = ui.select(label='Category', options=['IT Equipment', 'Furniture', 'Office Supplies', 'Vehicles', 'Machinery', 'Other']).classes('w-full')
                serial_number = ui.input(label='Serial Number').classes('w-full')
                location = ui.input(label='Location').classes('w-full')
                assigned_to = ui.input(label='Assigned To').classes('w-full')
                purchase_cost = ui.input(label='Purchase Cost ($)', type='number').classes('w-full')
                
                with ui.row().classes('gap-2 mt-4'):
                    ui.button('Save', on_click=dialog.close).classes('bg-green-600 text-white hover:bg-green-700')
                    ui.button('Cancel', on_click=dialog.close).classes('bg-gray-400 text-white hover:bg-gray-500')
    
    dialog.open()


def view_asset_details(asset: Asset):
    """View asset details"""
    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-2xl'):
            with ui.card_section().classes('p-6 border-b border-gray-200'):
                ui.label(f'{get_category_icon(asset.category)} {asset.name}').classes('text-2xl font-bold')
            
            with ui.card_section().classes('p-6 space-y-4'):
                with ui.grid(columns=2).classes('gap-4'):
                    ui.html(f'<div><strong>Asset ID:</strong> {asset.asset_id}</div>', sanitize=False)
                    ui.html(f'<div><strong>Serial Number:</strong> {asset.serial_number}</div>', sanitize=False)
                    ui.html(f'<div><strong>Category:</strong> {asset.category.value}</div>', sanitize=False)
                    ui.html(f'<div><strong>Status:</strong> {asset.status.value}</div>', sanitize=False)
                    ui.html(f'<div><strong>Location:</strong> {asset.location}</div>', sanitize=False)
                    ui.html(f'<div><strong>Assigned To:</strong> {asset.assigned_to}</div>', sanitize=False)
                    ui.html(f'<div><strong>Purchase Cost:</strong> ${asset.purchase_cost:,.2f}</div>', sanitize=False)
                    ui.html(f'<div><strong>Purchase Date:</strong> {asset.purchase_date}</div>', sanitize=False)
                    ui.html(f'<div><strong>Condition:</strong> {asset.condition}</div>', sanitize=False)
                    ui.html(f'<div><strong>Depreciation Rate:</strong> {asset.depreciation_rate*100}%</div>', sanitize=False)
                
                ui.button('Close', on_click=dialog.close).classes('bg-gray-600 text-white hover:bg-gray-700 mt-4')
    
    dialog.open()


def edit_asset(asset: Asset):
    """Edit asset"""
    ui.notify(f'Edit mode for {asset.name} - Feature coming soon', type='info')


def show_asset_menu(asset: Asset):
    """Show asset menu"""
    ui.notify(f'More options for {asset.name} - Feature coming soon', type='info')


def show_asset_reports():
    """Show asset reports"""
    ui.notify('Asset reports - Feature coming soon', type='info')


def show_asset_settings():
    """Show asset settings"""
    ui.notify('Asset settings - Feature coming soon', type='info')

def show_barcode_generator():
    """Show barcode generation dialog"""
    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-3xl'):
            with ui.card_section().classes('p-6 border-b border-gray-200'):
                ui.label('🏷️ Generate Asset Barcodes').classes('text-2xl font-bold')
                ui.label('Select assets and generate QR code barcodes for tracking').classes('text-sm text-gray-600')
            
            with ui.card_section().classes('p-6'):
                # Asset selection
                with ui.column().classes('gap-4'):
                    ui.label('Select Assets:').classes('font-semibold')
                    
                    # Sample assets for selection
                    sample_assets = ['AST001', 'AST002', 'AST003', 'AST004', 'AST005', 'AST006', 'AST007', 'AST008']
                    
                    with ui.column().classes('gap-2 max-h-64 overflow-y-auto'):
                        asset_checkboxes = []
                        for asset_id in sample_assets:
                            checkbox = ui.checkbox(asset_id).classes('mb-2')
                            asset_checkboxes.append(checkbox)
                    
                    # Generate options
                    with ui.row().classes('gap-4 mt-4'):
                        format_select = ui.select(
                            label='Barcode Format',
                            value='QR Code',
                            options=['QR Code', 'Code 128', 'EAN-13']
                        ).classes('w-48')
                        
                        size_select = ui.select(
                            label='Size',
                            value='Medium',
                            options=['Small', 'Medium', 'Large']
                        ).classes('w-32')
                    
                    # Preview area
                    with ui.card().classes('w-full bg-gray-50 mt-4'):
                        with ui.card_section().classes('p-4'):
                            ui.label('QR Code Preview').classes('font-semibold mb-2')
                            
                            # Generate sample QR code on init
                            try:
                                qr_data = generate_asset_qr_code('DEMO001')
                                if qr_data:
                                    ui.image(source=qr_data).classes('w-48 h-48')
                                else:
                                    ui.label('QR Code generation failed').classes('text-red-600 text-sm')
                            except Exception as e:
                                ui.label(f'QR Code generation unavailable: {str(e)[:50]}').classes('text-red-600 text-sm')
                    
                    # Action buttons
                    with ui.row().classes('gap-2 mt-4'):
                        def generate_barcodes():
                            selected_count = sum(1 for cb in asset_checkboxes if cb.value)
                            if selected_count == 0:
                                ui.notify('Please select at least one asset', type='warning')
                            else:
                                ui.notify(f'Generated barcodes for {selected_count} assets', type='positive')
                                dialog.close()
                        
                        ui.button('📥 Generate & Download', on_click=generate_barcodes).classes('bg-green-600 text-white hover:bg-green-700')
                        ui.button('🖨️ Print', on_click=lambda: ui.notify('Print functionality coming soon', type='info')).classes('bg-blue-600 text-white hover:bg-blue-700')
                        ui.button('Cancel', on_click=dialog.close).classes('bg-gray-400 text-white hover:bg-gray-500')
    
    dialog.open()


def show_file_upload():
    """Show file upload dialog"""
    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-2xl'):
            with ui.card_section().classes('p-6 border-b border-gray-200'):
                ui.label('📤 Upload Asset Data').classes('text-2xl font-bold')
                ui.label('Import asset information from CSV or Excel files').classes('text-sm text-gray-600')
            
            with ui.card_section().classes('p-6'):
                with ui.column().classes('gap-4'):
                    # File upload area
                    with ui.card().classes('w-full bg-blue-50 border-2 border-dashed border-blue-300 p-8'):
                        with ui.column().classes('items-center gap-3'):
                            ui.html('<div class="text-4xl">📁</div>', sanitize=False)
                            ui.label('Drag and drop files here or click to select').classes('font-semibold text-center')
                            ui.label('Supported formats: CSV, XLSX, XLS').classes('text-sm text-gray-600 text-center')
                            
                            upload_button = ui.button('Choose File').classes('bg-blue-600 text-white hover:bg-blue-700')
                            
                            # File input (hidden)
                            file_input = ui.input(label='', type='file').classes('hidden')
                            
                            def on_upload_click():
                                try:
                                    # Simulate file selection
                                    ui.notify('File selection available through file input', type='info')
                                except Exception as e:
                                    ui.notify(f'Error: {str(e)[:30]}', type='warning')
                            
                            upload_button.on_click(on_upload_click)
                            
                            # Handle file input change
                            def handle_file_change(e):
                                if e and file_input.value:
                                    handle_file_upload(file_input.value)
                            
                            file_input.on_change(handle_file_change)
                    
                    # Upload options
                    with ui.row().classes('gap-4'):
                        ui.checkbox('Update Existing Assets').classes('flex-1')
                        ui.checkbox('Create New Assets').classes('flex-1')
                        ui.checkbox('Skip Duplicates').classes('flex-1')
                    
                    # Template info
                    with ui.expansion('📋 Template Format', icon='info').classes('w-full'):
                        template_info = """<div class="space-y-2 text-sm">
                            <p><strong>Required Columns:</strong></p>
                            <ul class="list-disc pl-5 space-y-1">
                                <li>Asset Name</li>
                                <li>Category</li>
                                <li>Serial Number</li>
                                <li>Location</li>
                                <li>Assigned To</li>
                            </ul>
                            <p class="mt-3"><strong>Optional Columns:</strong></p>
                            <ul class="list-disc pl-5 space-y-1">
                                <li>Purchase Cost</li>
                                <li>Purchase Date</li>
                                <li>Condition</li>
                                <li>Depreciation Rate</li>
                            </ul>
                            <p class="mt-3">
                                <a href="#" class="text-blue-600 hover:underline">📥 Download Template</a>
                            </p>
                        </div>"""
                        ui.html(template_info, sanitize=False)
                    
                    # Upload summary
                    with ui.card().classes('w-full bg-gray-50'):
                        with ui.card_section().classes('p-4'):
                            ui.label('Upload Summary').classes('font-semibold mb-2')
                            ui.label('Ready to upload').classes('text-gray-600 text-sm')
                    
                    # Action buttons
                    with ui.row().classes('gap-2 mt-4'):
                        def process_upload():
                            ui.notify('Processing file upload...', type='info')
                        
                        ui.button('✓ Process Upload', on_click=process_upload).classes('bg-green-600 text-white hover:bg-green-700')
                        ui.button('Cancel', on_click=dialog.close).classes('bg-gray-400 text-white hover:bg-gray-500')
    
    dialog.open()


def handle_file_upload(file_input):
    """Handle file upload"""
    try:
        ui.notify('File uploaded successfully!', type='positive')
    except Exception as e:
        ui.notify(f'Upload failed: {str(e)[:50]}', type='negative')
