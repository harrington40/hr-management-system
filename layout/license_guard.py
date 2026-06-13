"""
License Guard
=============
Integrates the license_engine cryptographic validation layer with the NiceGUI
app.  Falls back to the legacy YAML-based flag when no signed license.json is
present so that development / demo environments still work.

Priority order
--------------
1. ``config/license.json``  +  ``config/activation.json``  (full cryptographic path)
2. ``config/license.yaml``  (legacy simple flag, for dev/demo only)

Usage in subpages.py:
    from layout.license_guard import require_license

    @router.page('/attendance/holidays')
    def show_holidays():
        Sidebar()
        if require_license('Holiday & Vacation Management'):
            return
        SetHolidays()
"""
from __future__ import annotations

import json
import yaml
from datetime import date
from pathlib import Path

from nicegui import ui
from helperFuns import get_mount_path, build_mount_route

BASE_DIR       = Path(__file__).parent.parent
LICENSE_JSON   = BASE_DIR / 'config' / 'license.json'
ACTIVATION_JSON= BASE_DIR / 'config' / 'activation.json'
LICENSE_YAML   = BASE_DIR / 'config' / 'license.yaml'
APP_MOUNT_PATH = get_mount_path()


# ─────────────────────────────────────────────────────────────────────────────
# Persistence helpers  (legacy YAML path — kept for backward compat)
# ─────────────────────────────────────────────────────────────────────────────

def _load_license_yaml() -> dict:
    try:
        with open(LICENSE_YAML) as f:
            data = yaml.safe_load(f) or {}
        return data.get('license', {})
    except Exception:
        return {}


def _save_license_yaml(lic: dict) -> None:
    try:
        with open(LICENSE_YAML, 'w') as f:
            yaml.dump({'license': lic}, f, default_flow_style=False, allow_unicode=True)
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def is_license_active() -> bool:
    """
    Return True when a valid license is present.

    Checks in order:
    1. Cryptographic path  (license.json + activation.json)
    2. Legacy YAML flag    (license.yaml active: true)
    """
    # ── 1. Cryptographic path ─────────────────────────────────────────────
    if LICENSE_JSON.exists() and ACTIVATION_JSON.exists():
        try:
            from license_engine.activation import verify_activation
            ok, _ = verify_activation(LICENSE_JSON, ACTIVATION_JSON)
            return ok
        except Exception:
            pass

    # ── 2. Legacy YAML fallback ───────────────────────────────────────────
    lic = _load_license_yaml()
    if not lic.get('active', False):
        return False
    expiry = lic.get('expiry', '')
    if expiry:
        try:
            if date.fromisoformat(str(expiry)[:10]) < date.today():
                return False
        except ValueError:
            pass
    return True


def get_license_info() -> dict:
    """Return the raw license dict (JSON preferred, YAML fallback)."""
    if LICENSE_JSON.exists():
        try:
            with open(LICENSE_JSON) as f:
                return json.load(f)
        except Exception:
            pass
    return _load_license_yaml()


def activate_license_key(
    key: str,
    holder: str = '',
    plan: str = 'Enterprise',
) -> tuple[bool, str]:
    """
    Validate and activate a license key.

    If a signed ``license.json`` whose ``license_id`` matches *key* (or whose
    ``key`` field matches) exists in ``config/``, the full cryptographic
    activation path is used.

    Otherwise, the legacy simple path writes to ``license.yaml`` — useful for
    development and demo usage.
    """
    # ── Cryptographic path ────────────────────────────────────────────────
    if LICENSE_JSON.exists():
        try:
            with open(LICENSE_JSON) as f:
                lic_data = json.load(f)
            # Accept if the entered key matches license_id or a 'key' field
            stored_key = lic_data.get('license_id', '') or lic_data.get('key', '')
            if key.strip() == stored_key.strip():
                from license_engine.activation import activate
                ok, result = activate(LICENSE_JSON, ACTIVATION_JSON)
                if ok:
                    expiry = lic_data.get('expires_at', '')
                    exp_str = f'until {expiry}' if expiry else 'perpetually'
                    return True, f'License activated {exp_str}. Display code: {result}'
                return False, result
        except Exception as exc:
            pass  # fall through to legacy path

    # ── Legacy simple path ────────────────────────────────────────────────
    if not key or len(key.strip()) < 16:
        return False, 'Key too short — please check your license key.'
    parts = key.strip().split('-')
    if len(parts) < 3:
        return False, 'Invalid key format. Expected: HRMkit-PLAN-XXXX-YYYY-ZZZZ'

    expiry = date.today().replace(year=date.today().year + 1).isoformat()
    lic = {
        'active': True,
        'key': key.strip(),
        'plan': plan,
        'expiry': expiry,
        'seats': 150,
        'activated_at': date.today().isoformat(),
        'holder': holder,
    }
    _save_license_yaml(lic)
    return True, f'License activated! Valid until {expiry}.'


# ─────────────────────────────────────────────────────────────────────────────
# Lock overlay UI
# ─────────────────────────────────────────────────────────────────────────────

def show_locked_page(page_title: str = 'This Feature') -> None:
    """Render a full-page license-required overlay."""
    license_url = build_mount_route('/billing/license-pricing', base=APP_MOUNT_PATH)

    # ── Full-page canvas with animated mesh gradient background ──────────
    ui.html('''
    <style>
    @keyframes hrmkit-drift {
        0%,100% { transform: translate(0,0) scale(1); }
        33%      { transform: translate(40px,-30px) scale(1.08); }
        66%      { transform: translate(-25px,20px) scale(.94); }
    }
    @keyframes hrmkit-spin {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }
    @keyframes hrmkit-float {
        0%,100% { transform: translateY(0); }
        50%      { transform: translateY(-10px); }
    }
    @keyframes hrmkit-pulse-ring {
        0%   { box-shadow: 0 0 0 0   rgba(124,58,237,.45); }
        70%  { box-shadow: 0 0 0 22px rgba(124,58,237,0);  }
        100% { box-shadow: 0 0 0 0   rgba(124,58,237,0);   }
    }
    .hrmkit-lock-page {
        position:relative;overflow:hidden;
        background:#0f0c2e;
        min-height:100vh;width:100%;
        display:flex;align-items:center;justify-content:center;
        padding:2rem;box-sizing:border-box;
    }
    .hrmkit-blob {
        position:absolute;border-radius:50%;filter:blur(90px);
        animation:hrmkit-drift 12s ease-in-out infinite;
        pointer-events:none;
    }
    .hrmkit-lock-icon {
        animation: hrmkit-float 3.2s ease-in-out infinite,
                   hrmkit-pulse-ring 2.4s ease-out infinite;
    }
    .hrmkit-plan-card {
        transition: transform .2s, box-shadow .2s;
        cursor:default;
    }
    .hrmkit-plan-card:hover {
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 20px 50px -12px rgba(0,0,0,.6) !important;
    }
    .hrmkit-cta-btn {
        border:none;cursor:pointer;
        transition: transform .15s, box-shadow .15s, filter .15s;
    }
    .hrmkit-cta-btn:hover {
        transform: translateY(-2px) scale(1.03);
        filter: brightness(1.1);
    }
    .hrmkit-cta-btn:active { transform: scale(.97); }
    .hrmkit-key-input {
        background: rgba(255,255,255,.08);
        border: 1.5px solid rgba(255,255,255,.18);
        border-radius: .75rem;
        color: #e2e8f0;
        padding: .65rem 1rem;
        font-size: .9rem;
        outline: none;
        width: 100%;
        box-sizing: border-box;
        transition: border-color .2s;
    }
    .hrmkit-key-input::placeholder { color: rgba(255,255,255,.35); }
    .hrmkit-key-input:focus { border-color: #818cf8; }
    </style>
    ''')

    with ui.element('div').classes('hrmkit-lock-page'):

        # ── Decorative blobs ─────────────────────────────────────────────
        ui.html(
            '<div class="hrmkit-blob" style="width:520px;height:520px;'
            'background:radial-gradient(circle,#4f46e5,transparent 70%);'
            'top:-120px;left:-160px;opacity:.55;"></div>'
            '<div class="hrmkit-blob" style="width:400px;height:400px;'
            'background:radial-gradient(circle,#7c3aed,transparent 70%);'
            'top:40%;right:-100px;opacity:.45;animation-delay:-4s;"></div>'
            '<div class="hrmkit-blob" style="width:320px;height:320px;'
            'background:radial-gradient(circle,#06b6d4,transparent 70%);'
            'bottom:-80px;left:30%;opacity:.35;animation-delay:-8s;"></div>'
        )

        # ── Grid dots overlay ─────────────────────────────────────────────
        ui.html(
            '<div style="position:absolute;inset:0;pointer-events:none;'
            'background-image:radial-gradient(rgba(255,255,255,.06) 1px,transparent 1px);'
            'background-size:32px 32px;"></div>'
        )

        # ── Main card ─────────────────────────────────────────────────────
        with ui.element('div').style(
            'position:relative;z-index:10;width:100%;max-width:860px;'
            'display:flex;flex-direction:column;align-items:center;gap:2rem;'
        ):

            # ── Brand badge ───────────────────────────────────────────────
            ui.html(
                '<div style="display:inline-flex;align-items:center;gap:.5rem;'
                'background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);'
                'border-radius:999px;padding:.35rem 1rem;backdrop-filter:blur(6px);">'
                '<span style="font-size:.75rem;font-weight:700;letter-spacing:.1em;'
                'text-transform:uppercase;color:#a5b4fc;">HRMkit Pro</span>'
                '<span style="width:6px;height:6px;border-radius:50%;background:#a5b4fc;'
                'display:inline-block;"></span>'
                '<span style="font-size:.75rem;color:#94a3b8;">License Required</span>'
                '</div>'
            )

            # ── Lock icon ─────────────────────────────────────────────────
            ui.html(
                '<div class="hrmkit-lock-icon" style="width:96px;height:96px;'
                'border-radius:1.75rem;'
                'background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 55%,#06b6d4 100%);'
                'display:flex;align-items:center;justify-content:center;font-size:2.8rem;'
                'box-shadow:0 16px 50px -8px rgba(79,70,229,.6);">'
                '🔒</div>'
            )

            # ── Headline block ────────────────────────────────────────────
            ui.html(
                f'<div style="text-align:center;">'
                f'<h1 style="font-size:2.4rem;font-weight:900;color:#f1f5f9;margin:0 0 .5rem;'
                f'letter-spacing:-.03em;line-height:1.1;">'
                f'Unlock <span style="background:linear-gradient(90deg,#818cf8,#c084fc,#22d3ee);'
                f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
                f'{page_title}</span></h1>'
                f'<p style="font-size:1rem;color:#94a3b8;margin:0;">'
                f'An active HRMkit license is needed to access this feature.</p>'
                f'</div>'
            )

            # ── Two-column: features + quick activate ─────────────────────
            with ui.element('div').style(
                'display:flex;gap:1.25rem;width:100%;flex-wrap:wrap;'
            ):

                # Left — feature list
                with ui.element('div').style(
                    'flex:1 1 320px;background:rgba(255,255,255,.05);'
                    'border:1px solid rgba(255,255,255,.1);border-radius:1.25rem;'
                    'padding:1.5rem;backdrop-filter:blur(8px);'
                ):
                    ui.html(
                        '<p style="font-size:.75rem;font-weight:700;letter-spacing:.1em;'
                        'text-transform:uppercase;color:#818cf8;margin:0 0 1rem;">'
                        '✦ Everything included</p>'
                    )
                    _features = [
                        ('#22d3ee', '📊', 'Full access to all HR management modules'),
                        ('#a78bfa', '👥', 'Unlimited employees, reports & data exports'),
                        ('#f472b6', '🤖', 'AI Orchestrator &amp; smart analytics engine'),
                        ('#34d399', '🔐', 'Role-based access control &amp; audit trails'),
                        ('#fb923c', '📅', 'Attendance, leave, holidays &amp; scheduling'),
                        ('#60a5fa', '📈', 'Payroll integration &amp; compliance reports'),
                    ]
                    for color, icon, text in _features:
                        ui.html(
                            f'<div style="display:flex;align-items:center;gap:.75rem;'
                            f'padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.06);">'
                            f'<div style="width:32px;height:32px;border-radius:.5rem;'
                            f'background:{color}22;display:flex;align-items:center;'
                            f'justify-content:center;font-size:1rem;flex-shrink:0;">{icon}</div>'
                            f'<span style="font-size:.87rem;color:#cbd5e1;">{text}</span>'
                            f'</div>'
                        )

                # Right — quick key entry + plans
                with ui.element('div').style(
                    'flex:1 1 280px;display:flex;flex-direction:column;gap:1rem;'
                ):

                    # Quick activate card
                    with ui.element('div').style(
                        'background:linear-gradient(135deg,rgba(79,70,229,.35),rgba(124,58,237,.3));'
                        'border:1px solid rgba(129,140,248,.35);border-radius:1.25rem;'
                        'padding:1.5rem;backdrop-filter:blur(8px);'
                    ):
                        ui.html(
                            '<p style="font-size:.75rem;font-weight:700;letter-spacing:.1em;'
                            'text-transform:uppercase;color:#a5b4fc;margin:0 0 .75rem;">'
                            '⚡ Quick Activate</p>'
                            '<p style="font-size:.82rem;color:#94a3b8;margin:0 0 .9rem;">'
                            'Already have a license key? Enter it below.</p>'
                        )
                        key_input = ui.input(placeholder='HRMkit-PLAN-XXXX-YYYY-ZZZZ') \
                            .props('outlined dense') \
                            .classes('w-full mb-3') \
                            .style(
                                'background:rgba(255,255,255,.07);'
                                'border-radius:.75rem;color:#e2e8f0;'
                            )

                        def _quick_activate():
                            from layout.license_guard import activate_license_key
                            ok, msg = activate_license_key(key_input.value)
                            if ok:
                                ui.notify(f'✅ {msg}', type='positive')
                                ui.timer(1.2, lambda: ui.navigate.reload(), once=True)
                            else:
                                ui.notify(f'❌ {msg}', type='negative')

                        ui.html(
                            '<button class="hrmkit-cta-btn" id="hrmkit-qa-btn" '
                            'style="width:100%;padding:.65rem;border-radius:.75rem;'
                            'background:linear-gradient(135deg,#4f46e5,#7c3aed);'
                            'color:#fff;font-size:.88rem;font-weight:700;'
                            'box-shadow:0 4px 18px -4px rgba(79,70,229,.6);">'
                            '🔑 Activate Now</button>'
                        )
                        # Actual button (hidden for styling, used for logic)
                        ui.button('Activate', on_click=_quick_activate) \
                            .props('flat dense') \
                            .style('display:none;') \
                            .classes('hrmkit-qa-real')
                        # Wire the styled button to the NiceGUI button via JS
                        ui.run_javascript(
                            'document.getElementById("hrmkit-qa-btn").onclick = () => '
                            'document.querySelector(".hrmkit-qa-real").click();'
                        )

                    # Pricing mini-cards
                    _plans = [
                        {'name': 'Starter',      'price': '$49',    'period': '/mo',
                         'seats': 'Up to 10 seats',
                         'from': '#0891b2', 'to': '#0e7490'},
                        {'name': 'Professional', 'price': '$149',   'period': '/mo',
                         'seats': 'Up to 50 seats',
                         'from': '#7c3aed', 'to': '#6d28d9', 'badge': 'Popular'},
                        {'name': 'Enterprise',   'price': 'Custom', 'period': '',
                         'seats': 'Unlimited seats',
                         'from': '#059669', 'to': '#047857'},
                    ]
                    with ui.element('div').style('display:flex;gap:.75rem;'):
                        for p in _plans:
                            badge_html = (
                                f'<div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);'
                                f'background:linear-gradient(90deg,#f59e0b,#ef4444);color:#fff;'
                                f'font-size:.65rem;font-weight:800;padding:.15rem .55rem;'
                                f'border-radius:999px;white-space:nowrap;letter-spacing:.05em;">'
                                f'{p["badge"]}</div>'
                            ) if p.get('badge') else ''
                            ui.html(
                                f'<div class="hrmkit-plan-card" style="flex:1 1 0%;position:relative;'
                                f'border-radius:1rem;padding:1rem .75rem;text-align:center;'
                                f'background:linear-gradient(145deg,{p["from"]}22,{p["to"]}11);'
                                f'border:1px solid {p["from"]}44;'
                                f'box-shadow:0 4px 20px -6px {p["from"]}55;">'
                                f'{badge_html}'
                                f'<div style="font-size:.78rem;font-weight:700;color:{p["from"]};'
                                f'margin-bottom:.25rem;">{p["name"]}</div>'
                                f'<div style="font-size:1.3rem;font-weight:900;color:#f1f5f9;">'
                                f'{p["price"]}<span style="font-size:.65rem;color:#94a3b8;">'
                                f'{p["period"]}</span></div>'
                                f'<div style="font-size:.7rem;color:#94a3b8;margin-top:.2rem;">'
                                f'{p["seats"]}</div>'
                                f'</div>'
                            )

            # ── CTA row ───────────────────────────────────────────────────
            with ui.element('div').style('display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;'):
                ui.html(
                    f'<button class="hrmkit-cta-btn" id="hrmkit-lic-btn" '
                    f'style="padding:.75rem 2.25rem;border-radius:.875rem;'
                    f'background:linear-gradient(135deg,#4f46e5,#7c3aed,#06b6d4);'
                    f'background-size:200% 200%;color:#fff;font-size:.95rem;font-weight:700;'
                    f'box-shadow:0 8px 28px -6px rgba(79,70,229,.7);">'
                    f'🔑 Manage License &amp; Pricing</button>'
                )
                ui.html(
                    '<button class="hrmkit-cta-btn" id="hrmkit-sales-btn" '
                    'style="padding:.75rem 2.25rem;border-radius:.875rem;'
                    'background:rgba(255,255,255,.07);'
                    'border:1.5px solid rgba(255,255,255,.2);'
                    'color:#e2e8f0;font-size:.95rem;font-weight:700;'
                    'backdrop-filter:blur(6px);">'
                    '💬 Talk to Sales</button>'
                )

            # Hidden NiceGUI buttons for routing
            nav_btn = ui.button('nav', on_click=lambda: ui.navigate.to(license_url)) \
                .style('display:none;').classes('hrmkit-nav-real')
            sales_btn = ui.button('sales', on_click=lambda: ui.notify('Our team will be in touch shortly!', type='info')) \
                .style('display:none;').classes('hrmkit-sales-real')

            ui.run_javascript(
                'document.getElementById("hrmkit-lic-btn").onclick   = () => document.querySelector(".hrmkit-nav-real").click();'
                'document.getElementById("hrmkit-sales-btn").onclick = () => document.querySelector(".hrmkit-sales-real").click();'
            )

            # ── Footer ────────────────────────────────────────────────────
            ui.html(
                '<p style="font-size:.78rem;color:#475569;text-align:center;">'
                'HRMkit &nbsp;·&nbsp; Enterprise HR Platform &nbsp;·&nbsp; '
                '<span style="color:#818cf8;">Secure · Scalable · Modern</span></p>'
            )


def require_license(page_title: str = 'This page') -> bool:
    """
    Call at the top of a protected page (after Sidebar()).
    Returns True and renders the lock overlay when no license is active.
    Returns False when the license is valid — page should render normally.

    Example:
        Sidebar()
        if require_license('Holiday Management'):
            return
        SetHolidays()
    """
    if is_license_active():
        return False
    show_locked_page(page_title)
    return True
