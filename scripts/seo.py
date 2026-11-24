"""
The SEO source of truth for the corporate site.

Every indexable page's <title>, meta description, primary keyword, H1, share
image, breadcrumb trail and structured-data type lives here, keyed by its path
from the site root. `scripts/apply-seo.py` writes them into the built pages —
the last step of the full rebuild, after apply-chrome — so the metadata is in
the static HTML, never set by script in the browser.

Rules this file keeps (and `apply-seo.py --check` enforces):
- every title is unique and at most 60 characters; every description unique,
  ideally 120–160 characters;
- every claim is one the page's own content (scripts/cases.py, stories.py,
  solutions.py, services.py, scripts/facts.md) already makes — the SEO brief's
  wording was adjusted wherever the record says something narrower;
- no city, office, price, rating or certification the repository does not
  confirm. The only confirmed address is Cape Town (Edgemead); there is no
  Johannesburg or Gauteng presence on record, so neither is targeted.

H1s are in sentence case, as every heading on the site is written; the
stylesheet sets them in capitals.
"""

# ── the site ──────────────────────────────────────────────────────────────
# The canonical host. https://gemis.co.za is the company's domain but it serves
# a different site today, so canonicals point at the address that actually
# serves these pages. When the custom domain is pointed here (a CNAME file and
# DNS — see docs/SEO-IMPLEMENTATION.md), change this one line and rebuild.
CANON = 'https://sphamandla-designer.github.io/gemis-site/'

ORG = {
    'name': 'GEM Information Systems',
    'alternateName': 'GEMIS',
    'legalName': 'GEM Information Systems (Pty) Ltd',
    'foundingDate': '2014',                        # scripts/facts.md
    'email': 'info@gemis.co.za',
    'logo': 'assets/img/logos/gemis.png',
    'address': {'streetAddress': '9 Tapiola Way', 'addressLocality': 'Edgemead, Cape Town',
                'addressRegion': 'Western Cape', 'addressCountry': 'ZA'},
    # verified profiles only (scripts/facts.md, stories.py)
    'sameAs': ['https://www.linkedin.com/company/gem-information-systems-pty-ltd/',
               'https://www.gemis.co.za/'],
    'slogan': 'Systems built to last. Partners built to stay.',
}

# Google Search Console HTML-tag verification. Leave empty until the owner adds
# the property and Google issues the token; apply-seo.py then writes
# <meta name="google-site-verification"> on the homepage. Never invent one.
GSC_VERIFICATION = ''

CARD = 'assets/img/og/gemis-share.jpg'            # 1200×630, tools/render-og.mjs
CARD_ALT = 'GEMIS — Systems built to last. Partners built to stay. Business systems on the Microsoft Cloud since 2014.'
VIDEO = 'assets/video/case-studies/'

HOME = ('Home', '')
SOL = ('Solutions', 'solutions/')
WORK = ('Case Studies', 'work/')
PROD = ('Products', 'products/')
INS = ('Insights', 'insights/')

# ── the pages ─────────────────────────────────────────────────────────────
# kind: home · collection · service · case · product · article · about ·
#       contact · page (anything else) · notfound (noindex)
PAGES = {
    # ── main pages ────────────────────────────────────────────────────────
    'index.html': dict(
        kind='home', keyword='custom software development South Africa',
        title='Custom Software & Business Systems South Africa | GEMIS',
        description='GEMIS designs, develops and supports custom business software, enterprise systems and mobile apps in South Africa — a long-term technology partner since 2014.',
        h1='Custom business software built around how your business works.',
        # the brand line the old H1 carried stays in the hero, under the new one
        h1_sub='Systems built to last. Partners built to stay.'),
    'solutions/': dict(
        kind='collection', keyword='software development services South Africa',
        title='Software Development & IT Solutions South Africa | GEMIS',
        description='Explore GEMIS software development services in South Africa: custom software, Microsoft Azure, enterprise SaaS, mobile apps, system integration and UX design.',
        h1='Software development and digital solutions for growing businesses.',
        crumbs=[HOME, SOL]),
    'products/': dict(
        kind='collection', keyword='business software products',
        title='Business Software & Digital Products | GEMIS',
        description='Explore GEMIS products: ManaGEM business management software, UX/UI and product design from GEMIS Studio, and practical technical training.',
        h1='Business software, product design and technology training.',
        crumbs=[HOME, PROD]),
    'work/': dict(
        kind='collection', keyword='software development case studies South Africa',
        title='Software Development Case Studies South Africa | GEMIS',
        description='GEMIS software development case studies from South African construction, insurance, waste management, mining, non-profit and education organisations.',
        h1='Business systems built to solve real operational challenges.',
        crumbs=[HOME, WORK]),
    'our-story/': dict(
        kind='about', keyword='South African software development company',
        title='About GEMIS | South African Software Development Partner',
        description='GEM Information Systems is a Cape Town software development company that has built and supported business systems for South African organisations since 2014.',
        h1='Building business systems and long-term technology partnerships.',
        crumbs=[HOME, ('Our Story', 'our-story/')]),
    'contact.html': dict(
        kind='contact', keyword='custom software development South Africa contact',
        title='Contact GEMIS | Custom Software Development South Africa',
        description='Looking for custom software or business systems in South Africa? Contact GEMIS to discuss your project and book a discovery session.',
        h1="Let's discuss your business systems project.",
        crumbs=[HOME, ('Contact', 'contact.html')]),
    'insights/': dict(
        kind='collection', keyword='business systems insights',
        title='Business Systems & Technology Insights | GEMIS',
        description='Practical insights from GEMIS on business software, POPIA compliance, keeping operations running through load-shedding, and moving off spreadsheets.',
        h1='Insights on business systems, software and technology.',
        crumbs=[HOME, INS]),
    'industries.html': dict(
        kind='page', keyword='business systems by industry',
        title='Industries We Build Business Systems For | GEMIS',
        description='The sectors GEMIS has built business systems for, with the evidence: NGOs and non-profits, waste and field operations, and multi-company business and finance.',
        crumbs=[HOME, ('Industries', 'industries.html')]),
    'privacy.html': dict(
        kind='page', keyword='GEMIS privacy notice',
        title='Privacy Notice | GEM Information Systems (GEMIS)',
        description='How GEM Information Systems handles what you send through this site, which cookies it uses (none unless you accept analytics) and your rights under POPIA.',
        crumbs=[HOME, ('Privacy notice', 'privacy.html')]),
    'terms.html': dict(
        kind='page', keyword='GEMIS terms of use',
        title='Terms of Use | GEM Information Systems (GEMIS)',
        description='The terms for using the GEM Information Systems website: what its information means, who owns its content, links, liability and governing law.',
        crumbs=[HOME, ('Terms of use', 'terms.html')]),
    '404.html': dict(kind='notfound', title='Page not found | GEM Information Systems (GEMIS)',
                     description='The page you were looking for has moved or never shipped.'),

    # ── the nine disciplines (scripts/solutions.py holds each page's copy) ──
    'solutions/custom-software/': dict(
        kind='service', keyword='custom software development South Africa',
        title='Custom Software Development South Africa | GEMIS',
        description='GEMIS develops custom business software in South Africa: workflow automation, business management systems, customer portals and enterprise applications.',
        h1='Custom software development built around your business.'),
    'solutions/microsoft-cloud/': dict(
        kind='service', keyword='Microsoft Azure solutions South Africa',
        title='Microsoft Azure Cloud Solutions South Africa | GEMIS',
        description='GEMIS designs, deploys, migrates and supports secure Microsoft Azure environments for South African businesses, built around the systems they run.',
        h1='Microsoft Azure cloud solutions for modern businesses.'),
    'solutions/enterprise-saas/': dict(
        kind='service', keyword='enterprise SaaS development South Africa',
        title='Enterprise SaaS Development South Africa | GEMIS',
        description='GEMIS designs and develops enterprise SaaS platforms: one multi-tenant system serving many organisations, each with its own data, users and integrations.',
        h1='Enterprise SaaS platforms built for many organisations.'),
    'solutions/mobile-apps/': dict(
        kind='service', keyword='mobile app development South Africa',
        title='Mobile App Development South Africa | GEMIS',
        description='GEMIS develops mobile apps that connect field teams, customers and business operations, including apps that keep working offline in the field.',
        h1='Mobile applications that connect your business operations.'),
    'solutions/business-intelligence/': dict(
        kind='service', keyword='Power BI business intelligence',
        title='Business Intelligence & Power BI Solutions | GEMIS',
        description='Turn business data into reporting you can trust with GEMIS business intelligence: Power BI dashboards, automated reports and connected data.',
        h1='Business intelligence and reporting that drive better decisions.'),
    'solutions/system-integration/': dict(
        kind='service', keyword='system integration services South Africa',
        title='Business System Integration Services South Africa | GEMIS',
        description='Connect accounting, ERP, CRM, payments and APIs with GEMIS system integration. Stop typing the same information twice and keep data flowing between systems.',
        h1='Connect your business systems and eliminate manual data transfers.'),
    'solutions/ux-design/': dict(
        kind='service', keyword='UX/UI design for business software',
        title='UX/UI Design & Business System Design | GEMIS',
        description='GEMIS designs business software around its users through research, workflow mapping, prototyping and interface design for enterprise applications.',
        h1='UX and system design built around the people who use your software.'),
    'solutions/modernisation/': dict(
        kind='service', keyword='legacy software modernisation South Africa',
        title='Legacy Software Modernisation South Africa | GEMIS',
        description='Modernise ageing business software with GEMIS. Improve existing systems, infrastructure and workflows in planned stages, without stopping the business.',
        h1='Modernise your existing business software without disrupting operations.'),
    'solutions/support/': dict(
        kind='service', keyword='software support and maintenance South Africa',
        title='Software Support & Maintenance South Africa | GEMIS',
        description='Keep business software reliable with GEMIS support: monitoring, maintenance, updates, troubleshooting and continuous improvement long after go-live.',
        h1='Ongoing software support that keeps your business running.'),

    # ── case studies (scripts/cases.py holds each record) ───────────────────
    'work/sbs-waterproofing/': dict(
        kind='case', keyword='construction business management system', client='SBS Waterproofing',
        title='Custom Business Management System for Construction | GEMIS',
        description='How GEMIS built SBS Waterproofing a business management system connecting enquiries, quotes, deposits, project profitability and stock.',
        h1='How GEMIS built a business management system for SBS Waterproofing.',
        image=VIDEO + 'SBS_explainer_thumb.jpg'),
    'work/homeassist/': dict(
        kind='case', keyword='insurance claims management software', client='HomeAssist',
        title='Insurance Claims Management Software | GEMIS',
        description="How GEMIS built HomeAssist's national plumbing-claims system: claims reported, plumbers dispatched, job evidence captured and signed off, customers kept informed.",
        h1='Building a digital claims management system for HomeAssist.',
        image=VIDEO + 'HomeAssist_explainer_thumb.jpg'),
    'work/wastemart/': dict(
        kind='case', keyword='waste management software', client='WasteMart',
        title='Waste Management Software & Operations System | GEMIS',
        description='How GEMIS built WasteMart an operations platform connecting quotes, online payments, scheduling, a driver app and collection tracking.',
        h1='Connecting waste management operations from quote to collection.',
        image=VIDEO + 'WasteMart_explainer_thumb.jpg'),
    'work/trans-hex/': dict(
        kind='case', keyword='mining reporting SAP integration', client='Trans Hex Group',
        title='Mining Reporting & SAP Integration Solution | GEMIS',
        description="How GEMIS stabilised a diamond miner's information system, automated its SAP financial data feed and built an integrated management report.",
        h1='Modernising mining operations through system integration and reporting.',
        image=VIDEO + 'TransHex_explainer_thumb.jpg'),
    'work/sonke/': dict(
        kind='case', keyword='NGO monitoring and evaluation software', client='Sonke Gender Justice',
        title='NGO Monitoring & Evaluation Software | GEMIS',
        description='How GEMIS built Sonke Gender Justice a monitoring and evaluation system with offline mobile capture, approvals and donor reporting from verified data.',
        h1='Designing a mobile monitoring and evaluation system for Sonke Gender Justice.',
        image=VIDEO + 'Sonke_explainer_thumb.jpg'),
    'work/tores-foundation/': dict(
        kind='case', keyword='school debating management platform', client="Tore's Foundation",
        title='School Debating Management Platform | GEMIS',
        description="How GEMIS built Tore's Foundation one platform for its schools debating programme: competitions, live standings and coaches' claims across 24 schools.",
        h1='Building a digital debating management platform for 24 schools.',
        image=VIDEO + 'Tores_debating_platform_thumb.jpg'),

    # ── ManaGEM (the GEMIS overview; its own site is a separate destination) ─
    'products/managem/': dict(
        kind='product', keyword='business management software', product='ManaGEM',
        title='ManaGEM Business Management Software | GEMIS',
        description='Meet ManaGEM, a business management platform connecting enquiries, quotes, jobs, stock, invoicing and everyday operations in one system.',
        h1='ManaGEM: one connected system for managing your business.',
        image=VIDEO + 'ManaGEM_explainer_thumb.jpg',
        crumbs=[HOME, PROD, ('ManaGEM', 'products/managem/')]),

    # ── insights (scripts/services.py ARTICLES holds each article) ──────────
    'insights/popia-business-systems-checklist/': dict(
        kind='article', keyword='POPIA compliance business systems',
        title='POPIA Compliance for Business Systems: A Checklist | GEMIS',
        description='A practical POPIA checklist for business systems: where customer data lives, who can access it, and what happens when someone asks for it back.',
        h1='POPIA compliance: a practical checklist for your business systems.'),
    'insights/load-shedding-operations-resilience/': dict(
        kind='article', keyword='business IT resilience load-shedding',
        title='Business IT Resilience During Load-Shedding | GEMIS',
        description='How cloud hosting, offline-capable apps and backups keep business systems running through load-shedding, when a generator alone is not enough.',
        h1='How to keep business systems running during load-shedding.'),
    'insights/spreadsheets-to-a-system/': dict(
        kind='article', keyword='replace spreadsheets with business software',
        title='When to Replace Spreadsheets with Business Software | GEMIS',
        description='Is your business outgrowing its spreadsheets? When to move to dedicated business software, what the move involves and what it really costs.',
        h1='When should your business move from spreadsheets to software?'),
}

# breadcrumbs that follow from the path
for _p, _v in PAGES.items():
    if 'crumbs' in _v or _v['kind'] in ('home', 'notfound'):
        continue
    if _p.startswith('solutions/'):
        _v['crumbs'] = [HOME, SOL, (None, _p)]
    elif _p.startswith('work/'):
        _v['crumbs'] = [HOME, WORK, (_v['client'], _p)]
    elif _p.startswith('insights/'):
        _v['crumbs'] = [HOME, INS, (None, _p)]


def url(path):
    return CANON + ('' if path == 'index.html' else path)


def validate():
    """Unique titles and descriptions, sensible lengths. Returns a list of problems."""
    problems, seen_t, seen_d = [], {}, {}
    for p, v in PAGES.items():
        t, d = v['title'], v['description']
        if len(t) > 60:
            problems.append(f'{p}: title is {len(t)} characters (max 60)')
        if v['kind'] != 'notfound' and not 110 <= len(d) <= 170:
            problems.append(f'{p}: description is {len(d)} characters (aim 120–160)')
        if t in seen_t:
            problems.append(f'{p}: title duplicates {seen_t[t]}')
        if d in seen_d:
            problems.append(f'{p}: description duplicates {seen_d[d]}')
        seen_t[t], seen_d[d] = p, p
    return problems


if __name__ == '__main__':
    probs = validate()
    for p, v in PAGES.items():
        print(f"{len(v['title']):3} {len(v['description']):3}  {p:46} {v['title']}")
    print('\n'.join(probs) or 'seo.py: every title and description is unique and in range.')
