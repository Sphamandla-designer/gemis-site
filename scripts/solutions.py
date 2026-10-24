"""
Content for the Solutions section: the directory at /solutions/ and the nine
service pages. Read by scripts/build-services.py.

Every claim here is traceable to one of four sources, recorded per claim in
docs/SOLUTIONS-EVIDENCE.md:

  * the original GEMIS service catalogue (the nine names, their one-line
    introductions and capability lists, carried since the first corporate
    build) — GEMIS's own description of what it offers;
  * the case-study records in scripts/stories.py and scripts/cases.py
    (what GEMIS did, the technology recorded, the status);
  * scripts/facts.md (dates, relationships, confirmed figures);
  * general, publicly verifiable facts (Azure has South African regions;
    Power BI has mobile apps).

Anything else is phrased as how GEMIS approaches the work, or as a question
settled per engagement — never as a guarantee. No prices, timelines,
service levels, certifications or measured results appear unless a source
above confirms them.

Service order and names follow scripts/services.py, which the navigation and
footer also read.
"""

# ── the directory ──────────────────────────────────────────────────────────

# one line each: what the discipline is, and when a visitor would choose it
DIRECTORY = {
    'custom-software': {
        'what': 'Business systems designed and built around how your organisation actually works.',
        'when': 'The work no longer fits off-the-shelf software, or is spread across several tools and spreadsheets.',
    },
    'microsoft-cloud': {
        'what': 'Azure environments designed, deployed and managed for the systems you depend on.',
        'when': 'A system runs on one office server, or you are planning a move to the cloud.',
    },
    'enterprise-saas': {
        'what': 'Platforms that serve many customer organisations from one product.',
        'when': 'You are building software to offer to many customers, not only to your own team.',
    },
    'mobile-apps': {
        'what': 'Mobile apps that bring work done in the field into your business system.',
        'when': 'The work happens on site, on the road or where the signal is unreliable.',
    },
    'business-intelligence': {
        'what': 'Reporting and Power BI dashboards drawn from the systems your figures come from.',
        'when': 'Reports are assembled by hand, or different reports disagree.',
    },
    'system-integration': {
        'what': 'Connections that let separate systems share information without retyping.',
        'when': 'Information is exported, emailed or retyped between systems.',
    },
    'ux-design': {
        'what': 'Research, workflow mapping, prototypes and interfaces for business software.',
        'when': 'People work around a system because it is slow or hard to use.',
    },
    'modernisation': {
        'what': 'Staged improvement of existing software and infrastructure.',
        'when': 'A system you depend on is ageing, but it cannot simply be switched off.',
    },
    'support': {
        'what': 'Monitoring, maintenance and improvement after go-live.',
        'when': 'A system needs looking after — including one someone else built.',
    },
}

# how the disciplines can combine — illustrative, not a fixed sequence
TOGETHER = [
    ('Understand', 'How the work is done today, where it breaks and what a change is worth.', ['ux-design']),
    ('Design', 'Workflows and interfaces shaped with the people who will use them.', ['ux-design']),
    ('Build', 'The system itself — for one organisation, for many, or for the field.', ['custom-software', 'enterprise-saas', 'mobile-apps']),
    ('Connect', 'Links to the systems already in place, and reporting drawn from them.', ['system-integration', 'business-intelligence']),
    ('Run', 'Hosting, identity, backup and recovery on Microsoft Azure.', ['microsoft-cloud']),
    ('Sustain', 'Maintenance, support and staged improvement as the business changes.', ['support', 'modernisation']),
]

# evidence on the directory: three projects that between them show the breadth
DIRECTORY_EVIDENCE = [
    {'slug': 'sbs-waterproofing', 'still': '03-deposit.jpg',
     'alt': 'Still from the SBS Waterproofing case study video: a quote accepted online, with the deposit invoice passed to accounting.',
     'why': 'A business system built around how SBS handles enquiries, quotes, deposits and stock — connected to accounting, looked after since 2015, and the origin of ManaGEM.',
     'shows': ['custom-software', 'system-integration', 'support']},
    {'slug': 'trans-hex', 'still': '02-sap-feed.jpg',
     'alt': 'Still from the Trans Hex Group case study video: the scheduled SAP financial import and its log.',
     'why': 'An existing information system stabilised first, then given an automated SAP feed and a management report that replaced weeks of manual compilation.',
     'shows': ['system-integration', 'business-intelligence', 'modernisation']},
    {'slug': 'sonke', 'still': '01-capture.jpg',
     'alt': 'Still from the Sonke Gender Justice case study video: a facilitator capturing a session on the offline mobile app.',
     'why': 'Sessions captured offline on a mobile app, checked and approved by role, and assembled into progress and donor reporting.',
     'shows': ['mobile-apps', 'ux-design', 'business-intelligence']},
]

# "where to start": problems mapped to the services that address them
PATHWAYS = [
    ('We need a system built around our processes.', ['custom-software', 'ux-design']),
    ('Our systems do not talk to each other.', ['system-integration', 'business-intelligence']),
    ('Our reporting takes too much manual effort.', ['business-intelligence', 'system-integration']),
    ('Our team works away from the office.', ['mobile-apps', 'custom-software']),
    ('Our current software needs to be improved.', ['modernisation', 'ux-design', 'microsoft-cloud']),
    ('We want to offer software to many organisations.', ['enterprise-saas']),
    ('We need ongoing technical support.', ['support', 'modernisation']),
]

# ── the nine service pages ─────────────────────────────────────────────────
# order: the sections a page shows, in sequence. Shared keys:
#   headline, copy, second (secondary link), problem, deliver, receive,
#   approach (+ approach_style), evidence, related, faq, cta
# Page-specific modules: compare, kinds, quote, timeline.

PAGES = {

    # ── 01 ─────────────────────────────────────────────────────────────────
    'custom-software': {
        'title': 'Custom software development — business systems built around your processes | GEMIS®',
        'desc': 'GEMIS designs and builds business systems around how your organisation works — mapped with your people, connected to the systems you run, and supported after go-live.',
        'headline': 'Systems designed around how your business actually runs.',
        'copy': 'When the work no longer fits off-the-shelf software, or lives across several tools and spreadsheets, GEMIS designs and builds a system around your processes, your people and the way the business is run.',
        'second': ('See systems we have built', '#evidence'),
        'visual': 'converge',
        'order': ['problem', 'deliver', 'approach', 'evidence', 'quote', 'related', 'faq'],
        'problem': {
            'heading': 'When the business has outgrown its tools',
            'statement': 'Most operations do not lack software. They have several tools that each hold part of the picture, a spreadsheet that holds the rest, and people who spend their day moving information between them.',
            'signs': [
                'The same customer or job is entered in more than one place.',
                'The real figures live in a spreadsheet someone maintains by hand.',
                'Staff work around the software rather than with it.',
                'Nobody can follow a job from first enquiry to final invoice in one place.',
            ],
        },
        'deliver': {
            'heading': 'One system for the work, captured once',
            'lede': 'The kinds of system GEMIS builds. Most projects combine several.',
            'items': [
                ('Internal management systems', 'The everyday work — enquiries, jobs, quotes, stock — in one system instead of several.'),
                ('Workflow automation', 'Routine steps such as reference numbers, invoices and alerts handled by the system, not by memory.'),
                ('Customer & supplier portals', 'Outside parties act on their part of the work — accepting a quote, paying, tracking an order — without phoning in.'),
                ('Operations platforms', 'Scheduling, dispatch and tracking for work spread across sites, vehicles and teams.'),
                ('Business portals', 'One web entry point where staff, partners or clients reach the information and tasks that concern them.'),
                ('Enterprise applications', 'Larger systems with role-based access, so each person sees and does what their role requires.'),
            ],
        },
        'approach_style': 'track',
        'approach': {
            'heading': 'How a custom system takes shape',
            'lede': 'The emphasis shifts from project to project; the order of thinking does not.',
            'steps': [
                ('Map the work', 'How the process is actually done today — on the floor, not on a whiteboard.'),
                ('Find the friction', 'Where information is retyped, delayed or lost, and what that costs.'),
                ('Design with users', 'Screens and workflows shaped and checked with the people who will use them.'),
                ('Build in stages', 'Working software demonstrated as it grows, so the direction can change early.'),
                ('Go live and stay', 'A careful rollout, then support and improvement from the team that built it.'),
            ],
        },
        'evidence': [
            {'slug': 'sbs-waterproofing', 'still': '01-enquiry.jpg',
             'alt': 'Still from the SBS Waterproofing case study video: a new enquiry captured in the system.',
             'why': 'When off-the-shelf apps stopped keeping up, GEMIS built SBS its own system in 2015 — enquiries, pipeline, online quote acceptance, deposits, profit per job and stock alerts. SBS still runs its business on it.'},
            {'slug': 'wastemart', 'still': '05-overview.jpg',
             'alt': 'Still from the WasteMart case study video: every order visible from quote to collection.',
             'why': 'One system from priced quote to confirmed collection, with customers paying through a secure link. WasteMart confirms it gives each depot six hours a week back.'},
            {'slug': 'homeassist', 'still': '02-dispatch.jpg',
             'alt': 'Still from the HomeAssist case study video: the nearest available plumber assigned to a job.',
             'why': 'Plumbing claims handled in one system: reported online or by insurers, assigned to the nearest available plumber, and tracked to sign-off.'},
        ],
        'quote': 'keshan-patel',
        'related': [
            ('ux-design', 'The system is designed with its users before it is built.'),
            ('system-integration', 'Most new systems need to exchange information with accounting, payments or an existing platform.'),
            ('microsoft-cloud', 'Where the system is hosted, who can reach it and how it is backed up.'),
            ('support', 'The system keeps changing with the business after go-live.'),
        ],
        'faq': [
            ('How does a custom software project start?',
             'With discovery: we learn how the work is done today, where it breaks and what a change is worth, before anything is designed or priced. What we find shapes the scope, and you decide whether to go further.'),
            ('What does a custom system cost?',
             'It depends on the scope, so we do not publish prices. A custom build usually costs more up front than a software licence; whether it pays back depends on how much work the current tools are causing. Discovery puts both sides of that into numbers for your business.'),
            ('Can it connect to the systems we already use?',
             'Usually, where those systems offer a way to connect. The system built for SBS Waterproofing passes deposit invoices to accounting, and HomeAssist’s links to insurers and manufacturers. Each connection is assessed during discovery rather than assumed.'),
            ('Who owns the system and the code?',
             'Ownership, licensing and handover are set out in the agreement for each project, so we agree them with you before the build starts.'),
            ('What happens after go-live?',
             'GEMIS can stay on to maintain and improve the system. SBS Waterproofing, HomeAssist and WasteMart have each worked with us for more than ten years.'),
        ],
        'cta': {
            'heading': 'Tell us how the work runs today.',
            'copy': 'Describe the process, the tools it depends on and where it breaks. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 02 ─────────────────────────────────────────────────────────────────
    'microsoft-cloud': {
        'title': 'Microsoft Cloud solutions — Azure environments designed and managed | GEMIS®',
        'desc': 'GEMIS designs, deploys and manages business systems on Microsoft Azure: hosting, Azure SQL, identity, integration, backup and recovery, planned around the business.',
        'headline': 'Infrastructure on Azure, designed around the business it runs.',
        'copy': 'GEMIS designs, deploys and manages business systems on Microsoft Azure — where applications and data live, who can reach them, how they are backed up and how they recover.',
        'second': ('See the questions to settle', '#faq'),
        'visual': 'layers',
        'order': ['problem', 'deliver', 'approach', 'evidence', 'related', 'faq'],
        'problem': {
            'heading': 'When the system depends on one machine',
            'statement': 'A system on a single office server depends on that server, its power supply, its backups and the person who looks after it. Azure changes those dependencies — but only when the environment is designed for the business rather than copied from a template.',
            'signs': [
                'The core system runs on one server in the office.',
                'Nobody is sure when a restore from backup was last tried.',
                'Staff cannot reach the system away from the office network.',
                'Access is granted and removed account by account, by hand.',
            ],
        },
        'deliver': {
            'heading': 'Each layer, planned for the system it carries',
            'lede': 'The parts of an Azure environment GEMIS designs and puts in place.',
            'items': [
                ('Microsoft Azure', 'An environment sized for the system’s workload, cost and growth.'),
                ('Azure SQL', 'Managed databases for the system’s data, with backup configured as part of the design.'),
                ('Cloud hosting', 'Applications hosted on Azure, reachable securely from where the work is done.'),
                ('Identity management', 'Sign-in and permissions managed centrally, so access follows each person’s role.'),
                ('API integration', 'Interfaces through which the system exchanges data with other platforms.'),
                ('Disaster recovery', 'A plan for restoring data and services after a failure, agreed as part of the design.'),
            ],
        },
        'approach_style': 'columns',
        'approach': {
            'heading': 'From the current setup to a managed environment',
            'lede': 'A migration and a new build follow the same thinking; a migration adds a way back at each step.',
            'steps': [
                ('Review', 'What runs where today, what it depends on, and what the business needs from it.'),
                ('Design', 'Hosting, data, identity, backup and recovery, each sized to the system.'),
                ('Deploy or migrate', 'In stages, with the existing setup kept available until the new one is proven.'),
                ('Operate', 'Monitoring, updates and cost reviews — by GEMIS or your own team, as agreed.'),
            ],
        },
        'evidence_note': 'The case studies record the platform each system is built on. They do not describe the hosting arrangements in detail, so none are claimed here.',
        'evidence': [
            {'slug': 'sbs-waterproofing', 'still': '06-system.jpg',
             'alt': 'Still from the SBS Waterproofing case study video: the modules of the business system.',
             'why': 'Recorded in the case study as built on Microsoft Azure, .NET and SQL, and in daily use since 2015.'},
            {'slug': 'homeassist', 'still': '06-overview.jpg',
             'alt': 'Still from the HomeAssist case study video: every job across the country in one view.',
             'why': 'Recorded as built on Microsoft Azure, .NET and SQL, with every job across the country visible in one place.'},
        ],
        'related': [
            ('modernisation', 'Moving an existing system to Azure is often the first stage of modernising it.'),
            ('support', 'Monitoring, updates and recovery tests continue after the move.'),
            ('system-integration', 'Systems on Azure still need to exchange data with the ones that are not.'),
            ('custom-software', 'New systems are designed for the environment they will run in.'),
        ],
        'faq': [
            ('Where will our data be hosted?',
             'Azure has regions in South Africa as well as abroad. The region is chosen with you for each system, taking into account where your users are, cost and your obligations under POPIA.'),
            ('Does moving to the cloud make our system secure and compliant?',
             'Not on its own. Azure provides strong building blocks, but security and POPIA compliance depend on how the environment is configured, how access is managed and how the system handles personal information. We design for those explicitly and are clear about where each responsibility sits.'),
            ('Who maintains the environment after it is set up?',
             'That is agreed per engagement. GEMIS can manage the environment as part of ongoing support, or hand it to your own IT team with the design written up.'),
            ('Can an existing system move without disrupting the business?',
             'Most migrations can be staged to keep disruption low — for example by running old and new side by side, with a way back at each step. How much disruption remains depends on the system, so it is assessed before the plan is agreed rather than promised in advance.'),
            ('What will it cost to run?',
             'Azure charges for what the environment uses, so the running cost depends on the system’s size and usage. The design includes an estimate, and the cost can be watched once the system is live.'),
            ('What happens during load-shedding?',
             'A system hosted in an Azure data centre does not depend on your office having power, so staff with charged devices and a connection can keep working. It does not remove the need for connectivity at your end.'),
        ],
        'cta': {
            'heading': 'Tell us what your systems run on today.',
            'copy': 'Where they are hosted, who looks after them and what worries you about that. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 03 ─────────────────────────────────────────────────────────────────
    'enterprise-saas': {
        'title': 'Enterprise SaaS platforms — multi-tenant software for many organisations | GEMIS®',
        'desc': 'GEMIS designs and develops multi-tenant platforms: one product serving many customer organisations, each with its own users, data and settings.',
        'headline': 'One platform, many organisations, each kept separate.',
        'copy': 'Enterprise SaaS is software built once and run for many customer organisations, each with its own users, data and settings. GEMIS designs and develops these platforms — a different discipline from building a system for one business.',
        'second': ('How it differs from a custom system', '#compare'),
        'visual': 'tenants',
        'order': ['problem', 'compare', 'deliver', 'approach', 'evidence', 'related', 'faq'],
        'problem': {
            'heading': 'When one system has to serve many customers',
            'statement': 'A system built for one business can assume one set of users, one way of working and one database. A product offered to many organisations cannot. Separation, configuration, onboarding and releases have to be designed in — or every new customer becomes another custom project.',
            'signs': [
                'Each new customer needs its own copy of the software.',
                'A change made for one customer risks breaking another.',
                'Onboarding takes development time rather than configuration.',
                'Nobody can see which features customers actually use.',
            ],
        },
        'compare': {
            'heading': 'A custom system and a platform are different projects',
            'cols': ('A system for one organisation', 'A platform for many'),
            'rows': [
                ('Users', 'One organisation’s staff and partners.', 'Many organisations, each with its own people and roles.'),
                ('Data', 'One business’s records.', 'Each customer’s records kept separate from every other’s.'),
                ('Change', 'Shaped around one way of working.', 'Released to every customer — so planned, and sometimes staged.'),
                ('A new customer', 'Not applicable.', 'Configured on the platform, rather than built from scratch.'),
            ],
        },
        'deliver': {
            'heading': 'What a platform needs from the start',
            'lede': 'The parts of a multi-tenant product GEMIS designs and develops.',
            'items': [
                ('Multi-tenant architecture', 'Customer organisations share one platform while their data and settings stay apart.'),
                ('Tenant configuration', 'Per-customer settings, so a new customer is set up rather than built for.'),
                ('Role-based access', 'Permissions per role within each customer, so people see what they should.'),
                ('Release management', 'Planned releases, so changes reach customers in a controlled way.'),
                ('Extensibility', 'Defined ways to add features and integrations without forking the product.'),
                ('Usage insight', 'A view of which features are used, to inform what the product does next.'),
            ],
        },
        'approach_style': 'columns',
        'approach': {
            'heading': 'From product idea to running platform',
            'lede': 'Platform work begins with the product and its customers, not with a single client’s process.',
            'steps': [
                ('Define the product', 'Who the customers are, what they share and where they differ.'),
                ('Design the architecture', 'Tenancy, identity, configuration and data separation.'),
                ('Build the core', 'The shared product, and the first customers’ configuration.'),
                ('Release and onboard', 'A release process and an onboarding path that do not need development.'),
                ('Maintain and evolve', 'Updates, support and a roadmap informed by how the product is used.'),
            ],
        },
        'evidence_note': 'ManaGEM is a GEMIS product you can use, not a service. Its internal architecture is not described here, so it is not offered as proof of every capability above.',
        'evidence': [
            {'slug': 'managem', 'still': '06-companies.jpg',
             'alt': 'Still from the ManaGEM video: the companies that run their operations on ManaGEM.',
             'why': 'GEMIS’s own business-management product, generalised from the system built for SBS Waterproofing and used by about a dozen companies — evidence of GEMIS developing and maintaining one product for many businesses.'},
        ],
        'related': [
            ('ux-design', 'A product used by many organisations has to work for people GEMIS will never meet.'),
            ('system-integration', 'Customers expect the platform to connect to the systems they already run.'),
            ('microsoft-cloud', 'Hosting, identity and recovery for a product many businesses depend on.'),
            ('support', 'A platform needs maintenance and releases for as long as customers use it.'),
        ],
        'aside': ('Looking for a ready-made system rather than a new platform?', 'See ManaGEM', 'products/managem/'),
        'faq': [
            ('What is the difference between a SaaS platform and a custom system?',
             'A custom system serves one organisation and is shaped around its way of working. A platform serves many organisations from one product, with each customer’s data, users and settings kept separate. Tenancy, configuration and releases have to be designed in from the start.'),
            ('How is one customer’s data kept separate from another’s?',
             'Through the architecture: separation is designed into the data model, access control and identity from the start. The right approach depends on the product and its customers, and is decided during design.'),
            ('Can new customers be onboarded without development?',
             'That is a design goal of a platform. Where a customer’s needs fall within the product’s configuration, onboarding is set-up rather than build; needs outside it become product decisions.'),
            ('How are new features released?',
             'Through a release process agreed with you, which can include releasing a change to some customers before others.'),
            ('Is ManaGEM an example of this?',
             'ManaGEM is GEMIS’s own business-management product, used by about a dozen companies. It shows our experience of developing one product for many businesses. If you want a ready-made system rather than a new platform, start with the ManaGEM page.'),
            ('Who owns a platform GEMIS develops?',
             'Ownership and licensing are set out in the agreement for that engagement, before development starts.'),
        ],
        'cta': {
            'heading': 'Planning software for many organisations?',
            'copy': 'Tell us who the customers are and what the product has to do for them. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 04 ─────────────────────────────────────────────────────────────────
    'mobile-apps': {
        'title': 'Mobile application development — field apps connected to your systems | GEMIS®',
        'desc': 'GEMIS builds mobile apps that extend business systems into the field: inspections, incident reports and data capture, with offline use where the work needs it.',
        'headline': 'Capture the work where it happens, online or offline.',
        'copy': 'GEMIS builds mobile applications that extend a business system to the people working away from a desk — on site, on the road or in the community — so what they capture reaches the rest of the business without being typed in again.',
        'second': ('See apps in the field', '#evidence'),
        'visual': 'field',
        'order': ['problem', 'evidence', 'deliver', 'approach', 'related', 'faq'],
        'problem': {
            'heading': 'When the work happens far from the system',
            'statement': 'Inspections, collections, sessions and site visits are often recorded on paper or in messages and typed in later. By then details are missing, the office is working from yesterday’s picture, and someone is re-entering what was already written down.',
            'signs': [
                'Field staff fill in forms that are captured again later.',
                'Photos and notes arrive by message and are filed by hand.',
                'The signal on site is unreliable, or absent.',
                'The office cannot see what was done until someone reports back.',
            ],
        },
        'deliver': {
            'heading': 'Field work, captured once',
            'lede': 'What GEMIS’s mobile apps are built to do.',
            'items': [
                ('Field operations', 'Jobs, routes and tasks on the phone of the person doing them.'),
                ('Inspections', 'Structured checklists and photo evidence captured at each step.'),
                ('Incident reporting', 'An incident recorded where it happens, with the details that matter.'),
                ('Data collection', 'Forms designed for the task, with validation before anything is sent.'),
                ('Offline functionality', 'Capture continues without a connection; records wait on the device.'),
                ('Synchronisation', 'Records reach the central system once a connection is available.'),
            ],
        },
        'approach_style': 'track',
        'approach': {
            'heading': 'Designed in the field, not at a desk',
            'lede': 'A field app succeeds or fails on conditions the office never sees.',
            'steps': [
                ('Follow the work', 'Where it happens, on what devices, with how much signal.'),
                ('Design for the task', 'The few things a person in the field must do, made quick.'),
                ('Plan for connectivity', 'What must work offline, and how records sync when signal returns.'),
                ('Connect to the system', 'The app as part of the business system, not beside it.'),
                ('Test where it is used', 'Checked in realistic conditions before the whole team relies on it.'),
            ],
        },
        'evidence': [
            {'slug': 'sonke', 'still': '01-capture.jpg',
             'alt': 'Still from the Sonke Gender Justice case study video: a session captured on the mobile app while offline.',
             'why': 'Facilitators capture each session on a mobile app that works offline and syncs when there is signal; M&E officers then check and approve every record.'},
            {'slug': 'homeassist', 'still': '04-evidence.jpg',
             'alt': 'Still from the HomeAssist case study video: a plumber photographing each step of a job in the app.',
             'why': 'Plumbers photograph each step of a job in the app, as proof that the work meets SANS standards.'},
            {'slug': 'wastemart', 'still': '04-collection.jpg',
             'alt': 'Still from the WasteMart case study video: a driver confirming a collection with a scan.',
             'why': 'Drivers confirm each collection on the mobile app with a scan, and the order updates for managers and customers.'},
        ],
        'related': [
            ('custom-software', 'The app is the field end of a business system.'),
            ('system-integration', 'Field records often need to reach accounting, scheduling or reporting.'),
            ('business-intelligence', 'Data captured in the field becomes reporting at head office.'),
            ('ux-design', 'Designing for one hand, bright sun and a hurry.'),
        ],
        'faq': [
            ('Can the app work without a connection?',
             'Yes, where the work needs it. Offline capture is designed in from the start: records are kept on the device and sent when a connection returns, as Sonke Gender Justice’s facilitators do. What can be done offline is decided per app, because some tasks need live information.'),
            ('Android, iOS or both?',
             'That depends on the devices your team uses and is decided during discovery. Many field teams use a mix, and the approach is chosen to suit it.'),
            ('How does data from the app reach the office?',
             'The app is connected to the central system, so a record captured in the field is available to the office once it has synced. There is no second system to retype into.'),
            ('How is information on the devices protected?',
             'Access is tied to each person’s sign-in. The specific protections — what is stored on the device, and how access is withdrawn from a lost phone — are designed for each app according to the information it holds.'),
            ('Who maintains the app after launch?',
             'Mobile apps need updates as phones and operating systems change. GEMIS can maintain the app as part of ongoing support.'),
        ],
        'cta': {
            'heading': 'Tell us where your work happens.',
            'copy': 'Who is in the field, what they record and what happens to it now. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 05 ─────────────────────────────────────────────────────────────────
    'business-intelligence': {
        'title': 'Business intelligence & reporting — Power BI and management reporting | GEMIS®',
        'desc': 'GEMIS builds reporting and Power BI dashboards drawn from the systems your figures come from, with agreed definitions and figures traceable to their source.',
        'headline': 'From scattered figures to reporting the business trusts.',
        'copy': 'GEMIS builds reporting that draws from the systems where the figures originate — including Power BI dashboards — so management sees consistent numbers without assembling them by hand.',
        'second': ('See the Trans Hex report', '#evidence'),
        'visual': 'provenance',
        'order': ['problem', 'approach', 'deliver', 'evidence', 'related', 'faq'],
        'problem': {
            'heading': 'When reporting is a manual job',
            'statement': 'When the figures a decision needs come from several systems, someone exports, copies and reconciles them before every meeting. The report arrives late, versions disagree, and the people preparing it are not doing the work they were hired for.',
            'signs': [
                'A monthly report takes days to compile.',
                'Two reports give different answers to the same question.',
                'Nobody can say where a particular figure came from.',
                'Managers keep their own spreadsheets rather than trust the official one.',
            ],
        },
        'approach_style': 'columns',
        'approach': {
            'heading': 'Questions first, data second',
            'lede': 'A dashboard is only as useful as the questions it was built to answer.',
            'steps': [
                ('Start with questions', 'Which decisions the reporting has to support, and for whom.'),
                ('Find the sources', 'Which systems hold each figure, and how they can be reached.'),
                ('Agree the definitions', 'What each measure means and who owns it, before it is drawn.'),
                ('Design for each audience', 'Executives, managers and teams each see what they act on.'),
                ('Keep it traceable', 'Every figure linked to its source, and the reporting maintained.'),
            ],
        },
        'deliver': {
            'heading': 'Reporting for each level of the business',
            'lede': 'The reporting GEMIS designs and builds, in Power BI or within the system itself.',
            'items': [
                ('Executive reporting', 'The few measures leadership steers by, on one page.'),
                ('Operational KPIs', 'Daily and weekly indicators for the teams doing the work.'),
                ('Sales analytics', 'Pipeline, conversion and revenue drawn from the sales records.'),
                ('Financial reporting', 'Budget against actual for the month and the year to date.'),
                ('Performance tracking', 'Progress against targets by site, region, programme or team.'),
                ('Monitoring', 'Figures refreshed on a schedule suited to each source, so the current position is visible.'),
            ],
        },
        'evidence_note': 'Neither case study records which reporting tool was used, so neither is presented as a Power BI project.',
        'evidence': [
            {'slug': 'trans-hex', 'still': '03-budget.jpg',
             'alt': 'Still from the Trans Hex Group case study video: the integrated management report, budget against actual.',
             'why': 'An integrated management report across plant, mining, finance, security and HR — budget against actual, filtered by mine and period, exported to Excel and PDF. A report that took weeks became available on demand; version two added forecasts and variances.'},
            {'slug': 'sonke', 'still': '02-approve.jpg',
             'alt': 'Still from the Sonke Gender Justice case study video: records checked and approved before they reach reporting.',
             'why': 'Progress against targets by country and programme, and donor reports that assemble from records already checked and approved — so every number traces to a real activity.'},
        ],
        'related': [
            ('system-integration', 'Reporting is only as good as the connections that feed it.'),
            ('custom-software', 'Often the missing data is work no system captures yet.'),
            ('microsoft-cloud', 'Where reporting data is held, and who can see it.'),
            ('modernisation', 'Reporting is frequently the first improvement to an existing system.'),
        ],
        'faq': [
            ('We already have reports. What would change?',
             'Usually the work behind them. When reports are compiled by hand, the effort repeats every cycle and the result is only as current as the last export. Reporting drawn from the source systems removes most of that preparation and gives everyone the same figures.'),
            ('Do all our systems need to be connected first?',
             'No. Power BI can draw from several sources at once. What does need settling first is what each figure means and which system is its source, so the same number means the same thing everywhere.'),
            ('Can we see dashboards on a phone?',
             'Yes. Power BI has mobile apps, and dashboards can be laid out for small screens where that is how they will be read.'),
            ('How current will the figures be?',
             'That depends on the sources and how often they can be refreshed — some several times a day, some daily or monthly. We agree the refresh schedule with you rather than promise real-time reporting.'),
            ('Can we trace a figure back to its source?',
             'That is a design requirement. Each figure is defined and linked to the system it is drawn from, which is what lets people trust the dashboard instead of keeping their own spreadsheets.'),
        ],
        'cta': {
            'heading': 'Which report takes too long to produce?',
            'copy': 'Tell us what it shows, who reads it and where the figures come from. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 06 ─────────────────────────────────────────────────────────────────
    'system-integration': {
        'title': 'System integration — connect accounting, ERP, CRM, payments and APIs | GEMIS®',
        'desc': 'GEMIS connects the systems a business already runs so information moves between them without retyping — mapped, monitored, documented and maintained.',
        'headline': 'Systems that share information, so nobody types it twice.',
        'copy': 'GEMIS connects the systems a business already runs — accounting, ERP and CRM platforms, payment providers, authentication services and third-party APIs — so information moves between them without retyping, exports or manual hand-offs.',
        'second': ('See integrations in use', '#evidence'),
        'visual': 'beforeafter',
        'order': ['problem', 'deliver', 'kinds', 'evidence', 'approach', 'related', 'faq'],
        'problem': {
            'heading': 'When information moves by hand',
            'statement': 'Each time the same information is entered into a second system, the business pays for it twice and creates a chance for the two to disagree. Over time the hand-offs become someone’s job, and the errors someone’s problem.',
            'signs': [
                'Invoices are retyped from one system into accounting.',
                'Exports are emailed and imported by hand.',
                'Payments are confirmed by checking a statement.',
                'Month-end reconciles figures that should already agree.',
            ],
        },
        'deliver': {
            'heading': 'An integration layer, not a tangle of exports',
            'lede': 'What GEMIS puts in place when it connects systems.',
            'items': [
                ('Mapping the flow', 'Every hand-off recorded: what moves, between which systems, when and why.'),
                ('One source per fact', 'Each piece of information given one authoritative system; the others read from it.'),
                ('Supported interfaces', 'Connections through each system’s own API or interface, not fragile copies.'),
                ('Failure handling', 'Scheduling, duplicate checks, logs and alerts, so a failed transfer is noticed.'),
                ('Monitoring and maintenance', 'Integrations watched and adjusted when a connected system changes.'),
                ('Documentation', 'A written account of what connects to what, for whoever maintains it next.'),
            ],
        },
        'kinds': {
            'heading': 'Kinds of system we connect',
            'items': ['Accounting systems', 'ERP platforms', 'CRM solutions', 'Payment gateways', 'Authentication services', 'Third-party APIs'],
            'note': 'Specific products are assessed case by case: what is possible depends on the interfaces each system provides.',
        },
        'approach_style': 'track',
        'approach': {
            'heading': 'How an integration is built',
            'lede': 'The business decisions come before the technical ones.',
            'steps': [
                ('Map', 'The information that moves between systems today, and how.'),
                ('Decide ownership', 'Which system is the source for each piece of information.'),
                ('Connect', 'Through supported interfaces, one flow at a time.'),
                ('Handle failure', 'Logging, duplicate checks and alerts designed in.'),
                ('Monitor', 'Watched in use, and maintained as the connected systems change.'),
            ],
        },
        'evidence': [
            {'slug': 'trans-hex', 'still': '02-sap-feed.jpg',
             'alt': 'Still from the Trans Hex Group case study video: the scheduled SAP import and its log.',
             'why': 'The daily SAP financial import automated: scheduled, de-duplicated, logged, with an email to the team if anything fails.'},
            {'slug': 'sbs-waterproofing', 'still': '03-deposit.jpg',
             'alt': 'Still from the SBS Waterproofing case study video: a quote accepted online and the deposit invoice passed to accounting.',
             'why': 'Quotes accepted online, with the deposit invoice following automatically into the accounting system.'},
            {'slug': 'homeassist', 'still': '05-insurers.jpg',
             'alt': 'Still from the HomeAssist case study video: links to insurers and manufacturers checking warranties and updating claims.',
             'why': 'Direct links to insurers and manufacturers check warranties and update claims automatically.'},
        ],
        'related': [
            ('business-intelligence', 'Connected systems are what make trustworthy reporting possible.'),
            ('modernisation', 'Integration is often how an older system is kept useful.'),
            ('custom-software', 'Sometimes the missing piece is a system to connect to.'),
            ('support', 'Integrations need watching as the systems around them change.'),
        ],
        'faq': [
            ('Which systems can you connect?',
             'Most systems that offer a supported way in, such as an API, a database interface or a scheduled file exchange. Our case studies include an SAP financial feed, accounting, and links to insurers and manufacturers. Each system is assessed before we commit, because what is possible depends on the interfaces it provides.'),
            ('What happens if an integration fails?',
             'It is designed to be noticed. For Trans Hex, the SAP import runs on a schedule, skips duplicates, logs every run and emails the team if anything fails. Comparable checks are designed into each integration.'),
            ('Which system should own the data?',
             'That is the first question we answer. Each piece of information gets one owner and the others read from it. It is a business decision as much as a technical one, and it is made before anything is connected.'),
            ('What happens when a connected system is updated?',
             'A change on either side can affect an integration, which is why integrations are monitored and maintained rather than left alone. Under an ongoing support arrangement, updates are checked and the connection adjusted as needed.'),
            ('Can you connect a system that has no API?',
             'Sometimes — through a database connection or a scheduled file exchange, for example — though these are less robust, and some systems cannot be connected safely. We say which applies after reviewing the system.'),
        ],
        'cta': {
            'heading': 'Where does your team retype information?',
            'copy': 'Name the systems and the hand-offs between them. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 07 ─────────────────────────────────────────────────────────────────
    'ux-design': {
        'title': 'UX & system design — business software designed around its users | GEMIS®',
        'desc': 'GEMIS designs business software from the work outward: user research, process mapping, prototypes, design systems and accessible interfaces, built by the same company.',
        'headline': 'Software designed around the people who use it every day.',
        'copy': 'Enterprise software should be clear and efficient for the people who spend their working day in it. GEMIS designs business systems from the work outward — research, process mapping, prototypes and interfaces — inside the company that builds them.',
        'second': ('See how design develops', '#approach'),
        'visual': 'frames',
        'order': ['problem', 'approach', 'deliver', 'evidence', 'related', 'faq'],
        'problem': {
            'heading': 'When the interface gets in the way of the work',
            'statement': 'A system that is hard to use gets worked around. Staff keep notes elsewhere, skip fields or phone someone instead — and the system ends up holding incomplete information. In business software, usability is an operational concern, not decoration.',
            'signs': [
                'New staff need long training before they can use the system.',
                'People keep side spreadsheets to do what the system should.',
                'Every screen shows everything to everyone, whatever their role.',
                'Simple tasks take many steps or screens.',
            ],
        },
        'approach_style': 'frames',
        'approach': {
            'heading': 'From the work to the interface',
            'lede': 'Each stage adds detail only once the one before has been checked with users.',
            'steps': [
                ('Observe', 'How people actually do the work, and what they need at each step.'),
                ('Map', 'Workflows and information requirements, by role.'),
                ('Prototype', 'Interactive drafts put in front of users early.'),
                ('Interface', 'Consistent screens and patterns, carried through to the build.'),
            ],
        },
        'deliver': {
            'heading': 'What design work produces',
            'lede': 'The design capabilities GEMIS brings to a business system.',
            'items': [
                ('User research', 'Understanding the people who use the system and the work they do.'),
                ('Business process mapping', 'Workflows and hand-offs drawn out before screens are designed.'),
                ('Interactive prototypes', 'Clickable drafts that users can try before anything is built.'),
                ('Design systems', 'Reusable interface patterns, so every new screen is consistent with the last.'),
                ('Enterprise dashboards', 'Overviews arranged around the decisions each role makes.'),
                ('Accessibility', 'Contrast, keyboard use, clear labels and readable layouts considered from the start.'),
            ],
        },
        'evidence_note': 'These case studies record design decisions. They do not include usability-testing records, so no measured results are claimed.',
        'evidence': [
            {'slug': 'sonke', 'still': '03-roles.jpg',
             'alt': 'Still from the Sonke Gender Justice case study video: different views for facilitators, country teams and leadership.',
             'why': 'Each role sees the view it needs — facilitators their sessions, country teams their country, leadership the whole picture.'},
            {'slug': 'homeassist', 'still': '03-updates.jpg',
             'alt': 'Still from the HomeAssist case study video: a homeowner receiving job updates on their phone.',
             'why': 'Designed for three audiences at once: homeowners kept informed by SMS or WhatsApp, plumbers capturing evidence in the app, and HomeAssist seeing every job.'},
        ],
        'related': [
            ('custom-software', 'The designs are built by the same company.'),
            ('modernisation', 'Redesigning an interface is often the first stage of improving a system.'),
            ('mobile-apps', 'Field apps live or die on the design of a few quick tasks.'),
            ('enterprise-saas', 'A platform has to work for people GEMIS will never meet.'),
        ],
        'aside': ('Need design work on its own — a teardown or an interface refresh?', 'Visit GEMIS Studio', 'studio/'),
        'faq': [
            ('Why does design matter for internal software?',
             'A system that is hard to use gets worked around, and a system that is worked around holds incomplete information. Good design decides whether the people who use the software every day put the right thing in the right place.'),
            ('Will our staff be involved?',
             'Yes. Design starts with the people who do the work: we observe how tasks are done and put prototypes in front of users early, so the design is checked against real work rather than a demonstration.'),
            ('Can you redesign a system we already have?',
             'Yes. Redesigning the interface of an existing system is one way to improve it without replacing it. We review how it is used first, so changes target the tasks that cause the most friction.'),
            ('How does design work with development?',
             'Design and development sit in the same company, so designers and developers work from the same requirements and the design is carried through to the built system.'),
            ('How is this different from GEMIS Studio?',
             'UX and system design is part of how GEMIS designs and builds business systems. GEMIS Studio is our product and interface design practice, with its own fixed-scope services. If you need design work on its own, start with the Studio.'),
        ],
        'cta': {
            'heading': 'Is your team working around its software?',
            'copy': 'Tell us which system it is and where people get stuck. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 08 ─────────────────────────────────────────────────────────────────
    'modernisation': {
        'title': 'Software modernisation — improve existing systems in planned stages | GEMIS®',
        'desc': 'GEMIS modernises existing software and infrastructure — cloud migration, interface redesign, performance, new features and data migration — in stages planned to keep disruption low.',
        'headline': 'Improve the system you depend on, one stage at a time.',
        'copy': 'GEMIS modernises existing software and infrastructure — moving it to the cloud, redesigning interfaces, improving performance, adding features and migrating data — in stages planned to keep disruption to daily operations low.',
        'second': ('Replace or improve?', '#compare'),
        'visual': 'stages',
        'order': ['problem', 'compare', 'approach', 'deliver', 'evidence', 'related', 'faq'],
        'problem': {
            'heading': 'When the system cannot be switched off',
            'statement': 'The system a business has outgrown is often the one it relies on most. Replacing it in one go is risky: data has to move, people have to relearn their work, and everything has to function on the first day. Improving it in stages lets the business keep working while the risk comes down.',
            'signs': [
                'The system is slow, dated or hard to change.',
                'It runs on infrastructure near the end of its life.',
                'Workarounds have grown up around its gaps.',
                'Replacing it outright feels too risky to begin.',
            ],
        },
        'compare': {
            'heading': 'Replacing everything is not the only option',
            'cols': ('Replace in one go', 'Improve in stages'),
            'rows': [
                ('Risk', 'Concentrated on one switch-over.', 'Spread across smaller, reversible steps.'),
                ('What is kept', 'Little of the old system.', 'What works well stays; what causes friction changes.'),
                ('Users', 'Relearn everything at once.', 'Adjust to one change at a time.'),
                ('When it fits', 'The old system cannot be salvaged.', 'The system is sound underneath but holding the business back.'),
            ],
        },
        'approach_style': 'columns',
        'approach': {
            'heading': 'A modernisation is a sequence of decisions',
            'lede': 'Each stage is planned, checked and settled before the next begins.',
            'steps': [
                ('Review', 'What the system does, how it is used and what it runs on.'),
                ('Separate', 'What works well from what people have learned to work around.'),
                ('Assess risk', 'Technical and operational risks of each change.'),
                ('Prioritise', 'Stages ordered by what costs the business most today.'),
                ('Migrate and validate', 'Data and infrastructure moved, then checked against the old system.'),
                ('Transition', 'Users moved across carefully, with support continuing afterwards.'),
            ],
        },
        'deliver': {
            'heading': 'Kinds of improvement',
            'lede': 'Most modernisations combine several, in an order agreed with you.',
            'items': [
                ('Cloud migration', 'Moving the system and its data to Microsoft Azure.'),
                ('Interface redesign', 'Making a dated interface clearer without changing what works underneath.'),
                ('Performance improvements', 'Finding and fixing what makes the system slow.'),
                ('Feature expansion', 'Adding what the business now needs to a system it already knows.'),
                ('Data migration', 'Moving records once, cleaning them as they go, and checking them afterwards.'),
                ('Staged rollouts', 'Changes introduced in planned stages, with a way back where possible.'),
            ],
        },
        'evidence': [
            {'slug': 'trans-hex', 'still': '01-stabilise.jpg',
             'alt': 'Still from the Trans Hex Group case study video: the existing information system stabilised first.',
             'why': 'GEMIS first stabilised the company’s own information system, then automated its SAP feed and built reporting into it. A second version extended it with weekly figures, forecasts and variances.'},
            {'slug': 'sbs-waterproofing', 'still': '04-profit.jpg',
             'alt': 'Still from the SBS Waterproofing case study video: profit shown for each project.',
             'why': 'The business system built in 2015 has been extended over more than a decade as SBS grew, and was later generalised into the ManaGEM product.'},
        ],
        'related': [
            ('microsoft-cloud', 'Moving to Azure is often one stage of a modernisation.'),
            ('ux-design', 'A clearer interface can transform an old system without replacing it.'),
            ('system-integration', 'Connecting an older system extends its useful life.'),
            ('support', 'The modernised system still needs looking after.'),
        ],
        'faq': [
            ('Do we need to replace the whole system?',
             'Not necessarily. Often the parts that work can stay while the parts that cause friction are improved or replaced in stages. Sometimes replacement is the better choice; the review is where that is decided.'),
            ('Will there be downtime?',
             'We plan stages to keep disruption low — for example by running old and new side by side and scheduling switch-overs at quiet times — but some changes need a short interruption. Any expected downtime is identified and agreed with you before it happens.'),
            ('What happens to our existing data?',
             'It is mapped, migrated, and checked against the existing system before anyone depends on it. Older records may be archived rather than moved; that is decided with you.'),
            ('How do you decide what to improve first?',
             'By weighing the friction each part causes against the risk and effort of changing it. The usual starting point is whatever costs the business most today.'),
            ('Can you modernise a system we did not build?',
             'Often, after reviewing the code, the infrastructure and any documentation. The review tells us whether improving it makes sense or whether another route is better.'),
        ],
        'cta': {
            'heading': 'Tell us about the system you depend on.',
            'copy': 'What it does, what it runs on and what holds you back. We come back within two working days with a short written view and a time to talk.',
        },
    },

    # ── 09 ─────────────────────────────────────────────────────────────────
    'support': {
        'title': 'Ongoing support & maintenance — monitoring, updates and improvement | GEMIS®',
        'desc': 'GEMIS monitors, maintains and improves the systems businesses depend on after go-live — with people who know the system. Some clients have worked with us for more than ten years.',
        'headline': 'We stay with the system long after go-live.',
        'copy': 'Software needs care after launch. GEMIS monitors, maintains and improves the systems businesses run on — with people who know the system, its history and how it is used.',
        'second': ('See how long clients stay', '#timeline'),
        'visual': 'loop',
        'order': ['problem', 'timeline', 'deliver', 'approach', 'evidence', 'related', 'faq'],
        'problem': {
            'heading': 'When nobody is looking after the system',
            'statement': 'Go-live is the start of a system’s life. The business changes, the platforms beneath it are updated, staff come and go. A system nobody looks after slowly drifts away from the business it was built for — until something breaks.',
            'signs': [
                'Updates and security patches are applied irregularly, or not at all.',
                'The people who built the system are no longer available.',
                'Small changes wait months because nobody owns them.',
                'New staff learn the system from whoever has time.',
            ],
        },
        'timeline': {
            'heading': 'Relationships measured in years',
            'lede': 'Three of the businesses GEMIS still works with, and when each relationship began.',
            'rows': [
                ('wastemart', 'WasteMart', 2013, 'Client since 2013'),
                ('sbs-waterproofing', 'SBS Waterproofing', 2014, 'Client since 2014 · system since 2015'),
                ('homeassist', 'HomeAssist', 2014, 'Client since 2014'),
            ],
            'start': 2013,
        },
        'deliver': {
            'heading': 'What support covers',
            'lede': 'Agreed per system, from the elements below.',
            'items': [
                ('Performance monitoring', 'Watching how the system behaves, so problems are found early.'),
                ('System maintenance', 'Keeping the system, its data and its environment in good order.'),
                ('Security updates', 'Applying platform and dependency updates as they are released.'),
                ('Feature enhancements', 'Planned improvements as the business changes.'),
                ('User training', 'Helping new staff, and existing ones with new features.'),
                ('Technical support', 'Troubleshooting from people who already know the system.'),
            ],
        },
        'approach_style': 'loop',
        'approach': {
            'heading': 'A cycle, not a ticket queue',
            'lede': 'Support follows the life of the system rather than a single request.',
            'steps': [
                ('Understand', 'The system, its environment and how the business uses it.'),
                ('Agree', 'What the arrangement covers, sized to the system.'),
                ('Maintain', 'Monitoring, updates and fixes, as a matter of routine.'),
                ('Improve', 'Changes scoped and rolled out as the business evolves.'),
            ],
        },
        'evidence': [
            {'slug': 'sbs-waterproofing', 'still': '02-pipeline.jpg',
             'alt': 'Still from the SBS Waterproofing case study video: every call, email and appointment tracked to the sale.',
             'why': 'GEMIS designed, built and still supports the system SBS has run its business on since 2015.'},
            {'slug': 'homeassist', 'still': '01-intake.jpg',
             'alt': 'Still from the HomeAssist case study video: jobs arriving from homeowners and insurers in one system.',
             'why': 'GEMIS and HomeAssist have worked side by side for more than ten years, and the system remains in use.'},
            {'slug': 'wastemart', 'still': '03-schedule.jpg',
             'alt': 'Still from the WasteMart case study video: paid orders going straight onto the schedule.',
             'why': 'The system has grown with WasteMart for more than ten years.'},
        ],
        'related': [
            ('modernisation', 'Support is often where the case for a staged improvement first appears.'),
            ('microsoft-cloud', 'Monitoring, updates and recovery for the environment the system runs in.'),
            ('system-integration', 'Integrations need watching as connected systems change.'),
            ('custom-software', 'Every system GEMIS builds can be supported by the team that built it.'),
        ],
        'faq': [
            ('What does ongoing support cover?',
             'It is agreed per system and can include monitoring, maintenance, security and dependency updates, troubleshooting, user training and planned improvements.'),
            ('How is support arranged?',
             'As an ongoing arrangement sized to the system and what it needs. The scope, response expectations and cost are set out in the agreement, so we do not publish standard terms here.'),
            ('Can you support a system someone else built?',
             'Often, after a review of the code, the hosting environment and any documentation. The review shows what support is possible and what should be addressed first.'),
            ('How are changes and improvements handled?',
             'Each request is scoped, agreed, built and rolled out in a controlled way. Larger improvements are planned with you as the business changes.'),
            ('How long do clients stay?',
             'Several of our clients have worked with us for more than ten years: WasteMart since 2013, and SBS Waterproofing and HomeAssist since 2014.'),
        ],
        'cta': {
            'heading': 'Is a system you rely on being looked after?',
            'copy': 'Tell us what it is, who built it and what concerns you. We come back within two working days with a short written view and a time to talk.',
        },
    },
}
