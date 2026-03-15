"""
License & Pricing Management Page
Displays software license details, active subscriptions, and available pricing plans.
"""
from nicegui import ui
from datetime import datetime, date
from layout.license_guard import activate_license_key, get_license_info, is_license_active


def create_license_pricing_page() -> None:
    """Render the full License & Pricing management page."""

    with ui.column().classes('w-full bg-gradient-to-br from-slate-100 to-indigo-50 min-h-screen p-6 gap-6'):

        # ── Gradient Header ───────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md text-white overflow-hidden') \
                .style('background:linear-gradient(135deg,#4f46e5,#7c3aed,#06b6d4);'):
            with ui.card_section().classes('px-8 py-6'):
                ui.html('<p style="font-size:.75rem;opacity:.75;letter-spacing:.08em;'
                        'text-transform:uppercase;margin-bottom:.5rem;">'
                        'Administration &#8250; License &amp; Pricing</p>')
                with ui.row().classes('items-center gap-5 w-full justify-between'):
                    with ui.row().classes('items-center gap-5'):
                        ui.html(
                            '<div style="width:52px;height:52px;border-radius:.75rem;'
                            'background:rgba(255,255,255,.18);display:flex;align-items:center;'
                            'justify-content:center;font-size:1.6rem;flex-shrink:0;">'
                            '&#128273;</div>'
                        )
                        with ui.column().classes('gap-1'):
                            ui.html('<h1 style="font-size:1.6rem;font-weight:900;margin:0;'
                                    'letter-spacing:-.02em;">License &amp; Pricing</h1>')
                            ui.html('<p style="font-size:.9rem;opacity:.82;margin:0;">'
                                    'Manage your HRMkit subscription, licenses, and billing</p>')
                    with ui.row().classes('gap-3'):
                        ui.button('\U0001f4e7 Contact Sales',
                                  on_click=lambda: ui.notify('Opening sales contact form...', type='info')) \
                            .style('background:rgba(255,255,255,.18);color:#fff;'
                                   'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                   'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')
                        ui.button('\U0001f4c4 Invoice History',
                                  on_click=lambda: ui.notify('Loading invoice history...', type='info')) \
                            .style('background:rgba(255,255,255,.18);color:#fff;'
                                   'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                                   'padding:.45rem 1.1rem;font-size:.85rem;font-weight:600;')

        # ── Tabs ─────────────────────────────────────────────────────────
        with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden'):
            tabs = ui.tabs().classes('w-full border-b border-slate-200')
            with tabs:
                t_overview = ui.tab('Current License',  icon='verified_user')
                t_plans    = ui.tab('Pricing Plans',    icon='local_offer')
                t_billing  = ui.tab('Billing & Usage',  icon='receipt_long')
                t_keys     = ui.tab('License Keys',     icon='vpn_key')

            with ui.tab_panels(tabs, value=t_overview).classes('w-full'):
                with ui.tab_panel(t_overview).classes('p-6'):
                    _license_overview_tab()
                with ui.tab_panel(t_plans).classes('p-6'):
                    _pricing_plans_tab()
                with ui.tab_panel(t_billing).classes('p-6'):
                    _billing_usage_tab()
                with ui.tab_panel(t_keys).classes('p-6'):
                    _license_keys_tab()


# ─────────────────────────────────────────────────────────────────────────────
# Tab 1 — Current License Overview
# ─────────────────────────────────────────────────────────────────────────────
def _license_overview_tab():
    # ── KPI strip ─────────────────────────────────────────────────────────
    _kpis = [
        {'icon': '\U0001f451', 'value': 'Enterprise', 'label': 'Current Plan',
         'sub': 'Renews Aug 2026',      'f': '#4f46e5', 't': '#7c3aed'},
        {'icon': '\U0001f46e', 'value': '150',         'label': 'Seat Licenses',
         'sub': '112 in use',           'f': '#0891b2', 't': '#0e7490'},
        {'icon': '\u2705',    'value': 'Active',      'label': 'License Status',
         'sub': 'Valid until Aug 2026', 'f': '#059669', 't': '#047857'},
        {'icon': '\U0001f4c5', 'value': '234',         'label': 'Days Remaining',
         'sub': 'Until renewal',        'f': '#d97706', 't': '#b45309'},
        {'icon': '\U0001f4b0', 'value': '$1 200',      'label': 'Monthly Cost',
         'sub': '$14 400 / year',       'f': '#be185d', 't': '#9d174d'},
    ]
    with ui.element('div').style(
        'display:flex;flex-wrap:nowrap;gap:1rem;width:100%;margin-bottom:1.5rem;'
    ):
        for c in _kpis:
            ui.html(
                f'<div style="flex:1 1 0%;background:linear-gradient(135deg,{c["f"]},{c["t"]});'
                'border-radius:1.25rem;padding:1.3rem 1.4rem;color:#fff;position:relative;'
                'overflow:hidden;box-shadow:0 6px 20px -5px rgba(0,0,0,.25);">'
                '<div style="position:absolute;top:-18px;right:-18px;width:80px;height:80px;'
                'border-radius:50%;background:rgba(255,255,255,.1);"></div>'
                f'<div style="font-size:1.5rem;margin-bottom:.35rem;">{c["icon"]}</div>'
                f'<div style="font-size:1.9rem;font-weight:900;line-height:1;">{c["value"]}</div>'
                f'<div style="font-size:.82rem;font-weight:700;opacity:.95;margin-top:.2rem;">{c["label"]}</div>'
                f'<div style="font-size:.75rem;opacity:.75;margin-top:.1rem;">{c["sub"]}</div>'
                '</div>'
            )

    # ── License details card + feature list ──────────────────────────────
    with ui.element('div').style('display:flex;gap:1.5rem;width:100%;flex-wrap:wrap;'):

        # Details
        with ui.element('div').style('flex:2 1 320px;background:#fff;border-radius:1.25rem;'
                                     'box-shadow:0 4px 18px -4px rgba(0,0,0,.1);overflow:hidden;'):
            with ui.element('div').style(
                'background:linear-gradient(90deg,#4f46e5,#7c3aed);padding:1rem 1.5rem;'
            ):
                ui.html('<h3 style="font-size:.95rem;font-weight:700;color:#fff;margin:0;">'
                        '\U0001f4cb License Details</h3>')
            with ui.element('div').style('padding:1.25rem 1.5rem;'):
                rows = [
                    ('License Type',     'Enterprise — Multi-site'),
                    ('License Holder',   'KWARECOM Inc.'),
                    ('License Number',   'HRMkit-ENT-2024-78543'),
                    ('Issue Date',       'August 15, 2024'),
                    ('Expiry Date',      'August 14, 2026'),
                    ('Seats Purchased',  '150 users'),
                    ('Seats Used',       '112 users  (38 available)'),
                    ('Modules Included', 'All — HR, Payroll, Analytics, AI'),
                    ('Support Level',    'Priority 24/7 + Dedicated CSM'),
                    ('Updates',          'Lifetime updates included'),
                ]
                for i, (k, v) in enumerate(rows):
                    bg = '#f8fafc' if i % 2 == 0 else '#ffffff'
                    ui.html(
                        f'<div style="display:flex;justify-content:space-between;'
                        f'padding:.65rem .5rem;background:{bg};border-radius:.5rem;'
                        'border-bottom:1px solid #f1f5f9;">'
                        f'<span style="font-size:.85rem;font-weight:600;color:#64748b;">{k}</span>'
                        f'<span style="font-size:.85rem;font-weight:700;color:#1e293b;">{v}</span>'
                        '</div>'
                    )

        # Included features
        with ui.element('div').style('flex:1 1 260px;background:#fff;border-radius:1.25rem;'
                                     'box-shadow:0 4px 18px -4px rgba(0,0,0,.1);overflow:hidden;'):
            with ui.element('div').style(
                'background:linear-gradient(90deg,#059669,#047857);padding:1rem 1.5rem;'
            ):
                ui.html('<h3 style="font-size:.95rem;font-weight:700;color:#fff;margin:0;">'
                        '\u2728 Included Features</h3>')
            with ui.element('div').style('padding:1.25rem 1.5rem;'):
                features = [
                    ('\U0001f465', 'Employee Management'),
                    ('\U0001f4ca', 'Advanced Analytics'),
                    ('\U0001f4c5', 'Leave & Attendance'),
                    ('\U0001f4b0', 'Payroll Integration'),
                    ('\u26a1',    'AI Orchestrator'),
                    ('\U0001f4cb', 'Custom Reports'),
                    ('\U0001f512', 'Role-Based Access'),
                    ('\U0001f310', 'API Access'),
                    ('\U0001f4be', 'Automated Backups'),
                    ('\U0001f4e7', 'Email Notifications'),
                    ('\U0001f4f1', 'Mobile Responsive'),
                    ('\U0001f9e0', 'AI-Powered Insights'),
                ]
                for icon, feat in features:
                    ui.html(
                        f'<div style="display:flex;align-items:center;gap:.6rem;'
                        'padding:.45rem 0;border-bottom:1px solid #f1f5f9;">'
                        f'<span style="font-size:1rem;">{icon}</span>'
                        f'<span style="font-size:.85rem;font-weight:600;color:#1e293b;">{feat}</span>'
                        '<span style="margin-left:auto;font-size:.75rem;background:#dcfce7;'
                        'color:#166534;padding:.18rem .55rem;border-radius:9999px;font-weight:700;">Included</span>'
                        '</div>'
                    )

    # ── Renew / Upgrade ───────────────────────────────────────────────────
    with ui.row().classes('gap-3 mt-4'):
        ui.button('\U0001f501 Renew License',
                  on_click=lambda: ui.notify('Opening license renewal...', type='info')) \
            .classes('bg-indigo-600 text-white px-6 py-2 rounded-xl font-bold')
        ui.button('\u2b06\ufe0f Upgrade Plan',
                  on_click=lambda: ui.notify('Loading upgrade options...', type='info')) \
            .classes('bg-purple-600 text-white px-6 py-2 rounded-xl font-bold')
        ui.button('\U0001f4e5 Download License',
                  on_click=lambda: ui.notify('Downloading license certificate...', type='info')) \
            .classes('bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 '
                     'px-5 py-2 rounded-xl font-semibold')


# ─────────────────────────────────────────────────────────────────────────────
# Tab 2 — Pricing Plans
# ─────────────────────────────────────────────────────────────────────────────
def _pricing_plans_tab():
    # Toggle billing period
    billing_period = {'monthly': True}

    ui.html(
        '<div style="text-align:center;margin-bottom:1.5rem;">'
        '<h2 style="font-size:1.4rem;font-weight:900;color:#1e293b;margin-bottom:.4rem;">'
        'Choose the Right Plan for Your Team</h2>'
        '<p style="color:#64748b;font-size:.9rem;">'
        'All plans include a 14-day free trial. No credit card required.</p>'
        '</div>'
    )

    # Billing toggle
    with ui.row().classes('justify-center gap-3 mb-6 items-center'):
        ui.label('Monthly').classes('font-semibold text-slate-600')
        period_toggle = ui.toggle(['Monthly', 'Annually'], value='Monthly') \
            .classes('text-sm')
        ui.html('<span style="background:#dcfce7;color:#166534;padding:.2rem .7rem;'
                'border-radius:9999px;font-size:.78rem;font-weight:700;">Save 20%</span>')

    # Plans data
    plans = [
        {
            'name': 'Starter',
            'icon': '\U0001f331',
            'monthly': 49,
            'annual_monthly': 39,
            'seats': 'Up to 10 users',
            'highlight': False,
            'badge': None,
            'color_from': '#64748b',
            'color_to': '#475569',
            'features': [
                'Employee management',
                'Basic attendance tracking',
                'Leave management',
                'Email notifications',
                'Standard reports',
                '5 GB storage',
                'Email support',
            ],
            'missing': ['Payroll integration', 'AI tools', 'API access', 'Custom branding'],
        },
        {
            'name': 'Professional',
            'icon': '\U0001f680',
            'monthly': 149,
            'annual_monthly': 119,
            'seats': 'Up to 50 users',
            'highlight': False,
            'badge': 'Popular',
            'color_from': '#4f46e5',
            'color_to': '#7c3aed',
            'features': [
                'Everything in Starter',
                'Payroll integration',
                'Advanced analytics',
                'Custom reports',
                'Role-based access',
                '50 GB storage',
                'Priority email + chat',
                'API access',
            ],
            'missing': ['AI Orchestrator', 'Multi-site', 'Dedicated CSM'],
        },
        {
            'name': 'Business',
            'icon': '\U0001f3e2',
            'monthly': 349,
            'annual_monthly': 279,
            'seats': 'Up to 150 users',
            'highlight': True,
            'badge': 'Best Value',
            'color_from': '#0891b2',
            'color_to': '#0e7490',
            'features': [
                'Everything in Professional',
                'AI Orchestrator',
                'Multi-site support',
                'Automated backups',
                'Custom branding',
                '500 GB storage',
                '24/7 phone support',
                'Onboarding assistance',
            ],
            'missing': ['Dedicated CSM', 'SLA guarantee'],
        },
        {
            'name': 'Enterprise',
            'icon': '\U0001f451',
            'monthly': 'Custom',
            'annual_monthly': 'Custom',
            'seats': 'Unlimited users',
            'highlight': False,
            'badge': 'Current Plan',
            'color_from': '#be185d',
            'color_to': '#9d174d',
            'features': [
                'Everything in Business',
                'Unlimited users',
                'Dedicated CSM',
                'SLA guarantee (99.9%)',
                'Custom integrations',
                'Unlimited storage',
                'On-premise option',
                'Security audit support',
                'Custom contract terms',
            ],
            'missing': [],
        },
    ]

    with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1.25rem;width:100%;'):
        for plan in plans:
            highlight_style = (
                'box-shadow:0 12px 40px -8px rgba(8,145,178,.4);'
                'transform:scale(1.02);'
                if plan['highlight'] else
                'box-shadow:0 4px 18px -4px rgba(0,0,0,.12);'
            )
            badge_html = ''
            if plan['badge']:
                badge_bg = '#fef3c7' if plan['badge'] != 'Current Plan' else '#dbeafe'
                badge_fg = '#92400e' if plan['badge'] != 'Current Plan' else '#1e40af'
                badge_html = (
                    f'<span style="position:absolute;top:.75rem;right:.75rem;'
                    f'background:{badge_bg};color:{badge_fg};padding:.2rem .7rem;'
                    'border-radius:9999px;font-size:.72rem;font-weight:800;">'
                    f'{plan["badge"]}</span>'
                )

            price_val = plan['monthly']
            price_html = (
                f'<div style="font-size:2.4rem;font-weight:900;line-height:1;">'
                f'${price_val}</div><div style="font-size:.8rem;opacity:.8;">/month</div>'
                if isinstance(price_val, int) else
                '<div style="font-size:2rem;font-weight:900;">Custom</div>'
                '<div style="font-size:.8rem;opacity:.8;">Contact us</div>'
            )

            feat_html = ''
            for f in plan['features']:
                feat_html += (
                    f'<div style="display:flex;align-items:center;gap:.5rem;'
                    'padding:.3rem 0;font-size:.85rem;color:#1e293b;">'
                    '<span style="color:#059669;font-weight:900;">\u2713</span>'
                    f'{f}</div>'
                )
            for f in plan['missing']:
                feat_html += (
                    f'<div style="display:flex;align-items:center;gap:.5rem;'
                    'padding:.3rem 0;font-size:.85rem;color:#94a3b8;">'
                    '<span style="color:#cbd5e1;font-weight:900;">\u2715</span>'
                    f'{f}</div>'
                )

            ui.html(
                f'<div style="flex:1 1 220px;border-radius:1.25rem;overflow:hidden;'
                f'background:#fff;position:relative;{highlight_style}">'
                f'<div style="height:6px;background:linear-gradient(90deg,{plan["color_from"]},{plan["color_to"]});"></div>'
                f'{badge_html}'
                f'<div style="background:linear-gradient(135deg,{plan["color_from"]},{plan["color_to"]});'
                'color:#fff;padding:1.5rem 1.4rem;">'
                f'<div style="font-size:1.8rem;margin-bottom:.4rem;">{plan["icon"]}</div>'
                f'<div style="font-size:1.1rem;font-weight:800;margin-bottom:.25rem;">{plan["name"]}</div>'
                f'<div style="font-size:.8rem;opacity:.8;margin-bottom:1rem;">{plan["seats"]}</div>'
                f'{price_html}'
                '</div>'
                '<div style="padding:1.25rem 1.4rem;">'
                f'{feat_html}'
                '<div style="margin-top:1rem;">'
                '<button style="width:100%;padding:.65rem;background:linear-gradient(90deg,'
                f'{plan["color_from"]},{plan["color_to"]});color:#fff;border:none;'
                'border-radius:.75rem;font-size:.88rem;font-weight:700;cursor:pointer;">'
                + ('Get Started' if plan['badge'] != 'Current Plan' else '\u2714\ufe0f Current Plan') +
                '</button>'
                '</div>'
                '</div></div>'
            )

    ui.html(
        '<div style="text-align:center;margin-top:1.5rem;padding:1.25rem;'
        'background:#f8fafc;border-radius:1rem;color:#64748b;font-size:.875rem;">'
        '\U0001f512 All plans include SSL encryption, GDPR compliance tools, and regular security updates.'
        '</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Tab 3 — Billing & Usage
# ─────────────────────────────────────────────────────────────────────────────
def _billing_usage_tab():
    # ── Header card ───────────────────────────────────────────────────────
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#0891b2,#0e7490);padding:1rem 1.5rem;'
        ):
            with ui.row().classes('items-center justify-between w-full'):
                ui.html('<h2 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0;">'
                        '\U0001f4b3 Billing &amp; Usage</h2>')
                with ui.row().classes('gap-2'):
                    ui.button('\U0001f4e5 Download Invoice',
                              on_click=lambda: ui.notify('Downloading invoice PDF...', type='info')) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')
                    ui.button('\U0001f4b3 Update Payment',
                              on_click=lambda: ui.notify('Opening payment settings...', type='info')) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')

    # Usage bar cards
    usage_items = [
        {'label': 'Seat Licenses',    'used': 112, 'total': 150, 'color': '#4f46e5'},
        {'label': 'API Calls (mo.)',  'used': 48200, 'total': 100000, 'color': '#0891b2'},
        {'label': 'Storage Used',     'used': 142, 'total': 500,   'color': '#059669'},
        {'label': 'Report Exports',   'used': 67,  'total': 200,   'color': '#d97706'},
    ]

    with ui.element('div').style('display:flex;flex-wrap:wrap;gap:1rem;width:100%;margin-bottom:1.5rem;'):
        for u in usage_items:
            pct = min(100, round(u['used'] / u['total'] * 100))
            warn_color = '#dc2626' if pct >= 90 else ('#d97706' if pct >= 70 else u['color'])
            used_label = f'{u["used"]:,}' if isinstance(u['used'], int) and u['used'] > 999 else str(u['used'])
            total_label = f'{u["total"]:,}' if isinstance(u['total'], int) and u['total'] > 999 else str(u['total'])
            ui.html(
                f'<div style="flex:1 1 200px;background:#fff;border-radius:1rem;'
                'box-shadow:0 4px 18px -4px rgba(0,0,0,.1);padding:1.25rem 1.4rem;">'
                f'<div style="font-weight:700;color:#1e293b;font-size:.9rem;margin-bottom:.6rem;">{u["label"]}</div>'
                f'<div style="font-size:1.6rem;font-weight:900;color:{warn_color};">{used_label}'
                f'<span style="font-size:.9rem;color:#94a3b8;font-weight:500;"> / {total_label}</span></div>'
                '<div style="background:#f1f5f9;border-radius:9999px;height:8px;margin-top:.6rem;overflow:hidden;">'
                f'<div style="height:100%;width:{pct}%;background:linear-gradient(90deg,{warn_color},{warn_color}cc);'
                'border-radius:9999px;transition:width .5s;"></div>'
                '</div>'
                f'<div style="font-size:.78rem;color:#94a3b8;margin-top:.3rem;">{pct}% used</div>'
                '</div>'
            )

    # Invoice table
    with ui.card().classes('w-full rounded-2xl shadow-sm bg-white overflow-hidden mb-4'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#1e293b22,#1e293b11);'
            'border-bottom:2px solid #e2e8f0;padding:.9rem 1.5rem;'
        ):
            ui.html('<h3 style="font-size:.95rem;font-weight:700;color:#1e293b;margin:0;">'
                    '\U0001f9fe Invoice History</h3>')
        with ui.element('div').style('padding:0;overflow-x:auto;'):
            invoices = [
                ('INV-2026-003', 'March 2026',   '$1,200.00', 'Enterprise 150 seats', 'Paid',     '#dcfce7', '#166534'),
                ('INV-2026-002', 'February 2026', '$1,200.00', 'Enterprise 150 seats', 'Paid',    '#dcfce7', '#166534'),
                ('INV-2026-001', 'January 2026',  '$1,200.00', 'Enterprise 150 seats', 'Paid',    '#dcfce7', '#166534'),
                ('INV-2025-012', 'December 2025', '$1,200.00', 'Enterprise 150 seats', 'Paid',    '#dcfce7', '#166534'),
                ('INV-2025-011', 'November 2025', '$1,200.00', 'Enterprise 150 seats', 'Paid',    '#dcfce7', '#166534'),
                ('INV-2025-010', 'October 2025',  '$1,200.00', 'Enterprise 150 seats', 'Paid',    '#dcfce7', '#166534'),
            ]
            thead = (
                '<thead><tr style="background:linear-gradient(90deg,#4f46e5,#7c3aed);color:#fff;">'
                '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Invoice</th>'
                '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Period</th>'
                '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Amount</th>'
                '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Description</th>'
                '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Status</th>'
                '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Action</th>'
                '</tr></thead>'
            )
            tbody = '<tbody>'
            for i, (inv, period, amount, desc, status, sbg, sfg) in enumerate(invoices):
                bg = '#f8fafc' if i % 2 == 0 else '#ffffff'
                tbody += (
                    f'<tr style="background:{bg};border-bottom:1px solid #e2e8f0;">'
                    f'<td style="padding:.7rem 1rem;font-weight:700;color:#1e293b;font-size:.85rem;">{inv}</td>'
                    f'<td style="padding:.7rem 1rem;color:#475569;font-size:.85rem;">{period}</td>'
                    f'<td style="padding:.7rem 1rem;font-weight:700;color:#059669;font-size:.88rem;">{amount}</td>'
                    f'<td style="padding:.7rem 1rem;color:#475569;font-size:.85rem;">{desc}</td>'
                    f'<td style="padding:.7rem 1rem;text-align:center;">'
                    f'<span style="padding:.22rem .65rem;border-radius:9999px;background:{sbg};color:{sfg};'
                    f'font-size:.75rem;font-weight:700;">{status}</span></td>'
                    f'<td style="padding:.7rem 1rem;text-align:center;">'
                    '<button style="padding:.3rem .8rem;background:#eff6ff;color:#1d4ed8;'
                    'border:1px solid #bfdbfe;border-radius:.5rem;font-size:.78rem;'
                    'font-weight:600;cursor:pointer;">\U0001f4e5 PDF</button></td>'
                    '</tr>'
                )
            tbody += '</tbody>'
            ui.html(
                f'<table style="width:100%;border-collapse:collapse;">{thead}{tbody}</table>'
            )

    # Payment method card
    with ui.card().classes('w-full rounded-2xl shadow-sm bg-white overflow-hidden'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#4f46e522,#7c3aed11);'
            'border-bottom:2px solid #e0e7ff;padding:.9rem 1.5rem;'
        ):
            ui.html('<h3 style="font-size:.95rem;font-weight:700;color:#4338ca;margin:0;">'
                    '\U0001f4b3 Payment Method</h3>')
        with ui.element('div').style('padding:1.25rem 1.5rem;display:flex;gap:1rem;flex-wrap:wrap;'):
            ui.html(
                '<div style="flex:1 1 260px;display:flex;align-items:center;gap:1rem;">'
                '<div style="background:linear-gradient(135deg,#1a1a2e,#16213e);'
                'border-radius:.75rem;padding:1rem 1.5rem;color:#fff;min-width:200px;">'
                '<div style="font-size:.7rem;opacity:.6;letter-spacing:.08em;">CREDIT CARD</div>'
                '<div style="font-size:1rem;font-weight:700;letter-spacing:.12em;margin:.6rem 0;">**** **** **** 4242</div>'
                '<div style="display:flex;justify-content:space-between;font-size:.78rem;opacity:.8;">'
                '<span>KWARECOM Inc.</span><span>08 / 27</span></div>'
                '</div>'
                '<div>'
                '<div style="font-weight:600;font-size:.9rem;color:#1e293b;">Visa ending in 4242</div>'
                '<div style="font-size:.82rem;color:#64748b;">Expires August 2027</div>'
                '<div style="font-size:.82rem;color:#64748b;">Billing cycle: 15th of each month</div>'
                '</div>'
                '</div>'
            )
            with ui.column().classes('gap-2 justify-center'):
                ui.button('\u270f\ufe0f Update Card',
                          on_click=lambda: ui.notify('Opening card update form...', type='info')) \
                    .classes('bg-indigo-600 text-white px-5 py-2 rounded-xl font-semibold text-sm')
                ui.button('\U0001f501 Change Plan',
                          on_click=lambda: ui.notify('Loading plan options...', type='info')) \
                    .classes('bg-slate-100 text-slate-700 border border-slate-200 px-5 py-2 rounded-xl font-semibold text-sm')


# ─────────────────────────────────────────────────────────────────────────────
# Tab 4 — License Keys
# ─────────────────────────────────────────────────────────────────────────────
def _license_keys_tab():
    with ui.card().classes('w-full rounded-2xl shadow-md bg-white overflow-hidden mb-4'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#475569,#334155);padding:1rem 1.5rem;'
        ):
            with ui.row().classes('items-center justify-between w-full'):
                ui.html('<h2 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0;">'
                        '\U0001f511 License Keys &amp; Activation</h2>')
                with ui.row().classes('gap-2'):
                    ui.button('+ Add License',
                              on_click=lambda: _show_add_license_dialog()) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')
                    ui.button('\U0001f504 Refresh',
                              on_click=lambda: ui.notify('Refreshing license data...', type='info')) \
                        .style('background:rgba(255,255,255,.18);color:#fff;'
                               'border:1px solid rgba(255,255,255,.35);border-radius:.75rem;'
                               'padding:.4rem 1rem;font-size:.82rem;font-weight:600;')

    keys = [
        {
            'key': 'HRMkit-ENT-2024-78543-XXXXXX',
            'module': 'Enterprise — Full Suite',
            'activated': 'Aug 15, 2024',
            'expires': 'Aug 14, 2026',
            'seats': 150,
            'status': 'Active',
            'status_bg': '#dcfce7',
            'status_fg': '#166534',
        },
        {
            'key': 'HRMkit-AI-2024-99123-YYYYYY',
            'module': 'AI Orchestrator Add-on',
            'activated': 'Sep 01, 2024',
            'expires': 'Aug 14, 2026',
            'seats': 150,
            'status': 'Active',
            'status_bg': '#dcfce7',
            'status_fg': '#166534',
        },
        {
            'key': 'HRMkit-API-2024-55432-ZZZZZZ',
            'module': 'API Gateway Access',
            'activated': 'Sep 01, 2024',
            'expires': 'Aug 14, 2026',
            'seats': 50,
            'status': 'Active',
            'status_bg': '#dcfce7',
            'status_fg': '#166534',
        },
    ]

    with ui.element('div').style('overflow-x:auto;border-radius:1rem;'
                                 'box-shadow:0 2px 12px -3px rgba(0,0,0,.1);'):
        thead = (
            '<thead><tr style="background:linear-gradient(90deg,#475569,#334155);color:#fff;">'
            '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">License Key</th>'
            '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Module</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Seats</th>'
            '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Activated</th>'
            '<th style="padding:.75rem 1rem;text-align:left;font-size:.82rem;">Expires</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Status</th>'
            '<th style="padding:.75rem 1rem;text-align:center;font-size:.82rem;">Actions</th>'
            '</tr></thead>'
        )
        tbody = '<tbody>'
        for i, k in enumerate(keys):
            bg = '#f8fafc' if i % 2 == 0 else '#ffffff'
            tbody += (
                f'<tr style="background:{bg};border-bottom:1px solid #e2e8f0;">'
                f'<td style="padding:.7rem 1rem;font-family:monospace;font-size:.82rem;color:#4338ca;font-weight:600;">'
                f'{k["key"]}</td>'
                f'<td style="padding:.7rem 1rem;font-weight:600;color:#1e293b;font-size:.85rem;">{k["module"]}</td>'
                f'<td style="padding:.7rem 1rem;text-align:center;color:#475569;font-size:.85rem;">{k["seats"]}</td>'
                f'<td style="padding:.7rem 1rem;color:#475569;font-size:.85rem;">{k["activated"]}</td>'
                f'<td style="padding:.7rem 1rem;color:#475569;font-size:.85rem;">{k["expires"]}</td>'
                f'<td style="padding:.7rem 1rem;text-align:center;">'
                f'<span style="padding:.2rem .65rem;border-radius:9999px;background:{k["status_bg"]};'
                f'color:{k["status_fg"]};font-size:.75rem;font-weight:700;">{k["status"]}</span></td>'
                '<td style="padding:.7rem 1rem;text-align:center;">'
                '<div style="display:flex;gap:.4rem;justify-content:center;">'
                '<button style="padding:.28rem .7rem;background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;'
                'border-radius:.5rem;font-size:.75rem;font-weight:600;cursor:pointer;">\U0001f4cb Copy</button>'
                '<button style="padding:.28rem .7rem;background:#fff1f2;color:#be123c;border:1px solid #fecdd3;'
                'border-radius:.5rem;font-size:.75rem;font-weight:600;cursor:pointer;">\U0001f6ab Revoke</button>'
                '</div></td>'
                '</tr>'
            )
        tbody += '</tbody>'
        ui.html(f'<table style="width:100%;border-collapse:collapse;">{thead}{tbody}</table>')

    # Add license key form
    with ui.card().classes('w-full rounded-2xl shadow-sm bg-white overflow-hidden mt-4'):
        with ui.element('div').style(
            'background:linear-gradient(90deg,#4f46e522,#7c3aed11);'
            'border-bottom:2px solid #e0e7ff;padding:.9rem 1.5rem;'
        ):
            ui.html('<h3 style="font-size:.95rem;font-weight:700;color:#4338ca;margin:0;">'
                    '\u2795 Activate a New License Key</h3>')
        with ui.element('div').style('padding:1.25rem 1.5rem;'):
            with ui.row().classes('w-full gap-4 items-end'):
                new_key_input = ui.input(
                    'License Key',
                    placeholder='HRMkit-XXX-YYYY-ZZZZZ-WWWWWW'
                ).classes('flex-1')
                ui.button('\u2705 Activate Key',
                          on_click=lambda: _activate_key(new_key_input.value)) \
                    .classes('bg-indigo-600 text-white px-6 py-2 rounded-xl font-bold')


def _activate_key(key: str, holder: str = '', plan: str = 'Enterprise') -> None:
    success, message = activate_license_key(key, holder=holder, plan=plan)
    if success:
        ui.notify(f'\u2705 {message}', type='positive')
        ui.timer(1.5, lambda: ui.navigate.reload(), once=True)
    else:
        ui.notify(f'\u274c {message}', type='negative')


def _show_add_license_dialog():
    with ui.dialog() as dialog, ui.card().classes('w-[500px]'):
        ui.label('Add / Activate License').classes('text-xl font-bold mb-1')
        ui.label('Enter your new license key to activate a module.').classes('text-slate-500 text-sm mb-4')
        key_in = ui.input('License Key', placeholder='HRMkit-XXX-YYYY-ZZZZZ-WWWWWW').classes('w-full mb-3')
        module_in = ui.select(
            ['Enterprise Suite', 'AI Orchestrator', 'API Gateway', 'Payroll Module', 'Mobile App'],
            label='Module'
        ).classes('w-full mb-4')
        with ui.row().classes('gap-3 w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close) \
                .classes('bg-slate-100 text-slate-700 border border-slate-200 px-4 py-2 rounded-xl font-semibold')
            ui.button('\u2705 Activate', on_click=lambda: [
                _activate_key(key_in.value, plan=module_in.value or 'Enterprise'),
                dialog.close()
            ]).classes('bg-indigo-600 text-white px-5 py-2 rounded-xl font-bold')
    dialog.open()
