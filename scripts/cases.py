"""
The individual case study pages, section by section.

Everything here is drawn from the case study videos (scripts/video-text.json),
scripts/stories.py and scripts/facts.md. Where the videos are silent — a
timeframe, a measured result, whether a system is still in daily use — the
section says so or is left out, rather than filled in. The only metric is the
one the client confirmed (WasteMart). "Status" is what the video actually
states: "live" only where the narration says the business still runs on it.

Keys, per story slug:
  value        the one-line value proposition under the headline
  status       the project status shown in the hero and the overview
  users        who uses the system
  role         GEMIS's role
  scope        what the engagement covered
  deliverables the documented deliverables, from the narration
  timeframe    only where the videos or facts give one; otherwise None
  challenge    paragraphs: business context, user needs, constraints, the problem
  approach     (principles, paragraphs): the chosen direction and why it fits
  outcomes     dict of delivered / verified / intended lists; verified may be empty
  related      two other slugs
  cta          the tailored enquiry line
"""

CASES = {
    'sbs-waterproofing': dict(
        value='One system for every enquiry, quote, deposit and job — built around how a waterproofing contractor actually sells and delivers work.',
        status='Live — in daily use since 2015',
        users='Sales and office staff, site teams and management at SBS Waterproofing; customers receive SMS references, quotes and invoices',
        role='Website and campaign partner from 2014; designer, builder and ongoing support partner of the business system from 2015',
        scope='Enquiry capture, sales pipeline, quoting, deposit invoicing linked to accounting, project profitability and stock',
        deliverables=[
            'Company website and Google campaign management (2014)',
            'Enquiry capture with an automatic SMS reference number to the customer',
            'Sales pipeline tracking every call, email and appointment to the sale',
            'Online quote acceptance with the deposit invoice raised automatically into accounting',
            'Profit shown per project and stock reorder reminders',
        ],
        timeframe='Website and campaigns from 2014; the business system from 2015, extended since',
        challenge=[
            'SBS Waterproofing keeps Cape Town’s roofs and walls dry. After GEMIS built its website and helped run its Google campaigns in 2014, enquiries started arriving faster than the business could keep track of them.',
            'The off-the-shelf apps SBS tried did not fit the way a waterproofing contractor works: an enquiry becomes a site visit, a quote, a deposit, a scheduled job and a final invoice, with stock consumed along the way. Each step lived in a different tool, so leads were lost between them and nobody could see which jobs made money.',
            'The business needed one place where every enquiry was captured, every step to the sale was tracked, and the paperwork that follows a sale happened on its own.',
        ],
        approach=(
            ['Capture once, at the moment it happens', 'Automate the hand-offs that leak time', 'Show the business whether each job pays'],
            [
                'Rather than adapt SBS to a generic package, GEMIS designed the system around SBS’s own pipeline. The enquiry is the root record: it is captured once, the customer gets an SMS reference straight away, and every call, email and appointment hangs off it until the job is won.',
                'The hand-offs that used to depend on someone remembering were automated. A quote goes out in a few clicks; when the customer accepts online, the deposit invoice follows automatically and lands in the accounting system without re-keying.',
                'Because the system holds the costs as well as the sale, every project shows whether it made money, and stock reorder reminders arrive before a job stalls. The design was general enough that the same system later became the basis of ManaGEM, GEMIS’s business management platform.',
            ],
        ),
        outcomes=dict(
            delivered=[
                'A single business system covering enquiry, pipeline, quoting, deposits, project profit and stock',
                'Automatic SMS references and online quote acceptance for customers',
                'A live link from accepted quotes into the accounting system',
            ],
            verified=[
                'More than ten years on, SBS still runs its business on the system GEMIS built',
                'SBS has grown many times over since the system went live (as stated in the case study)',
                'The system became the foundation of ManaGEM',
            ],
            intended=[
                'No enquiry lost between tools; every lead followed through to a decision',
                'Less office time spent on quotes, deposits and chasing paperwork',
                'Management decisions made on profit per job rather than on turnover alone',
            ],
        ),
        related=['wastemart', 'homeassist'],
        cta='Selling and delivering jobs from a spreadsheet and three apps? Let’s look at one system for the whole pipeline.',
    ),
    'homeassist': dict(
        value='A national plumbing-claims operation run from one system: report, dispatch, evidence and sign-off, with the customer informed at every step.',
        status='Live — in use for more than ten years',
        users='Homeowners and insurers logging claims; a national panel of plumbers in the field; HomeAssist’s operations team',
        role='Designer, builder and long-term support partner',
        scope='Claim intake, automatic dispatch, customer communication, field evidence capture, insurer and manufacturer integration, national dashboard',
        deliverables=[
            'Online claim reporting for homeowners and claim logging for insurers',
            'Automatic assignment of the next available plumber near the job, from a national panel',
            'SMS and WhatsApp updates to the customer at each step',
            'A plumber app that photographs each step of the work as evidence of SANS compliance',
            'Direct links to insurers and manufacturers that check warranties and update claims automatically',
            'One national dashboard from first report to sign-off',
        ],
        timeframe=None,
        challenge=[
            'A burst geyser is urgent for the homeowner, a claim for the insurer, and a dispatch problem for HomeAssist, which works with a national panel of plumbers.',
            'Each party needed something different: the homeowner wanted to report the problem in minutes and then know what was happening; the insurer needed the claim logged and the warranty position checked; the plumber needed to prove that each step of the repair met SANS standards; and HomeAssist needed to see every job in the country without phoning around.',
            'Handled by phone and email, those needs pulled in different directions: updates meant calls, evidence meant paperwork, and warranty checks meant waiting on manufacturers.',
        ],
        approach=(
            ['One job record, every party on it', 'Dispatch by proximity and availability, not by phone', 'Evidence captured where the work happens'],
            [
                'GEMIS built the system around a single job record that every party sees from their own side. Whether the homeowner reports online or the insurer logs the claim, the job lands in the same place.',
                'Dispatch was made automatic: the system finds the next available plumber near the job and assigns it, and the customer is kept informed by SMS or WhatsApp without anyone making a call.',
                'On site, the plumber’s app captures a photograph at each step, so SANS compliance is evidenced as the work is done rather than reconstructed afterwards. Behind the scenes, direct links to insurers and manufacturers check warranties and update claims, and HomeAssist watches the whole country from one dashboard.',
            ],
        ),
        outcomes=dict(
            delivered=[
                'Online reporting, automatic dispatch and customer messaging in one system',
                'A field app with photographic compliance evidence',
                'Automated insurer and manufacturer integration and a national dashboard',
            ],
            verified=[
                'GEMIS and HomeAssist have worked side by side for more than ten years, and the system remains in use',
            ],
            intended=[
                'Fewer phone calls for customers, plumbers and the office',
                'Faster repairs, because dispatch no longer waits on a person',
                'Compliance and warranty positions evidenced automatically',
            ],
        ),
        related=['wastemart', 'sonke'],
        cta='Running a field operation across the country by phone? Let’s talk about dispatch, evidence and customer updates in one system.',
    ),
    'wastemart': dict(
        value='A single call becomes a priced quote, a secure payment, a scheduled truck and a confirmed collection — without the manual work in between.',
        status='Live — the system has grown with WasteMart for more than ten years',
        users='WasteMart’s sales team, operations planners and drivers; customers quoting, paying and tracking orders',
        role='Designer, builder and long-term support partner',
        scope='Quoting with standard terms, online acceptance and payment, operations alerts and scheduling, driver mobile confirmation, order tracking',
        deliverables=[
            'Quotes priced automatically with standard terms and conditions attached',
            'Online acceptance and a secure payment link sent to the customer',
            'Operations alerted the moment payment lands, with the job placed on the schedule',
            'Truck and driver assignment, and a driver app that confirms collection with a scan',
            'Order tracking for managers and customers',
        ],
        timeframe=None,
        challenge=[
            'A business that needs its waste removed should be able to make one call. Behind that call at WasteMart sat a lot of manual work: building the quote, attaching the right terms, chasing payment, and then remembering to tell operations that a job was on.',
            'Sales, finance and operations each held part of the picture, so proof of payment was chased, jobs were scheduled late, and nobody — including the customer — could see where an order stood.',
            'The problem to solve was the chain of hand-offs between the call and the collection.',
        ],
        approach=(
            ['Remove every hand-off that depends on memory', 'Let payment drive the schedule', 'Give customers the same view as managers'],
            [
                'GEMIS designed the system so that each step triggers the next. The sales team picks the service and the quote is priced with standard terms attached automatically; the customer accepts it and receives a secure payment link straight away.',
                'The moment payment comes through, operations is alerted and the job goes onto the schedule. Planners assign the truck and driver, and the driver confirms the collection on the mobile app with a quick scan.',
                'Because the order record is shared, managers see every order from quote to collection in one place and the customer can track it too.',
            ],
        ),
        outcomes=dict(
            delivered=[
                'Automatic quoting, online acceptance and secure payment links',
                'Payment-driven scheduling with truck and driver assignment',
                'Driver scan confirmation and shared order tracking',
            ],
            verified=[
                'Six hours a week back, per depot (confirmed by the client)',
                'A system that has grown with WasteMart for more than ten years',
            ],
            intended=[
                'Less admin between sale and collection',
                'Faster payment, with no chasing for proof',
                'Every job on time and visible to the customer',
            ],
        ),
        related=['sbs-waterproofing', 'homeassist'],
        cta='Still chasing quotes, payments and schedules by hand? Let’s map the chain from call to collection.',
    ),
    'trans-hex': dict(
        value='One integrated management report for a diamond mine — plant, mining, finance, security and people — available on demand instead of weeks later.',
        status='Delivered 2017; a second version followed',
        users='Management at Trans Hex’s Baken mine and, from version two, other operations in the group',
        role='Stabilised the company’s in-house information system, automated the SAP data feed and built the reporting into it',
        scope='System stabilisation, scheduled SAP financial data integration, integrated management reporting with budget-against-actual, exports, forecasts and variances',
        deliverables=[
            'The company’s own management information system running reliably',
            'A daily SAP financial data import — scheduled, de-duplicated, logged, with failure emails to the team',
            'An integrated management report across plant, mining, finance, security and HR: gravel treated, carats, fleet availability and cost per carat, for the month and year to date',
            'Filters by mine, period and date range; export to Excel and PDF',
            'Version two: weekly figures, forecasts, variances, live exchange rates and mine groups',
        ],
        timeframe='2017, with version two following',
        challenge=[
            'Trans Hex has mined diamonds for more than fifty years. At its Baken mine on the Lower Orange River, management needed one clear view across plant, mining, finance, security and people.',
            'That view was pieced together in Excel from several sources, including SAP. It took weeks to assemble, errors crept in along the way, and by the time it was ready the month had moved on.',
            'The constraint was that the data already existed in systems the mine depended on; the problem was getting it into one reliable, repeatable report.',
        ],
        approach=(
            ['Make the foundation reliable before adding to it', 'Automate the feed, with failure made visible', 'Build the report into the system, not beside it'],
            [
                'GEMIS first got the company’s own information system running reliably, so that nothing new was built on an unstable base.',
                'The daily feed of financial data from SAP was then automated: it runs on schedule, skips duplicates, logs what it did, and emails the team if anything fails — so a missing day is noticed, not discovered at month-end.',
                'The management report was built into the system itself rather than assembled outside it, with budget against actual for the month and the year to date, filters by mine and period, and export to Excel and PDF. Version two extended the same structure with weekly figures, forecasts, variances, live exchange rates and mine groups, bringing other operations into the same view.',
            ],
        ),
        outcomes=dict(
            delivered=[
                'A stabilised in-house information system',
                'An automated, monitored SAP financial feed',
                'An integrated management report with filters, exports and a second version of extended measures',
            ],
            verified=[
                'A report that took weeks became available whenever it was needed (as stated in the case study)',
            ],
            intended=[
                'Fewer errors, because the data is loaded once and checked automatically',
                'Management decisions on current figures rather than last month’s',
                'One view across operations rather than one spreadsheet per source',
            ],
        ),
        related=['sonke', 'sbs-waterproofing'],
        cta='Compiling the management pack by hand from several systems? Let’s talk about an automated, integrated report.',
    ),
    'sonke': dict(
        value='A monitoring and evaluation system for work in forty countries — captured offline in the field, checked in the office, reported to donors from verified data.',
        status='Delivered 2018',
        users='Field facilitators, M&E officers, programme managers and leadership at Sonke Gender Justice; donors receive the reports',
        role='Designer and builder of the monitoring and evaluation system',
        scope='Offline-capable mobile capture, approval workflow, programme targets by country and programme, role-based views, donor reporting',
        deliverables=[
            'A mobile app on which facilitators capture each session, working offline and syncing when there is signal',
            'An approval workflow in which M&E officers check each record, so every number traces to a real activity',
            'Progress against targets by country and programme, as it happens',
            'Role-based views: country teams see their country, leadership the whole picture',
            'Donor reports assembled from already-verified data',
        ],
        timeframe='2018',
        challenge=[
            'Sonke Gender Justice works to end gender-based violence and reduce the spread of HIV in forty countries across Africa. Every day its teams run workshops, dialogues and outreach.',
            'Funders ask a hard question: what difference did it make? Answering it meant collecting evidence from sessions held far from any office, often without signal, and then proving that the numbers in a report corresponded to real activities.',
            'The problem was both capture and credibility: getting field data in reliably, and making it trustworthy enough to report.',
        ],
        approach=(
            ['Capture where the work happens, with or without signal', 'Verify before counting', 'Show each role only what it needs'],
            [
                'The system starts in the field: facilitators capture each session on a mobile app that works offline and syncs when there is signal, so a lack of connectivity never means a lost record.',
                'Nothing counts until it is checked. M&E officers review and approve what comes in, so every figure in a report can be traced back to a real activity — which is what makes the reporting credible to funders.',
                'Programme managers see progress against targets by country and programme as it happens, each role sees the view it needs, and donor reports come together from data that has already been verified.',
            ],
        ),
        outcomes=dict(
            delivered=[
                'An offline-first mobile capture app',
                'An approval workflow and traceable records',
                'Target tracking, role-based views and donor reporting',
            ],
            verified=[],
            intended=[
                'Less time on paperwork for field and office teams',
                'Donor reports built from verified data rather than reconstructed figures',
                'Programme decisions made on current progress against targets',
            ],
        ),
        related=['homeassist', 'tores-foundation'],
        cta='Reporting to funders from field data you cannot fully verify? Let’s talk about capture, approval and reporting in one system.',
    ),
    'tores-foundation': dict(
        value='One web platform for a schools debating programme: competitions, live standings, and coaches’ expenses and stipends claimed, checked and paid in one place.',
        status='Delivered',
        users='The programme team, coaches at 24 Western Cape schools, and more than 430 learners whose results and standings the platform tracks',
        role='Designer and builder of the platform, commissioned by the University of Stellenbosch Business School',
        scope='Competition set-up and results, live league standings, mobile expense and stipend claims, claim verification and a single payment batch to finance',
        deliverables=[
            'Competition set-up in minutes: schools, rounds, motions and judges',
            'Results captured as each debate ends, with standings updating straight away through to the year-end final',
            'Coaches claiming expenses and stipends from their phones: pick the session, snap the receipt, submit',
            'Claims checked against the sessions actually run, then approved',
            'One approved payment batch sent to finance',
        ],
        timeframe=None,
        challenge=[
            'Every week, Tore’s Foundation runs debating for more than 430 learners in 24 schools across the Western Cape. Behind every debate is a coach, a competition to run, and expenses and stipends to pay.',
            'On paper, all of that was slow for everyone: results were compiled after the fact, standings lagged, and coaches’ claims had to be gathered, matched to sessions and paid one by one.',
            'The University of Stellenbosch Business School asked GEMIS to build one platform that would run the competition and the money side of the programme together.',
        ],
        approach=(
            ['One platform for the debates and the admin behind them', 'Results live, as they happen', 'Claims matched to sessions before they are paid'],
            [
                'GEMIS built a single web platform rather than separate tools. Competitions are set up in minutes — schools, rounds, motions and judges — and results are captured as each debate ends, so the standings update straight away, right through to the year-end final.',
                'The same web app handles the money. Coaches claim expenses and stipends from their phones by picking the session, photographing the receipt and submitting.',
                'The programme team checks every claim against the sessions actually run, approves it, and sends one payment batch to finance — so payment is both faster and verifiable.',
            ],
        ),
        outcomes=dict(
            delivered=[
                'Competition management with live standings',
                'Mobile expense and stipend claims for coaches',
                'Claim verification and a single payment batch to finance',
            ],
            verified=[],
            intended=[
                'More time for debate, less time on admin',
                'Standings and results trusted because they are captured at the event',
                'Coaches paid faster, against sessions that verifiably ran',
            ],
        ),
        related=['sonke', 'sbs-waterproofing'],
        cta='Running a programme on paper and spreadsheets? Let’s talk about one platform for the activity and the admin behind it.',
    ),
}
