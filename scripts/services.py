"""
Content for the services, products and insights.

One module, read by scripts/apply-chrome.py (the two navigation drop-downs),
scripts/build-services.py (the Solutions page, nine service pages, the
Products page and the Insights pages) and scripts/build-home.py (the
homepage sections). Change a service here and every place it appears follows.

The nine services are the ones the services accordion carried since the
first corporate build. Their pages are built from scripts/solutions.py.
"""

# Small line icons, 24-unit viewBox, stroke only — the same family as the
# icons the homepage cards used.
ICONS = {
    'custom-software':
        '<rect x="3" y="4" width="18" height="14" rx="1.6"/><path d="M8 20h8M12 18v2M7 9l2.5 2.5L7 14M12 14h5"/>',
    'microsoft-cloud':
        '<path d="M7 18a4 4 0 0 1-.6-7.96A5.5 5.5 0 0 1 17 8.5a3.75 3.75 0 0 1 .5 7.5H7Z"/>',
    'enterprise-saas':
        '<rect x="3" y="3" width="8" height="8" rx="1.4"/><rect x="13" y="3" width="8" height="8" rx="1.4"/><rect x="3" y="13" width="8" height="8" rx="1.4"/><rect x="13" y="13" width="8" height="8" rx="1.4"/>',
    'mobile-apps':
        '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/><path d="M3 9.5v5M21 9.5v5"/>',
    'business-intelligence':
        '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'system-integration':
        '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><path d="M7 11l10-4.2M7 13l10 4.2"/>',
    'ux-design':
        '<path d="M4 20l4-1 10-10-3-3L5 16l-1 4Z"/><path d="M13 7l3 3M17 3l1 1"/>',
    'modernisation':
        '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v4h-4"/><path d="M12 8v4l3 2"/>',
    'support':
        '<path d="M4 13a8 8 0 0 1 16 0"/><rect x="3" y="13" width="4" height="6" rx="1.2"/><rect x="17" y="13" width="4" height="6" rx="1.2"/><path d="M19 19a3 3 0 0 1-3 3h-3"/>',
}

# slug, name and the one line the navigation drop-down shows. Everything else
# about a service — page copy, deliverables, evidence and FAQs — lives in
# scripts/solutions.py, with each claim sourced in docs/SOLUTIONS-EVIDENCE.md.
SERVICES = [
    {
        'slug': 'custom-software',
        'name': 'Custom software development',
        'short': 'Systems designed around how your business actually runs.',
    },
    {
        'slug': 'microsoft-cloud',
        'name': 'Microsoft Cloud solutions',
        'short': 'Azure environments designed, deployed and managed.',
    },
    {
        'slug': 'enterprise-saas',
        'name': 'Enterprise SaaS platforms',
        'short': 'Platforms that serve many organisations from one product.',
    },
    {
        'slug': 'mobile-apps',
        'name': 'Mobile application development',
        'short': 'Field work captured where it happens, online or offline.',
    },
    {
        'slug': 'business-intelligence',
        'name': 'Business intelligence & reporting',
        'short': 'Reporting and Power BI dashboards drawn from your systems.',
    },
    {
        'slug': 'system-integration',
        'name': 'System integration',
        'short': 'Make your systems talk to each other. End double capture.',
    },
    {
        'slug': 'ux-design',
        'name': 'UX & system design',
        'short': 'Business software designed around the people who use it.',
    },
    {
        'slug': 'modernisation',
        'name': 'Software modernisation',
        'short': 'Improve ageing systems in stages, with disruption kept low.',
    },
    {
        'slug': 'support',
        'name': 'Ongoing support & maintenance',
        'short': 'We stay after go-live. Some clients have been with us for over a decade.',
    },
]

BY_SLUG = {s['slug']: s for s in SERVICES}

# The three products. ManaGEM is built from scripts/stories.py; the other two
# are the Studio and the Academy.
PRODUCTS = [
    {
        # the live ManaGEM site; the overview at products/managem/ stays reachable
        # from the stories and the case study
        'slug': 'managem', 'name': 'ManaGEM', 'href': 'https://sphamandla-designer.github.io/ManaGEM/',
        'image': 'assets/img/menu/managem.jpg',
        'short': 'A proven business management platform, ready to run on.',
        'body': 'Enquiries followed to the sale, quotes accepted online, deposit invoices raised '
                'automatically, project profit, stock alerts and staff records in one place. It '
                'began as one client’s system, and about a dozen companies run their '
                'day-to-day operations on it today.',
        'cta': 'Explore ManaGEM',
    },
    {
        'slug': 'design-studio', 'name': 'Design Studio', 'href': 'studio/',
        'image': 'assets/img/menu/design-studio.jpg',
        'short': 'Product and interface design from the team that can also build it.',
        'body': 'GEMIS Studio takes on research, prototypes, interfaces and design systems — for '
                'our own systems and as a standalone service.',
        'cta': 'See the Studio',
    },
    {
        'slug': 'technical-academy', 'name': 'Technical Academy', 'href': 'https://gemis.tech/',
        'image': 'assets/img/menu/gemis-tech.jpg',
        'short': 'Practical AI and technical training for professionals and teams.',
        'body': 'Courses that keep the people who use the systems ahead of the systems — delivered '
                'at gemis.tech.',
        'cta': 'Visit gemis.tech',
    },
]

# ── News & Insights ──────────────────────────────────────────────────────
# Three articles on the subjects South African businesses search for when
# they are thinking about their systems. Written for this site.
ARTICLES = [
    {
        'slug': 'popia-business-systems-checklist',
        'chips': ['Compliance', 'Data protection', 'Access control', 'Microsoft Azure'],
        'tag': 'Compliance',
        'title': 'POPIA and your business systems: a practical checklist',
        'standfirst': 'Compliance is not a policy document. It is where your customer data lives, '
                      'who can see it, and what happens when someone asks for it back.',
        'date': '2026-10-21', 'read': '6 min read',
        'image': 'assets/img/bg/sky-deep.jpg',
        'sections': [
            ('Start with where the data actually is',
             ['The Protection of Personal Information Act applies to every business in South Africa '
              'that holds information about people — customers, staff, suppliers, applicants. Most '
              'businesses believe their personal information lives in one or two systems. When we '
              'map it, it is usually in six: the accounting package, the CRM, a shared spreadsheet, '
              'the payroll system, the WhatsApp group the drivers use, and an export someone emailed '
              'to themselves in 2022.',
              'The first practical step is a plain inventory. For each system: what personal '
              'information does it hold, why, who can see it, and how long is it kept? You cannot '
              'secure what you have not found, and you cannot answer a data-subject request about '
              'data you do not know you hold.']),
            ('Access control is the whole game',
             ['POPIA’s security safeguard condition comes down to one question an auditor will '
              'ask: who can see this, and why? A shared login, a spreadsheet on a shared drive, or an '
              'admin account everybody uses all fail that question in the same way.',
              'In a well-built system, access is by role, not by person, and every change to a '
              'customer record is logged with who made it and when. That is not an expensive '
              'feature; it is a design decision made at the start. Retrofitting it onto a system '
              'that was never built for it is where the cost comes from.']),
            ('The checklist',
             ['Keep this short and keep it honest:',
              '1. An inventory of every system that holds personal information, with an owner for each.\n'
              '2. A purpose for each category of data — if you cannot say why you hold it, delete it.\n'
              '3. Role-based access, with no shared logins, and an audit trail on customer records.\n'
              '4. A retention rule that the system enforces, not one a person has to remember.\n'
              '5. A tested way to find, export and delete one person’s data on request, within the Act’s timeframes.\n'
              '6. Backups that are encrypted and in a known location — a South African Azure region, for most of our clients.\n'
              '7. Operator agreements with every third party that processes data on your behalf.\n'
              '8. A named Information Officer, registered with the Regulator, who actually knows the answers to 1–7.']),
            ('Where systems help, and where they do not',
             ['A system cannot make a business compliant. It can make the compliant thing the easy '
              'thing: capture a customer once, with a purpose, under a role, with a retention date, '
              'and the inventory, the access control and the deletion rule all take care of '
              'themselves. That is the difference between compliance as a yearly panic and '
              'compliance as a property of how the business runs.',
              'If your customer data is spread across spreadsheets and exports, a consolidation '
              'project is usually the fastest route to both a better business and a defensible '
              'POPIA position — and the two pay for each other.']),
        ],
    },
    {
        'slug': 'load-shedding-operations-resilience',
        'chips': ['Resilience', 'Cloud', 'Offline-first', 'Field operations'],
        'tag': 'Resilience',
        'title': 'Keeping operations running through load-shedding: a systems view',
        'standfirst': 'Generators keep the lights on. They do not keep the business running if the '
                      'systems it depends on are sitting in a server room with no power.',
        'date': '2026-10-21', 'read': '5 min read',
        'image': 'assets/img/bg/sky-wide.jpg',
        'sections': [
            ('The server in the cupboard',
             ['When the power goes, three things happen to a business that runs its systems '
              'on-site: the server goes down, the internet connection goes down, and the staff '
              'who could work from their phones cannot, because the system they need is the '
              'server that is down.',
              'The usual answer is a bigger UPS or a generator for the server room. That keeps the '
              'server alive, but it does not restore the fibre, the router or the branch forty '
              'kilometres away that was also in stage four.']),
            ('Move the system, not the generator',
             ['A system running on Microsoft Azure does not notice that your office has lost power. '
              'It is in a data centre with redundant supply, and it is reachable from any phone with '
              'a signal. The question becomes how your people reach it — and a mobile data '
              'connection is a great deal cheaper to keep alive than a server room.',
              'For most of the businesses we work with, moving the core system to the cloud '
              'turned load-shedding from a stop-work event into an inconvenience. The office goes '
              'dark; the quotes, the orders and the schedule carry on from a laptop on a battery '
              'and a phone on LTE.']),
            ('Design for the field as well',
             ['The office is only half the problem. A driver, an inspector or a technician in the '
              'field is often somewhere with no signal regardless of the grid. A mobile app that '
              'has to be online to work stops the moment they walk into a basement.',
              'Offline-first design — capture on the device, sync when there is signal — covers '
              'both load-shedding and the ordinary realities of South African connectivity. It is '
              'a business decision made at the scoping stage, not a feature bolted on later, and it '
              'is the reason several of the field systems we built keep working on days the grid '
              'does not.']),
            ('A short resilience checklist',
             ['1. Is the system your staff need to do their jobs reachable from a phone, from anywhere?\n'
              '2. If the office loses power and internet for four hours, what can and cannot happen?\n'
              '3. Can field staff capture work without a connection, and does it sync itself afterwards?\n'
              '4. Are backups off-site, automatic and tested — not on a drive in the same cupboard?\n'
              '5. Who knows how to keep trading when the usual tools are unavailable, and have they practised it?']),
        ],
    },
    {
        'slug': 'spreadsheets-to-a-system',
        'chips': ['Strategy', 'Business systems', 'Cost', 'Migration'],
        'tag': 'Strategy',
        'title': 'From spreadsheets to a system: when to move, and what it really costs',
        'standfirst': 'The spreadsheet is not the problem. The problem is the moment it becomes the '
                      'only person in the business who knows what is going on.',
        'date': '2026-10-21', 'read': '7 min read',
        'image': 'assets/img/bg/sky-flip.jpg',
        'sections': [
            ('The signs you have outgrown it',
             ['Every business starts in a spreadsheet, and for a while that is exactly right. The '
              'signs that it has stopped being right are consistent across the companies we have '
              'worked with: two people cannot update it at the same time; nobody is sure which copy '
              'is current; a figure in the monthly report cannot be traced back to where it came '
              'from; one person’s leave stops the business; and the “master” has a '
              'tab called “old – do not use” that is still used.',
              'The real cost is not the spreadsheet. It is the hours a week spent reconciling it '
              'against the accounting system, the customer who was quoted twice at two prices, and '
              'the decisions that wait for the report.']),
            ('What a system changes',
             ['A system captures each piece of work once, at the point it happens, by the person '
              'who did it. Everyone else sees the same record. The report is not compiled; it is '
              'simply looked at. The rules the business lives by — a quote needs terms, a job needs '
              'a driver, an invoice needs a signed delivery note — are enforced by the system rather '
              'than remembered by the person.',
              'The businesses we work with describe the change the same way: not that the system '
              'does something new, but that the arguments stopped.']),
            ('What it really costs',
             ['Honest numbers are hard to give without a conversation, but the shape of the cost is '
              'consistent. A system designed around one business, built on the Microsoft Cloud and '
              'supported afterwards, is a project measured in months, not weeks, and in a capital '
              'figure plus a monthly running cost. Against that sits the time the business is '
              'currently spending on reconciliation, the errors it is absorbing, and the growth it '
              'cannot take on because the spreadsheet will not stretch.',
              'For a business that is already running on a platform like ManaGEM, the monthly '
              'figure is lower and the start is faster, because the system exists and is configured '
              'rather than built. The right answer depends on how unusual your operation is — and '
              'that is the first thing a discovery session establishes.']),
            ('How to move without breaking the business',
             ['1. Map the process as it is actually done, not as the procedure says. The spreadsheet is a good guide to what people really track.\n'
              '2. Decide what the system will own, and stop maintaining the spreadsheet for that once it is live.\n'
              '3. Migrate the data once, clean it as you go, and accept that some history stays in the archive.\n'
              '4. Run the old and new side by side for one cycle — one month-end, one billing run — then switch.\n'
              '5. Keep the people who built it. The system will need to change as the business does.']),
        ],
    },
]

ARTICLE_BY_SLUG = {a['slug']: a for a in ARTICLES}


# ── the ways of working and the delivery stages, for the horizontal timelines ──
WAYS = [
    ('Understand', 'We learn your business before proposing anything: how the work is actually done, where it breaks, and what a fix is worth.'),
    ('Design', 'We design the system around your people and your process, and test it with them before anything is built.'),
    ('Build', 'Short, demonstrated sprints on the Microsoft Cloud, so you see the system grow and steer it as it does.'),
    ('Evolve', 'Go-live is the start. We monitor, maintain and keep improving the system as the business changes.'),
]

STAGES = [
    ('Discovery', 'We immerse ourselves in your operations to understand the challenges and goals before proposing anything.'),
    ('Architecture', 'A secure, scalable Microsoft Cloud design that fits your business today — and where it is heading.'),
    ('UX & Design', 'Wireframes and prototypes make sure the system works the way your people actually do.'),
    ('Build', 'Iterative sprints with regular demonstrations keep you involved and the solution on target.'),
    ('Assurance', 'Structured testing, performance validation and user acceptance before anything reaches production.'),
    ('Support', 'Careful rollout, training and documentation — then ongoing monitoring and improvement.'),
]

NEXT_STEPS = [
    ('We read it properly', 'Your enquiry reaches a monitored GEMIS mailbox, not a personal address. Expect a reply from a person who has read it.'),
    ('A discovery conversation', 'We map how your organisation actually works — the goals, the friction and the constraints — before anyone proposes a system.'),
    ('A scoped way forward', 'You get an architecture, a plan and a cost you can act on. If we are not the right fit, we will say so.'),
]

MILESTONES = [
    ('Founded in Cape Town', 'GEM Information Systems opens its doors in 2014, building affordable tools for SMEs and non-profits.'),
    ('Into the Microsoft Cloud', 'Azure, Azure SQL and C# become the backbone — enterprise infrastructure for mission-critical work.'),
    ('Platforms at national scale', 'ERP, learning, waste, property and community systems serving organisations nationally and abroad.'),
    ('A long-term partner', 'Discovery through continuous improvement — we stay with the systems we ship.'),
]

APPROACH = [
    ('Understand the business', 'We start on your floor, not at a whiteboard: how the work is actually done, where it breaks, and what a fix is worth.'),
    ('Define the problem', 'One agreed statement of what the system has to do better, before anyone draws a screen or writes code.'),
    ('Design the solution', 'The system is designed around your people and process, and tested with them as prototypes before it is built.'),
    ('Validate and deliver', 'Demonstrated sprints, structured testing and a careful rollout — then we stay to keep improving it.'),
]
