"""
HR Administration Module
Modern HR administration interface for policies, compliance, and organizational management
"""

from nicegui import ui
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from datetime import datetime, timedelta


class PolicyStatus(Enum):
    """Policy status types"""
    ACTIVE = "Active"
    DRAFT = "Draft"
    ARCHIVED = "Archived"
    PENDING_APPROVAL = "Pending Approval"


class ComplianceStatus(Enum):
    """Compliance status"""
    COMPLIANT = "Compliant"
    AT_RISK = "At Risk"
    NON_COMPLIANT = "Non-Compliant"
    PENDING_REVIEW = "Pending Review"


@dataclass
class HRPolicy:
    """HR Policy data structure"""
    policy_id: str
    title: str
    category: str
    description: str
    status: PolicyStatus
    last_updated: str
    version: str
    affected_employees: int


@dataclass
class ComplianceItem:
    """Compliance checklist item"""
    item_id: str
    title: str
    category: str
    status: ComplianceStatus
    due_date: str
    responsible_person: str
    progress: int


class HRAdministrationManager:
    """HR Administration Manager"""
    
    def __init__(self):
        self.policies = self.load_policies()
        self.compliance_items = self.load_compliance_items()
        self.kpis = self.calculate_kpis()
    
    def load_policies(self) -> List[HRPolicy]:
        """Load HR policies"""
        return [
            HRPolicy(
                policy_id="POL001",
                title="Code of Conduct",
                category="Governance",
                description="Defines ethical standards and employee behavior expectations",
                status=PolicyStatus.ACTIVE,
                last_updated="2025-11-15",
                version="3.2",
                affected_employees=150
            ),
            HRPolicy(
                policy_id="POL002",
                title="Leave Policy",
                category="Time Off",
                description="Annual leave, sick leave, and special leave provisions",
                status=PolicyStatus.ACTIVE,
                last_updated="2025-10-20",
                version="2.1",
                affected_employees=150
            ),
            HRPolicy(
                policy_id="POL003",
                title="Workplace Safety",
                category="Safety",
                description="Health and safety guidelines for all work environments",
                status=PolicyStatus.ACTIVE,
                last_updated="2025-09-10",
                version="4.0",
                affected_employees=150
            ),
            HRPolicy(
                policy_id="POL004",
                title="Remote Work Policy",
                category="Flexibility",
                description="Guidelines for remote and hybrid work arrangements",
                status=PolicyStatus.DRAFT,
                last_updated="2025-11-25",
                version="1.0",
                affected_employees=85
            ),
            HRPolicy(
                policy_id="POL005",
                title="Performance Management",
                category="Development",
                description="Annual appraisal and performance review process",
                status=PolicyStatus.ACTIVE,
                last_updated="2025-08-05",
                version="2.5",
                affected_employees=150
            ),
        ]
    
    def load_compliance_items(self) -> List[ComplianceItem]:
        """Load compliance items"""
        return [
            ComplianceItem(
                item_id="COMP001",
                title="Employee Records Audit",
                category="Documentation",
                status=ComplianceStatus.COMPLIANT,
                due_date="2025-12-31",
                responsible_person="HR Manager",
                progress=100
            ),
            ComplianceItem(
                item_id="COMP002",
                title="Safety Training Certification",
                category="Training",
                status=ComplianceStatus.AT_RISK,
                due_date="2025-12-15",
                responsible_person="Safety Officer",
                progress=75
            ),
            ComplianceItem(
                item_id="COMP003",
                title="Annual Compensation Review",
                category="Compensation",
                status=ComplianceStatus.PENDING_REVIEW,
                due_date="2026-01-15",
                responsible_person="CFO",
                progress=40
            ),
            ComplianceItem(
                item_id="COMP004",
                title="Benefits Enrollment Updates",
                category="Benefits",
                status=ComplianceStatus.COMPLIANT,
                due_date="2025-12-10",
                responsible_person="Benefits Admin",
                progress=100
            ),
            ComplianceItem(
                item_id="COMP005",
                title="Diversity & Inclusion Report",
                category="Reporting",
                status=ComplianceStatus.NON_COMPLIANT,
                due_date="2025-11-30",
                responsible_person="HR Director",
                progress=20
            ),
        ]
    
    def calculate_kpis(self) -> Dict:
        """Calculate HR KPIs"""
        return {
            "total_employees": 150,
            "active_policies": len([p for p in self.policies if p.status == PolicyStatus.ACTIVE]),
            "compliance_rate": 80,
            "training_completion": 85,
            "employee_satisfaction": 7.8,
            "retention_rate": 92
        }


def get_status_badge_color(status) -> str:
    """Get badge color based on status"""
    if isinstance(status, PolicyStatus):
        colors = {
            PolicyStatus.ACTIVE: "green",
            PolicyStatus.DRAFT: "blue",
            PolicyStatus.ARCHIVED: "gray",
            PolicyStatus.PENDING_APPROVAL: "orange"
        }
        return colors.get(status, "gray")
    elif isinstance(status, ComplianceStatus):
        colors = {
            ComplianceStatus.COMPLIANT: "green",
            ComplianceStatus.AT_RISK: "orange",
            ComplianceStatus.NON_COMPLIANT: "red",
            ComplianceStatus.PENDING_REVIEW: "blue"
        }
        return colors.get(status, "gray")
    return "gray"


def create_hr_administration_page():
    """Create HR Administration page"""
    manager = HRAdministrationManager()
    
    with ui.column().classes('w-full h-full bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen'):
        # Header Section
        with ui.row().classes('w-full p-6'):
            with ui.card().classes('w-full bg-gradient-to-r from-blue-600 to-indigo-700 text-white'):
                with ui.card_section().classes('p-6'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.html('<h1 class="text-3xl font-bold flex items-center gap-3"><span class="text-4xl">📋</span>HR Administration</h1>')
                        with ui.row().classes('gap-4'):
                            ui.button('📝 Create Policy', on_click=lambda: create_policy_dialog()).classes('bg-white text-blue-600 hover:bg-blue-50 font-semibold')
                            ui.button('✅ Compliance Check', on_click=lambda: show_compliance_dialog()).classes('bg-white text-blue-600 hover:bg-blue-50 font-semibold')
                            ui.button('📊 Reports', on_click=lambda: show_reports()).classes('bg-white text-blue-600 hover:bg-blue-50 font-semibold')

        # KPI Dashboard
        with ui.row().classes('w-full px-6 mb-6 gap-4'):
            # Total Employees
            with ui.card().classes('flex-1 bg-gradient-to-br from-blue-500 to-blue-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">👥</div>')
                    ui.html(f'<div class="text-2xl font-bold">{manager.kpis["total_employees"]}</div>')
                    ui.html('<div class="text-sm opacity-90">Total Employees</div>')

            # Active Policies
            with ui.card().classes('flex-1 bg-gradient-to-br from-green-500 to-green-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">📄</div>')
                    ui.html(f'<div class="text-2xl font-bold">{manager.kpis["active_policies"]}</div>')
                    ui.html('<div class="text-sm opacity-90">Active Policies</div>')

            # Compliance Rate
            with ui.card().classes('flex-1 bg-gradient-to-br from-orange-500 to-orange-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">✅</div>')
                    ui.html(f'<div class="text-2xl font-bold">{manager.kpis["compliance_rate"]}%</div>')
                    ui.html('<div class="text-sm opacity-90">Compliance Rate</div>')

            # Employee Satisfaction
            with ui.card().classes('flex-1 bg-gradient-to-br from-purple-500 to-purple-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">😊</div>')
                    ui.html(f'<div class="text-2xl font-bold">{manager.kpis["employee_satisfaction"]}/10</div>')
                    ui.html('<div class="text-sm opacity-90">Employee Satisfaction</div>')

            # Retention Rate
            with ui.card().classes('flex-1 bg-gradient-to-br from-red-500 to-red-600 text-white'):
                with ui.card_section().classes('p-4 text-center'):
                    ui.html('<div class="text-3xl font-bold">📈</div>')
                    ui.html(f'<div class="text-2xl font-bold">{manager.kpis["retention_rate"]}%</div>')
                    ui.html('<div class="text-sm opacity-90">Retention Rate</div>')

        # Policies Section
        with ui.row().classes('w-full px-6 mb-6'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6 border-b border-gray-200'):
                    ui.html('<h2 class="text-2xl font-bold text-gray-800 mb-4">📚 HR Policies</h2>')
                
                with ui.card_section().classes('p-6'):
                    # Policies Table
                    with ui.column().classes('w-full'):
                        for policy in manager.policies:
                            with ui.card().classes('w-full mb-3 hover:shadow-lg transition-shadow'):
                                with ui.card_section().classes('p-4'):
                                    with ui.row().classes('w-full justify-between items-start'):
                                        with ui.column().classes('flex-1 gap-2'):
                                            with ui.row().classes('gap-2 items-center'):
                                                ui.html(f'<h3 class="text-lg font-bold text-gray-800">{policy.title}</h3>')
                                                status_color = get_status_badge_color(policy.status)
                                                badge_colors = {
                                                    'green': 'bg-green-100 text-green-800',
                                                    'blue': 'bg-blue-100 text-blue-800',
                                                    'orange': 'bg-orange-100 text-orange-800',
                                                    'gray': 'bg-gray-100 text-gray-800'
                                                }
                                                ui.html(f'<span class="px-3 py-1 rounded-full text-xs font-semibold {badge_colors.get(status_color, "")}">{policy.status.value}</span>')
                                            
                                            ui.html(f'<p class="text-sm text-gray-600">{policy.description}</p>')
                                            
                                            with ui.row().classes('gap-4 text-sm text-gray-500 mt-2'):
                                                ui.html(f'<span>📁 Category: {policy.category}</span>')
                                                ui.html(f'<span>👥 Affects: {policy.affected_employees} employees</span>')
                                                ui.html(f'<span>📅 v{policy.version} • Updated: {policy.last_updated}</span>')
                                        
                                        with ui.column().classes('gap-2'):
                                            ui.button('👁️', on_click=lambda p=policy: view_policy(p)).classes('p-2 bg-blue-100 hover:bg-blue-200 text-blue-600')
                                            ui.button('✏️', on_click=lambda p=policy: edit_policy(p)).classes('p-2 bg-green-100 hover:bg-green-200 text-green-600')
                                            ui.button('⋮', on_click=lambda p=policy: show_policy_menu(p)).classes('p-2 bg-gray-100 hover:bg-gray-200 text-gray-600')

        # Compliance Section
        with ui.row().classes('w-full px-6'):
            with ui.card().classes('w-full'):
                with ui.card_section().classes('p-6 border-b border-gray-200'):
                    with ui.row().classes('justify-between items-center'):
                        ui.html('<h2 class="text-2xl font-bold text-gray-800">✅ Compliance Checklist</h2>')
                        ui.button('+ Add Item', on_click=lambda: add_compliance_item()).classes('bg-green-600 text-white hover:bg-green-700')
                
                with ui.card_section().classes('p-6'):
                    with ui.column().classes('w-full gap-3'):
                        for item in manager.compliance_items:
                            status_color = get_status_badge_color(item.status)
                            badge_colors = {
                                'green': 'bg-green-100 text-green-800',
                                'orange': 'bg-orange-100 text-orange-800',
                                'red': 'bg-red-100 text-red-800',
                                'blue': 'bg-blue-100 text-blue-800',
                                'gray': 'bg-gray-100 text-gray-800'
                            }
                            
                            with ui.card().classes('w-full bg-gray-50 hover:bg-gray-100 transition-colors'):
                                with ui.card_section().classes('p-4'):
                                    with ui.row().classes('w-full items-center gap-4'):
                                        # Progress bar
                                        with ui.column().classes('w-20'):
                                            ui.html(f'<div class="text-center text-sm font-bold text-gray-700">{item.progress}%</div>')
                                            with ui.linear_progress(value=item.progress / 100).classes('w-full'):
                                                pass
                                        
                                        # Item details
                                        with ui.column().classes('flex-1 gap-1'):
                                            with ui.row().classes('gap-2 items-center'):
                                                ui.html(f'<strong class="text-gray-800">{item.title}</strong>')
                                                ui.html(f'<span class="px-2 py-1 rounded-full text-xs font-semibold {badge_colors.get(status_color, "")}">{item.status.value}</span>')
                                            
                                            with ui.row().classes('gap-4 text-xs text-gray-600'):
                                                ui.html(f'<span>📂 {item.category}</span>')
                                                ui.html(f'<span>👤 {item.responsible_person}</span>')
                                                ui.html(f'<span>📅 Due: {item.due_date}</span>')
                                        
                                        # Actions
                                        with ui.row().classes('gap-2'):
                                            ui.button('📝', on_click=lambda i=item: edit_compliance_item(i)).classes('p-2 bg-blue-100 hover:bg-blue-200 text-blue-600')
                                            ui.button('✓', on_click=lambda i=item: mark_compliance_done(i)).classes('p-2 bg-green-100 hover:bg-green-200 text-green-600')


def create_policy_dialog():
    """Create new policy dialog"""
    with ui.dialog() as dialog:
        with ui.card().classes('w-full'):
            with ui.card_section().classes('p-6'):
                ui.label('Create New HR Policy').classes('text-xl font-bold')
            
            with ui.card_section().classes('p-6 space-y-4'):
                title_input = ui.input(label='Policy Title', placeholder='e.g., Flexible Work Hours').classes('w-full')
                category_select = ui.select(
                    label='Category',
                    value='Governance',
                    options=['Governance', 'Time Off', 'Safety', 'Flexibility', 'Development', 'Compensation']
                ).classes('w-full')
                description_input = ui.textarea(label='Description', placeholder='Policy details...').classes('w-full')
                
                with ui.row().classes('gap-2 mt-4'):
                    ui.button('Save', on_click=dialog.close).classes('bg-green-600 text-white hover:bg-green-700')
                    ui.button('Cancel', on_click=dialog.close).classes('bg-gray-400 text-white hover:bg-gray-500')
    
    dialog.open()


def view_policy(policy: HRPolicy):
    """View policy details"""
    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-2xl'):
            with ui.card_section().classes('p-6 border-b border-gray-200'):
                ui.label(policy.title).classes('text-2xl font-bold')
            
            with ui.card_section().classes('p-6 space-y-4'):
                ui.html(f'<p><strong>Policy ID:</strong> {policy.policy_id}</p>')
                ui.html(f'<p><strong>Category:</strong> {policy.category}</p>')
                ui.html(f'<p><strong>Description:</strong> {policy.description}</p>')
                ui.html(f'<p><strong>Version:</strong> {policy.version}</p>')
                ui.html(f'<p><strong>Last Updated:</strong> {policy.last_updated}</p>')
                ui.html(f'<p><strong>Affected Employees:</strong> {policy.affected_employees}</p>')
                
                ui.button('Close', on_click=dialog.close).classes('bg-gray-600 text-white hover:bg-gray-700 mt-4')
    
    dialog.open()


def edit_policy(policy: HRPolicy):
    """Edit policy"""
    ui.notify(f'Edit mode for {policy.title} - Feature coming soon', type='info')


def show_policy_menu(policy: HRPolicy):
    """Show policy menu"""
    ui.notify(f'More options for {policy.title} - Feature coming soon', type='info')


def show_compliance_dialog():
    """Show compliance check dialog"""
    ui.notify('Compliance check - Feature coming soon', type='info')


def show_reports():
    """Show reports view"""
    ui.notify('Reports view - Feature coming soon', type='info')


def add_compliance_item():
    """Add new compliance item"""
    ui.notify('Add compliance item - Feature coming soon', type='info')


def edit_compliance_item(item: ComplianceItem):
    """Edit compliance item"""
    ui.notify(f'Edit {item.title} - Feature coming soon', type='info')


def mark_compliance_done(item: ComplianceItem):
    """Mark compliance item as done"""
    ui.notify(f'{item.title} marked as complete', type='positive')
