"""
Shared Employee Registry
Single source of truth for employee data across all pages.
Loads from config/employees.yaml on startup, merges in-memory enrollments,
and exposes a consistent interface so every page sees the same records.

ID Format: EMP{6-digit} e.g. EMP001001
"""

import yaml
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

_YAML_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'employees.yaml')

# ---------------------------------------------------------------------------
# Normalise legacy ID variants to canonical EMP{6-digit} format
# EMP-001  → EMP000001   EMP-101  → EMP000101   EMP1001 → EMP001001
# ---------------------------------------------------------------------------
_STRIP = re.compile(r'[^0-9]')

def normalise_id(raw: str) -> str:
    digits = _STRIP.sub('', str(raw))
    return f"EMP{digits.zfill(6)}"


class EmployeeRegistry:
    """Module-level singleton — import and use `employee_registry` directly."""

    def __init__(self):
        self._employees: Dict[str, Dict[str, Any]] = {}
        self._next_seq: int = 1
        self._load_yaml()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_yaml(self):
        try:
            with open(_YAML_PATH, 'r') as fh:
                raw: dict = yaml.safe_load(fh) or {}
            for raw_id, data in raw.items():
                emp = dict(data)
                canon_id = normalise_id(raw_id)
                emp['employee_id'] = canon_id
                # Flatten nested address for display convenience
                if isinstance(emp.get('address'), dict):
                    addr = emp['address']
                    emp['address_display'] = f"{addr.get('street','')}, {addr.get('city','')}, {addr.get('state','')} {addr.get('zip','')}"
                # Ensure required keys
                emp.setdefault('status', 'active')
                emp.setdefault('department', 'General')
                emp.setdefault('position', '')
                emp.setdefault('phone', '')
                emp.setdefault('email', '')
                self._employees[canon_id] = emp
                # Track highest numeric suffix so new IDs won't collide
                digits = int(_STRIP.sub('', raw_id) or '0')
                if digits >= self._next_seq:
                    self._next_seq = digits + 1
        except Exception as exc:
            print(f'[EmployeeRegistry] YAML load failed: {exc}')

    def _generate_id(self) -> str:
        new_id = f"EMP{self._next_seq:06d}"
        self._next_seq += 1
        return new_id

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_all(self, status: Optional[str] = None) -> List[Dict]:
        """Return all employees, optionally filtered by status string."""
        employees = list(self._employees.values())
        if status:
            employees = [e for e in employees if e.get('status', '').lower() == status.lower()]
        return employees

    def get(self, employee_id: str) -> Optional[Dict]:
        """Fetch a single employee by any recognised ID format."""
        return self._employees.get(normalise_id(employee_id))

    def add(self, data: Dict) -> str:
        """
        Register a new employee from enrollment form data.
        Returns the canonical employee_id assigned.
        data keys expected (at minimum): first_name, last_name, email,
            department, position, employment_type, start_date / hire_date
        """
        emp_id = data.get('employee_id') or self._generate_id()
        emp_id = normalise_id(emp_id)

        record = {
            'employee_id': emp_id,
            'first_name':       data.get('first_name', ''),
            'last_name':        data.get('last_name', ''),
            'email':            data.get('email', ''),
            'phone':            data.get('phone', ''),
            'department':       data.get('department', ''),
            'position':         data.get('position', ''),
            'employment_type':  data.get('employment_type', 'full_time'),
            'hire_date':        data.get('start_date') or data.get('hire_date', ''),
            'status':           data.get('status', 'active'),
            'salary':           data.get('salary'),
            'salary_grade':     data.get('salary_grade', ''),
            'manager_id':       data.get('reporting_manager') or data.get('manager_id', ''),
            'location':         data.get('work_location', 'On-site'),
            'role':             data.get('role', 'employee'),
            'performance_rating': data.get('performance_rating', 0.0),
            'created_at':       datetime.now().isoformat(),
            'updated_at':       datetime.now().isoformat(),
        }
        self._employees[emp_id] = record
        return emp_id

    def update(self, employee_id: str, updates: Dict) -> bool:
        """Patch an existing employee record. Returns True if found."""
        canon = normalise_id(employee_id)
        if canon not in self._employees:
            return False
        self._employees[canon].update(updates)
        self._employees[canon]['updated_at'] = datetime.now().isoformat()
        return True

    # ------------------------------------------------------------------
    # Convenience aggregates (used by dashboards, institution profile, etc.)
    # ------------------------------------------------------------------
    def count(self, status: Optional[str] = None) -> int:
        return len(self.get_all(status))

    def departments(self) -> List[str]:
        return sorted({e.get('department', '') for e in self._employees.values() if e.get('department')})

    def get_statistics(self) -> Dict:
        all_emps = self.get_all()
        return {
            'total_employees': len(all_emps),
            'active':          sum(1 for e in all_emps if e.get('status') == 'active'),
            'on_leave':        sum(1 for e in all_emps if e.get('status') == 'on_leave'),
            'departments':     len(self.departments()),
        }

    def as_select_options(self) -> List[str]:
        """Returns list of 'EMP001001 - First Last' strings for ui.select."""
        return [
            f"{e['employee_id']} - {e.get('first_name','')} {e.get('last_name','')}".strip()
            for e in sorted(self._employees.values(), key=lambda x: x['employee_id'])
        ]

    def save_yaml(self) -> bool:
        """Persist the current in-memory registry back to config/employees.yaml."""
        try:
            data = {}
            for emp_id, record in self._employees.items():
                # Omit convenience keys computed at load time
                entry = {k: v for k, v in record.items() if k not in ('employee_id', 'address_display')}
                data[emp_id] = entry
            with open(_YAML_PATH, 'w') as fh:
                yaml.dump(data, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)
            return True
        except Exception as exc:
            print(f'[EmployeeRegistry] YAML save failed: {exc}')
            return False

    def next_id(self) -> str:
        """Preview next ID without consuming it (for display in enroll form)."""
        return f"EMP{self._next_seq:06d}"


# Module-level singleton — import this everywhere
employee_registry = EmployeeRegistry()
