"""
Content for the services, products and insights.

One module, read by scripts/apply-chrome.py (the two navigation drop-downs),
scripts/build-services.py (the Solutions page, nine service pages, the
Products page and the Insights pages) and scripts/build-home.py (the
homepage sections). Change a service here and every place it appears follows.

The nine services and their capability lists are the ones the services
accordion carried since the first corporate build; the longer copy on each
service page was written for this site. Nothing names a client that is not
already in scripts/stories.py.
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

# (slug, name, one line, intro paragraph, capabilities, the longer page copy,
#  proof: a story slug that shows the service in production, or None)
SERVICES = [
    {
        'slug': 'custom-software',
        'faq': [
            ('How long does a custom system take to build?',
             'It depends on the size of the operation, but the shape is consistent: a short discovery, a design that is tested with your people, then a build in demonstrated sprints over months rather than weeks. You see working software early and steer it, so there is no long wait for a big reveal.'),
            ('What does it cost compared with off-the-shelf software?',
             'A custom build is a capital project plus a monthly running cost, so it costs more up front than a licence. It pays back where off-the-shelf software is being worked around — in retyping, reconciliation and the growth a template cannot take. A discovery session puts a number on both sides.'),
            ('Who owns the system and the code?',
             'You do. The system is built on your Microsoft Cloud environment, documented, and handed over with the people who built it still looking after it. Nothing is locked to us.'),
            ('Can it connect to the systems we already run?',
             'Yes. Most of what we build has to talk to an accounting package, a payment provider or an existing platform from day one, and integration is scoped at the start rather than added later.'),
        ],
        'name': 'Custom software development',
        'short': 'Systems designed around how your business actually runs.',
        'intro': 'When off-the-shelf software holds you back, we design and build solutions around '
                 'your exact processes, people and goals — software that fits your business, not '
                 'the other way around.',
        'caps': ['Enterprise applications', 'Business portals', 'Internal management systems',
                 'Workflow automation', 'Customer & supplier portals', 'Operations platforms'],
        'body': [
            ('Why it matters',
             'Most businesses do not have a software shortage. They have five systems that disagree '
             'with each other, a spreadsheet that holds the truth, and a person who knows which one '
             'to believe. A custom system replaces that arrangement with one place where the work '
             'is captured once and every report draws from it.'),
            ('How we work',
             'We start on your floor, not at a whiteboard: we map the process as it is actually '
             'done, find where it breaks, and design the system around the people who will use it '
             'every day. Builds run in short, demonstrated sprints, so you see the system grow and '
             'can change course before anything is expensive to change.'),
            ('What you get',
             'A system on the Microsoft Cloud that your team owns, documented and supported by the '
             'people who built it. Several of the systems we built in our first two years are still '
             'running today, and still ours to look after.'),
        ],
        'proof': 'wastemart',
    },
    {
        'slug': 'microsoft-cloud',
        'faq': [
            ('Is our data kept in South Africa?',
             'For most clients, yes. Azure has South African regions, and we design environments in-country unless a business has a reason to do otherwise, which also helps with POPIA obligations.'),
            ('Will we need our own IT team to run it?',
             'No. We architect the environment, deploy it, monitor it and keep it patched as part of ongoing support. You see the cost and the status; we do the running.'),
            ('What happens during load-shedding?',
             'A system on Azure does not notice that your office has lost power. It stays reachable from a phone or a laptop on a battery, which is one of the main reasons businesses move their core system to the cloud.'),
            ('Can you move an existing system to the cloud without downtime?',
             'We migrate in stages with a tested way back at each step, and run old and new side by side until the switch is a formality. The business does not have to stop to move.'),
        ],
        'name': 'Microsoft Cloud solutions',
        'short': 'Secure, scalable infrastructure on Azure, run for you.',
        'intro': 'We architect, deploy and manage solutions on the Microsoft Cloud — the same '
                 'platform trusted by enterprises worldwide for security, reliability and scale.',
        'caps': ['Microsoft Azure', 'Azure SQL', 'Cloud hosting', 'Identity management',
                 'API integration', 'Disaster recovery'],
        'body': [
            ('Why it matters',
             'A server in a cupboard is a single point of failure with a power cable. Moving the '
             'systems a business depends on to Azure takes the hardware, the backups and the '
             'patching off your plate, and puts the data in a South African region with the '
             'resilience to ride out the next outage.'),
            ('How we work',
             'We design the environment before anything is deployed: identity, network, data, '
             'backup and recovery, each sized to the business rather than to a template. Then we '
             'migrate in stages with a tested way back at every step, so the business never has '
             'to stop.'),
            ('What you get',
             'An environment you can see the cost of, with monitoring that tells us about a '
             'problem before you do, and a recovery plan that has actually been rehearsed.'),
        ],
        'proof': 'trans-hex',
    },
    {
        'slug': 'enterprise-saas',
        'faq': [
            ('What makes a platform different from a custom system?',
             'A platform serves many organisations from one shared core, with each customer’s configuration, data and permissions kept separate. Tenancy, billing and release management have to be designed in from the start; they cannot be bolted on later.'),
            ('Have you built one before?',
             'Yes. ManaGEM, our own business management platform, runs on exactly this foundation — a shared core with per-tenant configuration — and several of the systems in our case studies serve more than one organisation.'),
            ('How do you handle security and access across tenants?',
             'Role-based access that holds up to audit, data isolated per tenant, identity on the Microsoft Cloud, and a release process that lets a change reach one customer before all of them.'),
            ('Can the platform grow without growing our support team?',
             'That is the point of it. Onboarding a new customer is configuration rather than a build, and the reporting shows which features are earning their keep.'),
        ],
        'name': 'Enterprise SaaS platforms',
        'short': 'Multi-tenant platforms built to serve thousands of users.',
        'intro': 'Multi-tenant platforms engineered to serve thousands of users — built for '
                 'performance, security and growth from day one.',
        'caps': ['Property management', 'Business operations', 'Healthcare', 'Manufacturing',
                 'Logistics', 'Government & NGO'],
        'body': [
            ('Why it matters',
             'A platform that serves many organisations is a different kind of system from one '
             'that serves a single business. Tenancy, permissions, billing, performance under load '
             'and the ability to roll out a change to everyone at once all have to be designed in '
             'at the start — they cannot be bolted on later.'),
            ('How we work',
             'We build on an architecture we have shipped before: a shared core with per-tenant '
             'configuration, role-based access that holds up to audit, and a release process that '
             'lets a feature reach one customer, then all of them. ManaGEM, our own business '
             'management platform, runs on exactly this foundation.'),
            ('What you get',
             'A platform that grows with your customer base without growing your support team, '
             'and the data to see which features are earning their keep.'),
        ],
        'proof': 'homeassist',
    },
    {
        'slug': 'mobile-apps',
        'faq': [
            ('Does the app work without signal?',
             'Yes. Offline-first is built in from the start: work is captured on the device and syncs when there is a connection. In South Africa signal is a hope, not a plan, so we never assume it.'),
            ('Android, iOS or both?',
             'Both, from one codebase, so a field team on mixed devices runs the same app. We also design for one hand and a dirty screen, because that is how it is actually used.'),
            ('Is the app a separate system from the office one?',
             'No. The app is a window onto the same system, so a scan in the field is visible in the office the moment it lands, and nothing is retyped.'),
            ('What about the phones themselves?',
             'The app runs on ordinary Android and iOS devices, so there is no special hardware to buy, and a lost phone can be cut off from the system without losing data.'),
        ],
        'name': 'Mobile application development',
        'short': 'Capture work where it happens — online or offline, always in sync.',
        'intro': 'Mobile apps that extend your systems into the field — capturing work where it '
                 'happens, online or offline, always in sync.',
        'caps': ['Field operations', 'Inspections', 'Incident reporting', 'Data collection',
                 'Offline functionality', 'Real-time synchronisation'],
        'body': [
            ('Why it matters',
             'The work that matters most often happens furthest from a desk: on a site, in a '
             'truck, at a customer’s door. If it is written on paper and typed in later, it '
             'arrives late and wrong. A mobile app that works without signal, and syncs when it '
             'has one, closes that gap.'),
            ('How we work',
             'We design the app around the handful of things a person in the field actually has '
             'to do, and make each one fast with one hand and a dirty screen. Offline-first is '
             'built in from the start, because in South Africa signal is a hope, not a plan.'),
            ('What you get',
             'A native-feeling app for Android and iOS that is part of your system, not a '
             'separate one — so a scan in the field is visible in the office the moment it lands.'),
        ],
        'proof': 'wastemart',
    },
    {
        'slug': 'business-intelligence',
        'faq': [
            ('We already have reports. What would change?',
             'Reports that are compiled by hand are a week old by the time they are read. A dashboard draws live from the systems the numbers come from, so the question is answered when it is asked and the people compiling reports get their week back.'),
            ('Do we need all our data in one place first?',
             'No. Power BI connects to several sources at once. What does need to be agreed first is who owns each figure, so that a number means the same thing everywhere it appears.'),
            ('Can people see it on their phones?',
             'Yes. Dashboards are built to be read on a phone every morning, not only on a boardroom screen.'),
            ('Can you show where a number came from?',
             'Every figure traces back to the system it was drawn from. That is what makes the business trust the dashboard enough to stop keeping its own spreadsheet.'),
        ],
        'name': 'Business intelligence & reporting',
        'short': 'Power BI dashboards that turn scattered data into decisions.',
        'intro': 'Power BI dashboards that turn scattered data into clear, real-time '
                 'decision-making tools for every level of your organisation.',
        'caps': ['Executive reporting', 'Operational KPIs', 'Sales analytics', 'Financial reporting',
                 'Performance tracking', 'Real-time monitoring'],
        'body': [
            ('Why it matters',
             'A report that takes a week to compile is a week old by the time it is read. When '
             'the numbers a decision needs are assembled by hand from several systems, decisions '
             'wait, and the people assembling them are not doing the job they were hired for.'),
            ('How we work',
             'We begin with the questions, not the data: which five numbers would change what you '
             'do this week? Then we connect the sources, agree who owns each figure, and build '
             'dashboards that answer those questions at a glance, on a phone, every morning.'),
            ('What you get',
             'Live reporting that the business trusts because every number traces back to the '
             'system it came from — and the weeks-long report reduced to a click.'),
        ],
        'proof': 'trans-hex',
    },
    {
        'slug': 'system-integration',
        'faq': [
            ('Which systems can you connect?',
             'Accounting packages, ERP and CRM platforms, payment gateways, authentication services and most third-party APIs. Where a system has no interface, we build the bridge.'),
            ('Will integration break when one of the systems is updated?',
             'We connect through each system’s proper interface rather than through exports and imports, monitor the integration layer, and maintain it as part of ongoing support, so an update on one side is handled rather than discovered.'),
            ('Which system should own the data?',
             'That is the first question we answer. Each piece of information gets one owner, and the others read from it. It is a business decision as much as a technical one, and it is made before anything is connected.'),
            ('What does it save?',
             'Every retyping, and with it the errors, the delays and the arguments about which figure is right. Accounting, operations, payments and reporting end up agreeing without anyone reconciling them.'),
        ],
        'name': 'System integration',
        'short': 'Make your systems talk to each other. End double capture.',
        'intro': 'We make your systems talk to each other — eliminating double capture, '
                 'disconnected data and manual hand-offs between platforms.',
        'caps': ['Accounting systems', 'ERP platforms', 'CRM solutions', 'Third-party APIs',
                 'Payment gateways', 'Authentication services'],
        'body': [
            ('Why it matters',
             'Every time the same information is typed into a second system, the business pays '
             'twice and gets two versions of the truth. Integration removes the retyping, and with '
             'it the errors, the delays and the arguments about which figure is right.'),
            ('How we work',
             'We map every hand-off between your systems, decide which one owns each piece of '
             'data, and connect them through their proper interfaces rather than through '
             'exports and imports. Where a system has no interface, we build the bridge.'),
            ('What you get',
             'Accounting, operations, payments and reporting that agree with each other without '
             'anyone retyping anything, and an integration layer that is documented, monitored '
             'and ours to maintain.'),
        ],
        'proof': 'trans-hex',
    },
    {
        'slug': 'ux-design',
        'faq': [
            ('Why does design matter for internal software?',
             'A system that is hard to use gets worked around, and a system that is worked around holds bad data. Good design decides whether the people who live in the software every day put the right thing in the right place.'),
            ('Do you test designs with our staff?',
             'Yes. Prototypes go in front of the people who will use them early, so the design is checked against a real working day rather than a demo.'),
            ('Is the design team separate from the build team?',
             'GEMIS Studio is the design practice inside the company that builds, so what is designed is what ships, and a design decision never gets lost in a hand-off.'),
            ('Can you redesign a system we already have?',
             'Yes. Redesigning a dated interface is one of the most common ways we modernise a system without replacing it, and it usually cuts training and support calls straight away.'),
        ],
        'name': 'UX & system design',
        'short': 'Enterprise software people actually enjoy using.',
        'intro': 'Enterprise software doesn’t have to feel like enterprise software. We design '
                 'systems people actually enjoy using — clear, fast and considered.',
        'caps': ['User research', 'Business process mapping', 'Interactive prototypes',
                 'Design systems', 'Enterprise dashboards', 'Accessibility'],
        'body': [
            ('Why it matters',
             'A system that is hard to use gets worked around, and a system that is worked around '
             'holds bad data. Design is not decoration: it decides whether the people who have to '
             'live in the software every day will put the right thing in the right place.'),
            ('How we work',
             'We watch the work before we draw a screen. Prototypes go in front of the people who '
             'will use them early, so the design is tested against a real Tuesday afternoon, not '
             'a demo. GEMIS Studio is the design practice inside the company that builds, so what '
             'is designed is what ships.'),
            ('What you get',
             'Interfaces that need less training, fewer support calls and no manual — and a design '
             'system that keeps every future screen consistent with the first.'),
        ],
        'proof': 'sonke',
    },
    {
        'slug': 'modernisation',
        'faq': [
            ('Do we have to replace the whole system at once?',
             'No, and we recommend against it. We move a system in stages — the data first, then the parts that hurt most — with old and new running side by side until the switch is a formality.'),
            ('Will the business have to stop while you work?',
             'No. Zero-disruption rollouts are the standard: every stage has a tested way back, and the business keeps trading throughout.'),
            ('What happens to our existing data?',
             'It is migrated once, cleaned as it goes, and checked against the old system before the switch. Some history may stay in an archive where it belongs.'),
            ('How do you decide what to keep?',
             'We separate what the old system does well from what people have learned to work around. The first is kept; the second is where the modernisation earns its cost.'),
        ],
        'name': 'Software modernisation',
        'short': 'Move ageing systems forward without stopping the business.',
        'intro': 'We migrate ageing systems to the cloud, redesign dated interfaces, improve '
                 'performance and expand features — all without disrupting your daily operations.',
        'caps': ['Cloud migration', 'Interface redesign', 'Performance improvements',
                 'Feature expansion', 'Data migration', 'Zero-disruption rollouts'],
        'body': [
            ('Why it matters',
             'The system a business has outgrown is usually also the one it cannot switch off. '
             'Replacing it in one go is the riskiest project most companies will ever run. '
             'Modernising it in stages keeps the business running while the risk comes down.'),
            ('How we work',
             'We separate what the old system does well from what people have learned to work '
             'around, then move it piece by piece: the data first, then the parts that hurt most, '
             'with the old and new running side by side until the switch is a formality.'),
            ('What you get',
             'A system that is on the cloud, faster, easier to use and ready for the next ten '
             'years — without a single day the business could not trade.'),
        ],
        'proof': 'sbs-waterproofing',
    },
    {
        'slug': 'support',
        'faq': [
            ('What does ongoing support include?',
             'Monitoring, maintenance, security updates, training for new staff, technical support, and improvements as the business changes — on a monthly arrangement sized to the system rather than to a contract template.'),
            ('Who answers when we call?',
             'The people who built the system, who already know it. Our founding clients have been with us since 2013 and 2014, and we still look after the systems we built them.'),
            ('Can you support a system someone else built?',
             'Usually, after a review of the code, the environment and the documentation. Where it is on the Microsoft Cloud or can be moved there, support is straightforward.'),
            ('How do changes get made after go-live?',
             'The same way the system was built: a request, a short scope, a demonstrated change and a rollout that does not interrupt the business. Go-live is the start of the system’s life, not the end of the project.'),
        ],
        'name': 'Ongoing support & maintenance',
        'short': 'We stay after go-live. Some clients have been with us for over a decade.',
        'intro': 'Software needs care beyond go-live. We stay with you — monitoring, maintaining '
                 'and continuously improving the systems your business runs on.',
        'caps': ['Performance monitoring', 'System maintenance', 'Security updates',
                 'Feature enhancements', 'User training', 'Technical support'],
        'body': [
            ('Why it matters',
             'Go-live is the start of a system’s life, not the end of the project. The '
             'business changes, the regulations change, the platform underneath changes. A system '
             'nobody looks after drifts away from the business it was built for.'),
            ('How we work',
             'Every system we build comes with the people who built it. We monitor it, keep it '
             'patched and secure, train new staff on it, and improve it as the business grows — '
             'on a monthly arrangement sized to the system rather than to a contract template.'),
            ('What you get',
             'A partner who answers the phone and already knows your system. Our founding '
             'clients have been with us since 2013 and 2014, and we still look after the systems '
             'we built them.'),
        ],
        'proof': 'sbs-waterproofing',
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
