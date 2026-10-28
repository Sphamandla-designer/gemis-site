#!/usr/bin/env python3
"""
The canonical story data for the GEMIS Stories update.

Every fact here traces to GEMIS_case_study_videos.md — either the narration or a
"Relationship or period" line, both of which the implementation prompt counts as
confirmed — or to the brief. Summaries and transcripts are copied verbatim from
that file and must never be edited or paraphrased.

Anything not confirmed carries a `tbc` id instead of a value. Those ids are
listed in OPEN_ITEMS.md and counted by scripts/check-tbc.mjs.

Figures shown on app screens inside the videos are sample data. They are not
quoted anywhere, per the video document's own instruction.
"""
import json
import os
import re

VIDEO_DIR = 'assets/video/case-studies/'
CANONICAL = 'https://sphamandla-designer.github.io/gemis-site/'
BASE_URL = CANONICAL + VIDEO_DIR

# The three relationships that begin the story. Colour is never the only marker:
# every thread also carries its client name as text.
FOUNDING = ['sbs-waterproofing', 'homeassist', 'wastemart']

# The people whose words appear on the site. Names, titles and companies are
# from facts.md. The quotations themselves are read, character for character,
# from endorsements.md (see load_endorsements below); nothing is ever written
# here. A person with no line in that file has no card on the live build.
ENDORSERS = {
    'keshan-patel': dict(
        name='Keshan Patel', title='CEO', company='HomeAssist (Pty) Ltd', slug='homeassist',
        since='Client since 2014', initials='KP', line_tbc='endorsement-keshan-line'),
    'ryan-smith': dict(
        name='Ryan Smith', title=None, company='SBS Waterproofing', slug='sbs-waterproofing',
        since='Client since 2014', initials='RS', line_tbc='endorsement-ryan-line'),
    'philippine-francke': dict(
        name='Philippine Francke', title='Managing Director', company='HashTopic', slug=None,
        since=None, initials='PF', line_tbc='endorsement-philippine-line'),
    'nazier-mathinus': dict(
        name='Nazier Mathinus', title=None, company='WasteMart', slug='wastemart',
        since=None, initials='NM', line_tbc='endorsement-nazier-line'),
}
# the homepage order
ENDORSEMENT_ORDER = ['keshan-patel', 'ryan-smith', 'philippine-francke']

ENDORSEMENTS_FILE = None
for _cand in ('_project/assets-incoming/content/endorsements.md', 'scripts/endorsements.md'):
    _p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), _cand)
    if os.path.exists(_p):
        ENDORSEMENTS_FILE = _p
        break


def load_endorsements():
    """
    endorsements.md → {key: line}. The file is the source of truth and the
    quotations are copied exactly: a line is taken verbatim from the block
    under the person's name (a "## Name" or "### Name" heading, or a "**Name**"
    label), with only the surrounding whitespace and any blockquote marker
    removed. Nothing is paraphrased, shortened or added.
    """
    if not ENDORSEMENTS_FILE:
        return {}
    text = open(ENDORSEMENTS_FILE, encoding='utf-8').read()
    found = {}
    for key, e in ENDORSERS.items():
        m = re.search(r'(?:^#{1,4}\s*|^\*\*)' + re.escape(e['name']) + r'\b[^\n]*\n(.*?)(?=^#{1,4}\s|^\*\*|\Z)', text, flags=re.S | re.M)
        if not m:
            continue
        body = m.group(1)
        lines = []
        for ln in body.splitlines():
            ln = re.sub(r'^\s*>\s?', '', ln.rstrip())
            if ln.strip():
                lines.append(ln.strip())
        if lines:
            found[key] = ' '.join(lines).strip()
    return found


ENDORSEMENT_LINES = load_endorsements()
for _k, _e in ENDORSERS.items():
    _e['line'] = ENDORSEMENT_LINES.get(_k)

STORIES = [
    dict(
        slug='sbs-waterproofing', client='SBS Waterproofing', order=1,
        industry='Construction services — waterproofing and roofing',
        period='Client since 2014 · system since 2015', period_tbc=None,
        since='2014', since_tbc=None,
        headline='The system behind more than a decade of growth',
        challenge='Website and Google campaigns from 2014; their own business system '
                  'from 2015, which grew into ManaGEM',
        outcome='Still running the business on the system GEMIS built, more than ten years on',
        endorser='ryan-smith',
        capabilities=['Enquiry capture and sales pipeline, with an SMS reference number to the customer',
                      'Every call, email and appointment tracked through to the sale',
                      'Quotes accepted online, with the deposit invoice following automatically into accounting',
                      'Profit shown per project',
                      'Stock reorder reminders'],
        tech='Microsoft Azure · .NET · SQL · mobile',
        video='SBS_explainer',
        video_title='SBS Waterproofing: the system behind more than a decade of growth',
        duration='PT1M17S', duration_label='1:17',
        keywords='CRM and sales pipeline, online quote acceptance, automatic invoicing, accounting integration, job profitability, stock management, SME growth',
        about='SBS Waterproofing (Cape Town)',
        capability_tags=['platforms'], industry_tag='construction',
    ),
    dict(
        slug='homeassist', client='HomeAssist', order=2,
        industry='Insurance and home services — plumbing repairs',
        period='Client since 2014', period_tbc=None,
        since='2014', since_tbc=None,
        headline='Plumbing claims, from report to sign-off',
        challenge='One system for burst-geyser and plumbing jobs: nearest-plumber dispatch, '
                  'SMS and WhatsApp updates, SANS photo evidence, insurer and warranty links',
        outcome='Every job across the country visible in one place, from first report to sign-off',
        endorser='keshan-patel',
        capabilities=['Homeowners report online, or insurers log the claim',
                      'The next available plumber near the job is assigned automatically from a national panel',
                      'Customers kept informed by SMS or WhatsApp at every step',
                      'Plumbers photograph each step in the app, proving SANS compliance',
                      'Direct links to insurers and manufacturers check warranties and update claims'],
        tech='Microsoft Azure · .NET · SQL · mobile',
        video='HomeAssist_explainer',
        video_title='HomeAssist: plumbing claims, from report to sign-off',
        duration='PT1M29S', duration_label='1:29',
        keywords='job dispatch, field service app, insurer integration, warranty checks, SANS compliance, SMS and WhatsApp notifications, national dashboard',
        about='HomeAssist',
        capability_tags=['field-operations', 'integration'], industry_tag='insurance',
    ),
    dict(
        slug='wastemart', client='WasteMart', order=3,
        industry='Waste management and skip hire',
        period='Client for more than ten years', period_tbc=None,
        since=None, since_tbc=None,
        headline='From quote to collection, handled',
        challenge='Automatic quotes with terms, secure payment links, scheduling, '
                  'driver scan confirmation, order tracking',
        outcome='Every order visible from quote to collection, for managers and customers alike',
        endorser='nazier-mathinus',
        capabilities=['Quotes priced automatically, with standard terms and conditions attached',
                      'Customers accept and pay through a secure link',
                      'Operations alerted the moment payment lands, and the job goes onto the schedule',
                      'Planners assign truck and driver; the driver confirms collection with a scan',
                      'Managers and customers can both track the order'],
        tech='Microsoft Azure · .NET · SQL · mobile',
        video='WasteMart_explainer',
        video_title='WasteMart: from quote to collection, handled',
        duration='PT1M29S', duration_label='1:29',
        keywords='automated quoting, online payment links, scheduling, driver mobile app, barcode scan confirmation, order tracking',
        about='WasteMart',
        capability_tags=['field-operations', 'platforms'], industry_tag='waste',
        metric='Six hours a week back, per depot',
    ),
    dict(
        slug='trans-hex', client='Trans Hex Group', order=4,
        industry='Mining — diamonds',
        period='2017', period_tbc=None, since=None, since_tbc=None,
        headline='From a weeks-long report to one click',
        challenge='Baken mine: SAP data feed automated and an integrated management report built in',
        outcome='A report that took weeks became available on demand',
        endorser=None,
        capabilities=['The company’s own information system stabilised first',
                      'Daily SAP financial feed automated — scheduled, de-duplicated, logged, with failure emails',
                      'Integrated management report across plant, mining, finance, security and HR',
                      'Budget against actual for month and year to date, filterable by mine and period',
                      'Export to Excel and PDF; version two added weekly figures, forecasts, variances and live exchange rates'],
        tech='SAP integration · SQL · reporting',
        video='TransHex_explainer',
        video_title='Trans Hex Group: from a weeks-long report to one click',
        duration='PT1M21S', duration_label='1:21',
        keywords='management information system (MIS), SAP data import, KPI reporting, budget vs actual, mining operations reporting, Excel and PDF export',
        about='Trans Hex Group (Baken mine, Lower Orange River)',
        capability_tags=['integration'], industry_tag='mining',
    ),
    dict(
        slug='sonke', client='Sonke Gender Justice', order=5,
        industry='Non-profit — gender-based violence and HIV prevention',
        period='2018', period_tbc=None, since=None, since_tbc=None,
        headline='Monitoring and evaluation across Africa',
        challenge='Offline mobile capture, approval workflow, programme targets and donor '
                  'reporting, for work in 40 countries',
        outcome='Donor reports build from data that has already been checked',
        endorser=None,
        capabilities=['Facilitators capture each session on a mobile app that works offline and syncs when there is signal',
                      'M&amp;E officers check and approve what comes in, so every number traces to a real activity',
                      'Programme managers see progress against targets by country and programme',
                      'Each role sees the view it needs — country teams their country, leadership the whole picture',
                      'Donor reports assemble from already-verified data'],
        tech='Mobile · offline sync · SQL · reporting',
        video='Sonke_explainer',
        video_title='Sonke Gender Justice: monitoring and evaluation across Africa',
        duration='PT1M22S', duration_label='1:22',
        keywords='monitoring and evaluation (M&E), offline mobile data capture, approval workflow, programme targets, role-based dashboards, donor reporting',
        about='Sonke Gender Justice',
        capability_tags=['field-operations', 'integration'], industry_tag='non-profit',
    ),
    dict(
        slug='tores-foundation', client="Tore's Foundation", order=6,
        industry='Education — schools debating programme',
        period='2014', period_tbc=None, since=None, since_tbc=None,
        headline='A debating platform for 24 schools',
        challenge='Built for the University of Stellenbosch Business School: competitions, '
                  'live standings, mobile expense and stipend claims for 430+ learners',
        outcome='More time for debate, less time on admin',
        endorser=None,
        capabilities=['Competitions set up in minutes: schools, rounds, motions and judges',
                      'Results captured as each debate ends, with standings updating straight away',
                      'Coaches claim expenses and stipends in the same web app — pick the session, snap the receipt, submit',
                      'The programme team checks every claim against the sessions actually run',
                      'One approved payment batch goes to finance'],
        tech='Web platform · mobile capture · SQL',
        video='Tores_debating_platform',
        video_title="Tore's Foundation: a debating platform for 24 schools",
        duration='PT1M22S', duration_label='1:22',
        keywords='competition management, live standings, mobile expense claims, stipend payments, approval workflow, education programme admin',
        about="Tore's Foundation programme, for the University of Stellenbosch Business School",
        capability_tags=['platforms'], industry_tag='education',
    ),
    dict(
        slug='managem', client='ManaGEM', order=7,
        industry='Business management software — compact ERP',
        period='Developed from the SBS Waterproofing system of 2015', period_tbc=None, since=None, since_tbc=None,
        headline='Born in a real business, built for many',
        challenge='Generalised from the system built for SBS Waterproofing in 2015 into a platform other businesses could run on',
        outcome='About a dozen companies run their day-to-day operations on it',
        endorser='ryan-smith',
        capabilities=['Capture every enquiry and follow it to the sale, with SMS and email updates',
                      'Quotes accepted online, with deposit invoices following automatically',
                      'Project tracking with the profit on each job',
                      'Stock levels with an alert before you run out',
                      'Products, prices and staff records in the same system'],
        tech='Microsoft Azure · .NET · SQL',
        video='ManaGEM_explainer',
        video_title='ManaGEM: born in a real business, built for many',
        duration='PT1M6S', duration_label='1:06',
        keywords='ERP, business management software, CRM, quoting, invoicing, project costing, stock control, SME operations',
        about='ManaGEM (GEMIS product)', about_type='SoftwareApplication',
        capability_tags=['platforms'], industry_tag='software',
        is_product=True,
    ),
]

# Summaries and transcripts are NOT typed here. They are machine-extracted from
# GEMIS_case_study_videos.md into scripts/video-text.json and attached below, so a
# retyped apostrophe can never drift from the source. Regenerate that file with
# scripts/extract-video-text.py if the source document changes.
_TEXT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'video-text.json'), encoding='utf-8'))
for _s in STORIES:
    _t = _TEXT[_s['video']]
    _s['summary'] = _t['summary']
    _s['transcript'] = _t['transcript']

BY_SLUG = {s['slug']: s for s in STORIES}

# The six that get their own story page. ManaGEM is a product, and its page is
# solutions/managem/, not a client story.
STORY_PAGES = [s for s in STORIES if not s.get('is_product')]


# ──────────────────────────────────────────────────────────────────────────
# Confirmed in scripts/facts.md
# ──────────────────────────────────────────────────────────────────────────
CONFIRMED = {
    'metric_wastemart': 'Six hours a week back, per depot',
    'metric_managem': 'Month-end close: nine days to two',
    'stat_systems': '50+',
    'stat_sectors': '5+',
    'managem_trial_live': True,
    'footer_linkedin': 'https://www.linkedin.com/company/gem-information-systems-pty-ltd/',
}

# ──────────────────────────────────────────────────────────────────────────
# What is still open, and what kind of open it is.
#
#   'blocking' — shipping it would be WRONG, not merely incomplete. The gate
#                fails on these.
#   'hideable' — shipping without it is fine. It disappears cleanly from the
#                live build, leaving a layout that still looks deliberate, and
#                is visible only under ?review=1. The gate warns on these.
# ──────────────────────────────────────────────────────────────────────────
TBC_KIND = {
    # ── blocking ─────────────────────────────────────────────────────────
    # Tore's Foundation is 2014, which places it after Trans Hex (2017) and
    # Sonke (2018) in the brief's running order.
    'timeline-order': 'blocking',
    # facts.md confirms the free trial is live but gives no URL, and the
    # separate ManaGEM site is still "FILL". A trial CTA with nowhere to go is
    # worse than no CTA.
    'managem-trial-url': 'blocking',

    # ── hideable ─────────────────────────────────────────────────────────
    # a person whose quotation is not yet in endorsements.md has no card live
    # (Keshan, Ryan and Philippine are confirmed there now, so only Nazier remains)
    'endorsement-nazier-line': 'hideable',
    'logo-wastemart': 'hideable',
    'logo-homeassist': 'hideable',
    'logo-sbs-waterproofing': 'hideable',
    'logo-trans-hex': 'hideable',
    'logo-sonke': 'hideable',
    'logo-tores-foundation': 'hideable',
    'then-now-screenshots': 'hideable',
    'team-photos': 'hideable',
    'entry-finos-status': 'hideable',
    'entry-smartstart-status': 'hideable',
    'entry-rentflow-status': 'hideable',
    'entry-nuracoach-status': 'hideable',
    'entry-lungelo-status': 'hideable',
    'managem-external-site': 'hideable',
    'eighth-video': 'hideable',
    'standalone-bundle': 'hideable',
    # facts.md gives no phone number: the one the old site carried is hidden
    # until it is confirmed
    # the partnership line stays on the hero at the owner's instruction, and is
    # flagged until facts.md confirms the current partner designation
    'microsoft-partner-badge': 'hideable',
}

BLOCKING = sorted(k for k, v in TBC_KIND.items() if v == 'blocking')
HIDEABLE = sorted(k for k, v in TBC_KIND.items() if v == 'hideable')
