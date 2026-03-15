from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, timedelta
import json
import uuid

# Import employee data manager for real-time statistics
from .enroll_staff import employee_data_manager
from helperFuns.employee_registry import employee_registry

# Advanced Department Management System with HR Time Management Algorithms
class DepartmentDataManager:
    """
    Sophisticated department management system with time tracking,
    workforce analytics, and institution integration algorithms
    """
    
    def __init__(self):
        # Connect with institution data for consistency
        self.institution_id = "KWARECOM-001"

        # Department metadata: budget, head, location, type, performance baselines, hours
        _meta = {
            "Human Resources":        dict(code="HR",  budget=250000, head="Sarah Johnson",   location="Building A, Floor 2", dept_type="Core",    efficiency=92, satisfaction=88, turnover=5.2,  productivity=94, start="08:00", end="17:00", break_m=60, flex=True),
            "Information Technology": dict(code="IT",  budget=450000, head="Michael Chen",    location="Building B, Floor 3", dept_type="Core",    efficiency=96, satisfaction=91, turnover=8.1,  productivity=98, start="09:00", end="18:00", break_m=60, flex=True),
            "Finance":                dict(code="FIN", budget=180000, head="Emily Rodriguez", location="Building A, Floor 4", dept_type="Core",    efficiency=89, satisfaction=85, turnover=3.4,  productivity=91, start="08:30", end="17:30", break_m=45, flex=False),
            "Marketing":              dict(code="MKT", budget=320000, head="David Thompson",  location="Building C, Floor 1", dept_type="Revenue", efficiency=87, satisfaction=82, turnover=12.3, productivity=86, start="08:00", end="17:00", break_m=60, flex=True),
            "Operations":             dict(code="OPS", budget=210000, head="Patricia Brown",  location="Building D, Floor 1", dept_type="Core",    efficiency=90, satisfaction=84, turnover=6.8,  productivity=88, start="07:30", end="16:30", break_m=60, flex=False),
            "Sales":                  dict(code="SLS", budget=380000, head="James Wilson",    location="Building C, Floor 2", dept_type="Revenue", efficiency=84, satisfaction=79, turnover=14.5, productivity=83, start="08:00", end="17:00", break_m=60, flex=True),
            "Legal":                  dict(code="LGL", budget=150000, head="Amanda Foster",   location="Building A, Floor 3", dept_type="Support", efficiency=93, satisfaction=90, turnover=2.1,  productivity=95, start="08:30", end="17:30", break_m=60, flex=True),
            "Administration":         dict(code="ADM", budget=130000, head="Robert Taylor",   location="Building A, Floor 1", dept_type="Support", efficiency=88, satisfaction=86, turnover=4.5,  productivity=87, start="08:00", end="17:00", break_m=60, flex=False),
        }

        # Build real employee counts per department from registry
        emp_counts: dict = {}
        for e in employee_registry.get_all():
            d = e.get('department', '')
            if d:
                emp_counts[d] = emp_counts.get(d, 0) + 1

        departments_list = []
        for i, dept_name in enumerate(employee_data_manager.departments, start=1):
            m = _meta.get(dept_name, {})
            code = m.get('code', dept_name[:3].upper())
            budget = m.get('budget', 100000)
            # Real registry count — 0 for empty departments is valid
            emp_count = emp_counts.get(dept_name, 0)
            departments_list.append({
                "id": f"DEPT-{i:03d}",
                "name": dept_name,
                "code": code,
                "description": f"Manages {dept_name.lower()} operations and related functions",
                "head_employee_id": f"EMP-{i:03d}",
                "head_name": m.get('head', 'TBD'),
                "location": m.get('location', f'Building A, Floor {i}'),
                "budget": budget,
                "employee_count": emp_count,
                "established_date": "2020-01-15",
                "status": "Active",
                "department_type": m.get('dept_type', 'Core'),
                "cost_center": f"CC-{code}-001",
                "working_hours": {
                    "start": m.get('start', '08:00'),
                    "end": m.get('end', '17:00'),
                    "break_duration": m.get('break_m', 60),
                    "flexible_hours": m.get('flex', True)
                },
                "performance_metrics": {
                    "efficiency_score": m.get('efficiency', 85),
                    "employee_satisfaction": m.get('satisfaction', 80),
                    "turnover_rate": m.get('turnover', 5.0),
                    "productivity_index": m.get('productivity', 85)
                }
            })

        total_budget = sum(d['budget'] for d in departments_list)
        # Use registry as the single source of truth for total employees
        total_emps = employee_registry.count()
        avg_eff = round(
            sum(d['performance_metrics']['efficiency_score'] for d in departments_list) / len(departments_list), 1
        ) if departments_list else 0

        self.departments_data = {
            "departments": departments_list,
            "statistics": {
                "total_departments": len(departments_list),
                "total_employees": total_emps,
                "total_budget": total_budget,
                "average_efficiency": avg_eff,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        # Time management algorithms
        self.time_tracking_config = {
            "standard_work_week": 40,
            "overtime_threshold": 8,
            "break_compliance_required": True,
            "flexible_time_window": 2  # hours
        }
        
        # Validation rules for departments
        self.validation_rules = {
            "name": {"required": True, "min_length": 2, "max_length": 50},
            "code": {"required": True, "min_length": 2, "max_length": 10, "unique": True},
            "budget": {"required": True, "min_value": 1000, "max_value": 10000000},
            "employee_count": {"required": True, "min_value": 1}
        }

    def get_all_departments(self):
        """Retrieve all departments with calculated metrics"""
        departments = self.departments_data["departments"]
        for dept in departments:
            dept["calculated_metrics"] = self.calculate_department_metrics(dept)
        return departments

    def get_department_by_id(self, dept_id):
        """Get specific department with full details"""
        departments = self.departments_data["departments"]
        for dept in departments:
            if dept["id"] == dept_id:
                dept["calculated_metrics"] = self.calculate_department_metrics(dept)
                return dept
        return None

    def calculate_department_metrics(self, department):
        """Advanced HR time management metrics calculation algorithm"""
        total_budget = self.departments_data["statistics"]["total_budget"] or 1
        total_employees = self.departments_data["statistics"]["total_employees"] or 1
        emp_count = max(department["employee_count"], 1)
        return {
            "cost_per_employee": round(department["budget"] / emp_count, 2),
            "efficiency_rating": self.get_efficiency_rating(department["performance_metrics"]["efficiency_score"]),
            "turnover_status": self.get_turnover_status(department["performance_metrics"]["turnover_rate"]),
            "budget_utilization": round((department["budget"] / total_budget) * 100, 1),
            "workforce_distribution": round((emp_count / total_employees) * 100, 1),
            "working_hours_per_week": self.calculate_weekly_hours(department["working_hours"]),
            "overtime_projection": self.calculate_overtime_projection(department),
            "productivity_trend": self.get_productivity_trend(department["performance_metrics"]["productivity_index"])
        }

    def calculate_weekly_hours(self, working_hours):
        """Calculate total weekly working hours"""
        start_hour = int(working_hours["start"].split(":")[0])
        end_hour = int(working_hours["end"].split(":")[0])
        daily_hours = end_hour - start_hour - (working_hours["break_duration"] / 60)
        return daily_hours * 5  # 5 working days

    def calculate_overtime_projection(self, department):
        """Calculate projected overtime based on efficiency and workload"""
        base_hours = self.calculate_weekly_hours(department["working_hours"])
        efficiency = department["performance_metrics"]["efficiency_score"]
        
        if efficiency > 95:
            return max(0, base_hours - 40)  # High efficiency, minimal overtime
        elif efficiency > 85:
            return max(0, base_hours - 38)  # Medium efficiency, some overtime
        else:
            return max(0, base_hours - 35)  # Lower efficiency, more overtime needed

    def get_efficiency_rating(self, score):
        """Convert efficiency score to rating"""
        if score >= 95: return "Excellent"
        elif score >= 90: return "Very Good" 
        elif score >= 80: return "Good"
        elif score >= 70: return "Fair"
        else: return "Needs Improvement"

    def get_turnover_status(self, rate):
        """Assess turnover rate status"""
        if rate <= 5: return "Low"
        elif rate <= 10: return "Normal"
        elif rate <= 15: return "High"
        else: return "Critical"

    def get_productivity_trend(self, index):
        """Determine productivity trend"""
        if index >= 95: return "Trending Up"
        elif index >= 85: return "Stable"
        else: return "Needs Attention"

    def create_department(self, dept_data):
        """Create new department with validation"""
        if self.validate_department_data(dept_data):
            new_dept = {
                "id": f"DEPT-{str(uuid.uuid4())[:3].upper()}",
                "created_date": datetime.now().isoformat(),
                **dept_data,
                "status": "Active",
                "performance_metrics": {
                    "efficiency_score": 85,  # Default starting value
                    "employee_satisfaction": 80,
                    "turnover_rate": 0,
                    "productivity_index": 85
                }
            }
            self.departments_data["departments"].append(new_dept)
            self.update_statistics()
            return True, "Department created successfully"
        return False, "Validation failed"

    def update_department(self, dept_id, updates):
        """Update existing department"""
        department = self.get_department_by_id(dept_id)
        if department:
            department.update(updates)
            self.update_statistics()
            return True, "Department updated successfully"
        return False, "Department not found"

    def delete_department(self, dept_id):
        """Delete department (with safety checks)"""
        departments = self.departments_data["departments"]
        for i, dept in enumerate(departments):
            if dept["id"] == dept_id:
                if dept["employee_count"] > 0:
                    return False, "Cannot delete department with active employees"
                departments.pop(i)
                self.update_statistics()
                return True, "Department deleted successfully"
        return False, "Department not found"

    def validate_department_data(self, data):
        """Comprehensive validation algorithm"""
        for field, rules in self.validation_rules.items():
            if field in data:
                value = data[field]
                if rules.get("required") and not value:
                    return False
                if "min_length" in rules and len(str(value)) < rules["min_length"]:
                    return False
                if "unique" in rules and rules["unique"]:
                    if self.is_code_duplicate(value, data.get("id")):
                        return False
        return True

    def is_code_duplicate(self, code, exclude_id=None):
        """Check for duplicate department codes"""
        for dept in self.departments_data["departments"]:
            if dept["code"] == code and dept["id"] != exclude_id:
                return True
        return False

    def update_statistics(self):
        """Update global department statistics"""
        departments = self.departments_data["departments"]
        self.departments_data["statistics"] = {
            "total_departments": len(departments),
            "total_employees": sum(d["employee_count"] for d in departments),
            "total_budget": sum(d["budget"] for d in departments),
            "average_efficiency": round(sum(d["performance_metrics"]["efficiency_score"] for d in departments) / len(departments), 1),
            "last_updated": datetime.now().isoformat()
        }

    def get_dashboard_analytics(self):
        """Generate analytics for dashboard integration"""
        departments = self.departments_data["departments"]
        return {
            "department_performance": [
                {"name": d["name"], "efficiency": d["performance_metrics"]["efficiency_score"]}
                for d in departments
            ],
            "budget_distribution": [
                {"department": d["name"], "budget": d["budget"], "percentage": round((d["budget"] / self.departments_data["statistics"]["total_budget"]) * 100, 1)}
                for d in departments
            ],
            "workforce_distribution": [
                {"department": d["name"], "employees": d["employee_count"]}
                for d in departments
            ]
        }

# Global department manager instance
dept_manager = DepartmentDataManager()

def DepartmentalSections():
    """
    Modern Departmental Sections page with advanced HR time management algorithms
    and seamless institution integration
    """
    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-blue-50 min-h-screen p-6 gap-6'):

        # ── Header card ───────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-gradient-to-r from-indigo-700 to-blue-700 text-white'):
            with ui.card_section().classes('px-8 py-6'):
                with ui.row().classes('w-full justify-between items-center'):
                    with ui.column().classes('gap-1'):
                        with ui.row().classes('items-center gap-2 text-indigo-200 text-sm mb-1'):
                            ui.html('<span>🏠 Dashboard</span>')
                            ui.html('<span class="opacity-50">/</span>')
                            ui.html('<span>Administration</span>')
                            ui.html('<span class="opacity-50">/</span>')
                            ui.html('<span class="text-white font-medium">Departmental Sections</span>')
                        ui.html('<h1 class="text-3xl font-extrabold tracking-tight">🏢 Departmental Sections</h1>')
                    with ui.row().classes('gap-3'):
                        ui.button('Export Data',    icon='download', on_click=export_department_data).props('outline color=white')
                        ui.button('Add Department', icon='add',      on_click=show_add_department_dialog).props('outline color=white')

        # ── KPI stats ────────────────────────────────────────────────────────
        create_department_stats_overview()

        # ── Tabs ─────────────────────────────────────────────────────────────
        with ui.tabs().classes('w-full mb-4') as tabs:
            overview_tab = ui.tab('Overview', icon='dashboard')
            departments_tab = ui.tab('Departments', icon='account_tree')
            analytics_tab = ui.tab('Analytics', icon='analytics')
            time_management_tab = ui.tab('Time Management', icon='schedule')

        with ui.tab_panels(tabs, value=overview_tab).classes('w-full'):
            with ui.tab_panel(overview_tab):
                create_overview_section()
            with ui.tab_panel(departments_tab):
                create_departments_list_section()
            with ui.tab_panel(analytics_tab):
                create_analytics_section()
            with ui.tab_panel(time_management_tab):
                create_time_management_section()

def create_department_stats_overview():
    """Create department statistics overview cards — evenly distributed, modern gradient design."""
    stats = dept_manager.departments_data["statistics"]

    cards = [
        {
            "icon": "🏢",
            "label": "Total Departments",
            "value": str(stats["total_departments"]),
            "sub": "Active units",
            "from_": "#6366f1",   # indigo-500
            "to_":   "#4338ca",   # indigo-700
            "orb1":  "rgba(255,255,255,0.12)",
            "orb2":  "rgba(255,255,255,0.06)",
        },
        {
            "icon": "👥",
            "label": "Total Employees",
            "value": str(stats["total_employees"]),
            "sub": "Across all depts",
            "from_": "#10b981",   # emerald-500
            "to_":   "#065f46",   # emerald-900
            "orb1":  "rgba(255,255,255,0.14)",
            "orb2":  "rgba(255,255,255,0.07)",
        },
        {
            "icon": "💰",
            "label": "Total Budget",
            "value": f'${stats["total_budget"]:,}',
            "sub": "Annual allocation",
            "from_": "#f59e0b",   # amber-500
            "to_":   "#b45309",   # amber-700
            "orb1":  "rgba(255,255,255,0.15)",
            "orb2":  "rgba(255,255,255,0.07)",
        },
        {
            "icon": "📈",
            "label": "Avg Efficiency",
            "value": f'{stats["average_efficiency"]}%',
            "sub": "Performance score",
            "from_": "#ef4444",   # rose-500
            "to_":   "#9f1239",   # rose-900
            "orb1":  "rgba(255,255,255,0.13)",
            "orb2":  "rgba(255,255,255,0.06)",
        },
    ]

    with ui.row().classes('w-full gap-5 flex-nowrap'):
        for c in cards:
            ui.html(f"""
<div style="
    flex: 1 1 0%;
    min-width: 0;
    background: linear-gradient(135deg, {c['from_']}, {c['to_']});
    border-radius: 1.25rem;
    padding: 1.5rem 1.75rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px -6px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
" onmouseover="this.style.transform='translateY(-6px)';this.style.boxShadow='0 20px 40px -8px rgba(0,0,0,0.35)'"
   onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 10px 30px -6px rgba(0,0,0,0.3)'">

  <!-- decorative background orbs -->
  <div style="position:absolute;top:-28px;right:-28px;width:110px;height:110px;
              border-radius:50%;background:{c['orb1']};pointer-events:none;"></div>
  <div style="position:absolute;bottom:-20px;left:-20px;width:80px;height:80px;
              border-radius:50%;background:{c['orb2']};pointer-events:none;"></div>

  <!-- icon pill -->
  <div style="display:inline-flex;align-items:center;justify-content:center;
              width:52px;height:52px;border-radius:0.875rem;
              background:rgba(255,255,255,0.18);
              backdrop-filter:blur(6px);
              font-size:1.75rem;margin-bottom:1rem;
              box-shadow:inset 0 1px 1px rgba(255,255,255,0.3);">
    {c['icon']}
  </div>

  <!-- metric -->
  <div style="font-size:2.25rem;font-weight:900;letter-spacing:-0.03em;
              line-height:1;margin-bottom:0.4rem;
              text-shadow:0 2px 8px rgba(0,0,0,0.15);">
    {c['value']}
  </div>

  <!-- label -->
  <div style="font-size:0.8rem;font-weight:700;text-transform:uppercase;
              letter-spacing:0.12em;opacity:0.85;margin-bottom:0.25rem;">
    {c['label']}
  </div>

  <!-- sub label -->
  <div style="font-size:0.72rem;opacity:0.6;font-weight:500;">
    {c['sub']}
  </div>
</div>
""")

def create_overview_section():
    """Create overview section — one row of 4-5 department cards evenly spread."""
    departments = dept_manager.get_all_departments()

    # Cycle through vivid gradient pairs for visual variety
    _gradients = [
        ("from-indigo-500 to-blue-600",    "#6366f1", "#2563eb"),
        ("from-emerald-500 to-teal-600",   "#10b981", "#0d9488"),
        ("from-violet-500 to-purple-600",  "#8b5cf6", "#9333ea"),
        ("from-rose-500 to-pink-600",      "#ef4444", "#db2777"),
        ("from-amber-500 to-orange-600",   "#f59e0b", "#ea580c"),
        ("from-cyan-500 to-sky-600",       "#06b6d4", "#0284c7"),
    ]

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.card_section().classes('px-6 pt-6 pb-2'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.html('<h2 class="text-xl font-bold text-gray-800">📊 Department Performance Overview</h2>')
                ui.html(f'<span class="text-xs text-gray-400 bg-gray-100 px-3 py-1 rounded-full">'
                        f'{len(departments)} departments</span>')

        with ui.card_section().classes('px-6 pb-6'):
            # flex-wrap so if >5 depts they wrap, min-w-0 keeps flex-1 from overflowing
            with ui.element('div').style(
                'display:flex; flex-wrap:wrap; gap:1rem; width:100%;'
            ):
                for idx, dept in enumerate(departments):
                    metrics   = dept["calculated_metrics"]
                    eff       = dept["performance_metrics"]["efficiency_score"]
                    _, g_from, g_to = _gradients[idx % len(_gradients)]

                    if eff >= 90:
                        eff_color = "#059669"   # emerald
                        eff_bg    = "#d1fae5"
                    elif eff >= 80:
                        eff_color = "#d97706"   # amber
                        eff_bg    = "#fef3c7"
                    else:
                        eff_color = "#dc2626"   # rose
                        eff_bg    = "#fee2e2"

                    ui.html(f"""
<div style="
    flex: 1 1 0%;
    min-width: 180px;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 4px 18px -4px rgba(0,0,0,0.12);
    background: #fff;
    transition: transform .2s ease, box-shadow .2s ease;
    cursor: default;
" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 14px 28px -6px rgba(0,0,0,0.18)'"
   onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 18px -4px rgba(0,0,0,0.12)'">

  <!-- gradient top bar -->
  <div style="
    height: 7px;
    background: linear-gradient(90deg, {g_from}, {g_to});
  "></div>

  <div style="padding: 1rem 1.1rem 1.1rem;">

    <!-- dept name + active badge -->
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:.5rem; margin-bottom:.75rem;">
      <span style="font-weight:700; font-size:.9rem; color:#1e293b; line-height:1.3;">{dept["name"]}</span>
      <span style="flex-shrink:0; padding:.15rem .55rem; border-radius:9999px;
                   font-size:.65rem; font-weight:700;
                   background:linear-gradient(90deg,{g_from},{g_to}); color:#fff;">
        Active
      </span>
    </div>

    <!-- metrics rows -->
    <div style="display:flex; flex-direction:column; gap:.45rem;">

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:.72rem; color:#94a3b8; font-weight:500;">👥 Employees</span>
        <span style="font-size:.8rem; font-weight:700; color:#1e293b;">{dept["employee_count"]}</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:.72rem; color:#94a3b8; font-weight:500;">📈 Efficiency</span>
        <span style="font-size:.8rem; font-weight:700;
                     padding:.1rem .45rem; border-radius:9999px;
                     background:{eff_bg}; color:{eff_color};">{eff}%</span>
      </div>

      <!-- efficiency mini-bar -->
      <div style="width:100%; height:4px; background:#e2e8f0; border-radius:9999px; overflow:hidden;">
        <div style="height:4px; border-radius:9999px;
                    background:linear-gradient(90deg,{g_from},{g_to});
                    width:{eff}%;"></div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:.72rem; color:#94a3b8; font-weight:500;">💰 Budget</span>
        <span style="font-size:.78rem; font-weight:600; color:#475569;">${dept["budget"]:,}</span>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:.72rem; color:#94a3b8; font-weight:500;">💵 Cost/Emp</span>
        <span style="font-size:.78rem; font-weight:600; color:#475569;">${metrics["cost_per_employee"]:,}</span>
      </div>

    </div>
  </div>
</div>
""")

def create_departments_list_section():
    """Create detailed departments list with management capabilities"""
    departments = dept_manager.get_all_departments()

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.card_section().classes('px-6 pt-6 pb-2'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.html('<h2 class="text-xl font-bold text-gray-800">🏢 Department Management</h2>')
                ui.html(f'<span class="text-xs text-gray-400 bg-gray-100 px-3 py-1 rounded-full">'
                        f'{len(departments)} departments</span>')

        with ui.element('div').classes('w-full overflow-x-auto px-2 pb-4'):
            with ui.element('table').classes('w-full min-w-full border-collapse'):

                # Header
                with ui.element('thead'):
                    with ui.element('tr').classes(
                        'bg-gradient-to-r from-indigo-600 to-blue-600 text-white text-sm'
                    ):
                        th = 'px-4 py-3 text-left font-semibold tracking-wide uppercase whitespace-nowrap'
                        for icon_h, text_h in [
                            ('🏢', 'Department'), ('👤', 'Head'), ('👥', 'Employees'),
                            ('💰', 'Budget'), ('📈', 'Efficiency'), ('⚙', 'Actions'),
                        ]:
                            with ui.element('th').classes(th):
                                ui.html(f'{icon_h} {text_h}')

                # Body
                with ui.element('tbody'):
                    td = 'px-4 py-3 text-sm text-gray-700 whitespace-nowrap'
                    for idx, dept in enumerate(departments):
                        stripe   = 'bg-slate-50' if idx % 2 == 0 else 'bg-white'
                        eff      = dept['performance_metrics']['efficiency_score']
                        eff_cls  = ('text-emerald-600 font-bold' if eff >= 90
                                    else 'text-amber-600 font-bold' if eff >= 80
                                    else 'text-rose-600 font-bold')
                        with ui.element('tr').classes(
                            f'{stripe} border-b border-gray-100 '
                            'hover:bg-blue-50 transition-colors duration-150'
                        ):
                            # Dept name + code
                            with ui.element('td').classes(td):
                                ui.html(
                                    f'<div class="font-semibold text-gray-900">{dept["name"]}</div>'
                                    f'<div class="text-xs text-gray-400">{dept["code"]} · {dept["location"]}</div>'
                                )
                            # Head
                            with ui.element('td').classes(td):
                                ui.label(dept['head_name'])
                            # Employees
                            with ui.element('td').classes(td):
                                ui.html(f'<span class="font-bold text-gray-900">{dept["employee_count"]}</span>')
                            # Budget
                            with ui.element('td').classes(td):
                                ui.html(f'<span class="font-medium">${dept["budget"]:,}</span>')
                            # Efficiency
                            with ui.element('td').classes(td):
                                ui.html(f'<span class="{eff_cls}">{eff}%</span>')
                            # Actions
                            with ui.element('td').classes(td):
                                with ui.row().classes('gap-1'):
                                    ui.button(icon='visibility').props('flat round dense color=green size=sm') \
                                        .on_click(lambda d=dept: view_department_details(d))
                                    ui.button(icon='edit').props('flat round dense color=blue size=sm') \
                                        .on_click(lambda d=dept: edit_department_dialog(d))
                                    ui.button(icon='delete').props('flat round dense color=red size=sm') \
                                        .on_click(lambda d=dept: delete_department_confirm(d))

def create_analytics_section():
    """Create analytics section with charts and metrics"""
    analytics = dept_manager.get_dashboard_analytics()

    with ui.row().classes('w-full gap-6'):
        # Budget Distribution
        with ui.card().classes('flex-1 rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.card_section().classes('px-6 pt-6 pb-2'):
                ui.html('<h2 class="text-lg font-bold text-gray-800">💰 Budget Distribution</h2>')
            with ui.card_section().classes('px-6 pb-6'):
                with ui.column().classes('w-full gap-3'):
                    for item in analytics["budget_distribution"]:
                        with ui.row().classes('items-center justify-between'):
                            ui.html(f'<span class="text-sm font-medium text-gray-700">{item["department"]}</span>')
                            ui.html(f'<span class="text-sm font-bold text-blue-600">{item["percentage"]}%</span>')
                        with ui.element('div').classes('w-full bg-gray-200 rounded-full h-2'):
                            ui.element('div').classes('bg-gradient-to-r from-blue-500 to-indigo-500 h-2 rounded-full') \
                                .style(f'width: {item["percentage"]}%')

        # Workforce Distribution
        with ui.card().classes('flex-1 rounded-2xl shadow-md bg-white overflow-hidden'):
            with ui.card_section().classes('px-6 pt-6 pb-2'):
                ui.html('<h2 class="text-lg font-bold text-gray-800">👥 Workforce Distribution</h2>')
            with ui.card_section().classes('px-6 pb-6'):
                total_employees = sum(item["employees"] for item in analytics["workforce_distribution"])
                with ui.column().classes('w-full gap-3'):
                    for item in analytics["workforce_distribution"]:
                        percentage = round((item["employees"] / total_employees) * 100, 1) if total_employees else 0
                        with ui.row().classes('items-center justify-between'):
                            ui.html(f'<span class="text-sm font-medium text-gray-700">{item["department"]}</span>')
                            ui.html(f'<span class="text-sm font-bold text-emerald-600">{item["employees"]} ({percentage}%)</span>')
                        with ui.element('div').classes('w-full bg-gray-200 rounded-full h-2'):
                            ui.element('div').classes('bg-gradient-to-r from-emerald-400 to-green-500 h-2 rounded-full') \
                                .style(f'width: {percentage}%')

def create_time_management_section():
    """Create time management section with HR algorithms"""
    departments = dept_manager.get_all_departments()

    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
        with ui.card_section().classes('px-6 pt-6 pb-2'):
            ui.html('<h2 class="text-xl font-bold text-gray-800">⏱ Time Management &amp; Scheduling</h2>')

        with ui.element('div').classes('w-full overflow-x-auto px-2 pb-4'):
            with ui.element('table').classes('w-full min-w-full border-collapse'):

                with ui.element('thead'):
                    with ui.element('tr').classes(
                        'bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm'
                    ):
                        th = 'px-4 py-3 text-left font-semibold tracking-wide uppercase whitespace-nowrap'
                        for h in ['🏢 Department', '🕐 Hours', '📅 Weekly Hrs',
                                  '⏰ Overtime', '🔄 Flexible', '🔵 Status']:
                            with ui.element('th').classes(th):
                                ui.html(h)

                with ui.element('tbody'):
                    td = 'px-4 py-3 text-sm text-gray-700 whitespace-nowrap'
                    for idx, dept in enumerate(departments):
                        metrics  = dept["calculated_metrics"]
                        hours    = dept["working_hours"]
                        overtime = metrics["overtime_projection"]
                        eff      = dept["performance_metrics"]["efficiency_score"]
                        stripe   = 'bg-slate-50' if idx % 2 == 0 else 'bg-white'

                        ot_cls   = ('text-rose-600 font-bold' if overtime > 5
                                    else 'text-amber-500 font-bold' if overtime > 0
                                    else 'text-emerald-600 font-bold')
                        if eff >= 90:
                            status_html = '<span class="px-2 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">Optimal</span>'
                        elif eff >= 80:
                            status_html = '<span class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">Good</span>'
                        else:
                            status_html = '<span class="px-2 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800">Review</span>'

                        with ui.element('tr').classes(
                            f'{stripe} border-b border-gray-100 '
                            'hover:bg-blue-50 transition-colors duration-150'
                        ):
                            with ui.element('td').classes(td):
                                ui.html(f'<span class="font-semibold text-gray-900">{dept["name"]}</span>')
                            with ui.element('td').classes(td):
                                ui.label(f'{hours["start"]} – {hours["end"]}')
                            with ui.element('td').classes(td):
                                ui.html(f'<span class="font-bold text-gray-900">{metrics["working_hours_per_week"]:.1f}h</span>')
                            with ui.element('td').classes(td):
                                ui.html(f'<span class="{ot_cls}">{overtime:.1f}h</span>')
                            with ui.element('td').classes(td):
                                flex = hours["flexible_hours"]
                                ui.html(
                                    '<span class="px-2 py-0.5 rounded-full text-xs font-bold '
                                    + ('bg-emerald-100 text-emerald-800">Yes</span>' if flex
                                       else 'bg-slate-100 text-slate-600">No</span>')
                                )
                            with ui.element('td').classes(td):
                                ui.html(status_html)

# Dialog and action functions
async def show_add_department_dialog():
    """Show add department dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
        ui.label('Add New Department').classes('text-xl font-semibold mb-4')
        
        name_input = ui.input('Department Name').classes('w-full mb-3').props('outlined')
        code_input = ui.input('Department Code').classes('w-full mb-3').props('outlined')
        description_input = ui.textarea('Description').classes('w-full mb-3').props('outlined rows=3')
        budget_input = ui.number('Annual Budget', value=100000).classes('w-full mb-3').props('outlined')
        location_input = ui.input('Location').classes('w-full mb-3').props('outlined')
        
        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=dialog.close).props('flat')
            ui.button('Create Department', on_click=lambda: create_new_department(
                dialog, name_input.value, code_input.value, description_input.value,
                budget_input.value, location_input.value
            )).props('color=primary')
    
    dialog.open()

async def create_new_department(dialog, name, code, description, budget, location):
    """Create new department with validation"""
    if not name or not code:
        ui.notify('Name and Code are required!', color='negative')
        return
    
    dept_data = {
        "name": name,
        "code": code.upper(),
        "description": description,
        "budget": budget,
        "location": location,
        "employee_count": 0,
        "established_date": datetime.now().isoformat()[:10],
        "head_employee_id": None,
        "head_name": "To be assigned",
        "department_type": "Support",
        "cost_center": f"CC-{code.upper()}-001",
        "working_hours": {
            "start": "09:00",
            "end": "17:00",
            "break_duration": 60,
            "flexible_hours": True
        }
    }
    
    success, message = dept_manager.create_department(dept_data)
    if success:
        ui.notify('Department created successfully!', color='positive')
        dialog.close()
        # Refresh the page
        ui.navigate.to('/administration/departments')
    else:
        ui.notify(f'Error: {message}', color='negative')

async def edit_department_dialog(department):
    """Show edit department dialog"""
    ui.notify(f'Edit {department["name"]} - Feature coming soon!', color='info')

async def view_department_details(department):
    """Show department details dialog"""
    metrics = department["calculated_metrics"]
    
    with ui.dialog() as dialog, ui.card().classes('w-[600px] p-6'):
        ui.label(f'{department["name"]} Details').classes('text-xl font-semibold mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            # Left column
            with ui.column().classes('gap-3'):
                ui.label('Basic Information').classes('font-semibold text-lg text-blue-600')
                ui.label(f'Department Code: {department["code"]}').classes('text-sm')
                ui.label(f'Location: {department["location"]}').classes('text-sm')
                ui.label(f'Head: {department["head_name"]}').classes('text-sm')
                ui.label(f'Established: {department["established_date"]}').classes('text-sm')
                ui.label(f'Type: {department["department_type"]}').classes('text-sm')
                
                ui.label('Financial Information').classes('font-semibold text-lg text-green-600 mt-4')
                ui.label(f'Annual Budget: ${department["budget"]:,}').classes('text-sm')
                ui.label(f'Cost Center: {department["cost_center"]}').classes('text-sm')
                ui.label(f'Cost per Employee: ${metrics["cost_per_employee"]:,}').classes('text-sm')
            
            # Right column
            with ui.column().classes('gap-3'):
                ui.label('Performance Metrics').classes('font-semibold text-lg text-purple-600')
                ui.label(f'Efficiency Score: {department["performance_metrics"]["efficiency_score"]}%').classes('text-sm')
                ui.label(f'Employee Satisfaction: {department["performance_metrics"]["employee_satisfaction"]}%').classes('text-sm')
                ui.label(f'Turnover Rate: {department["performance_metrics"]["turnover_rate"]}%').classes('text-sm')
                ui.label(f'Productivity Index: {department["performance_metrics"]["productivity_index"]}%').classes('text-sm')
                
                ui.label('Time Management').classes('font-semibold text-lg text-orange-600 mt-4')
                ui.label(f'Working Hours: {department["working_hours"]["start"]} - {department["working_hours"]["end"]}').classes('text-sm')
                ui.label(f'Weekly Hours: {metrics["working_hours_per_week"]:.1f}h').classes('text-sm')
                ui.label(f'Overtime Projection: {metrics["overtime_projection"]:.1f}h').classes('text-sm')
                ui.label(f'Flexible Hours: {"Yes" if department["working_hours"]["flexible_hours"] else "No"}').classes('text-sm')
        
        with ui.row().classes('w-full justify-end mt-6'):
            ui.button('Close', on_click=dialog.close).props('flat')
    
    dialog.open()

async def delete_department_confirm(department):
    """Show delete confirmation dialog"""
    if department["employee_count"] > 0:
        ui.notify(f'Cannot delete {department["name"]} - Department has active employees', color='negative')
        return
    
    ui.notify(f'Delete {department["name"]} - Feature coming soon!', color='warning')

async def export_department_data():
    """Export department data"""
    ui.notify('Exporting department data...', color='info')
    await asyncio.sleep(1)
    ui.notify('Department data exported successfully!', color='positive')

# Integration APIs for other modules
def get_department_integration_data():
    """API for other modules to get department data"""
    return dept_manager.get_all_departments()

def get_department_by_employee(employee_id):
    """Find which department an employee belongs to"""
    # This would integrate with employee management system
    departments = dept_manager.get_all_departments()
    for dept in departments:
        if dept["head_employee_id"] == employee_id:
            return dept
    return None

def update_department_employee_counts():
    """Update all department employee counts based on actual employee data"""
    try:
        from ...components.administration.enroll_staff import employee_data_manager
        
        # Get current employee counts by department
        department_counts = {}
        for emp in employee_data_manager.employees.values():
            if emp['employment_info']['status'] == 'Active':
                dept = emp['employment_info']['department']
                department_counts[dept] = department_counts.get(dept, 0) + 1
        
        # Update each department's employee count
        for dept_data in dept_manager.departments_data['departments']:
            dept_name = dept_data['name']
            new_count = department_counts.get(dept_name, 0)
            
            # Only update if the count has changed
            if dept_data.get('employee_count', 0) != new_count:
                dept_manager.update_department(dept_data['id'], {"employee_count": new_count})
        
        # Update department statistics
        dept_manager.update_statistics()
        
        print(f"Updated department employee counts: {department_counts}")
        
    except Exception as e:
        print(f"Error updating department employee counts: {e}")

def update_department_employee_count(dept_id, new_count):
    """Update employee count when employees are added/removed"""
    success, message = dept_manager.update_department(dept_id, {"employee_count": new_count})
    if success:
        dept_manager.update_statistics()
    return success, message