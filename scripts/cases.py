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


# ── the redesign's detail: what each page can show beyond the record above ──
# Every line below comes from the case study video narration (transcripts in
# scripts/stories.py) or from scripts/facts.md. Where the repository holds no
# record — formal research, usability testing, user-acceptance records — the
# page says so; nothing is labelled research that was not.
DETAIL = {
    'sbs-waterproofing': {
        'role_short': 'Website partner from 2014; designer, builder and support partner of the business system from 2015',
        'status_short': 'Live — in daily use since 2015',
        'basis': [
            'There is no research report in the record for this project. The system was designed from how SBS Waterproofing already worked: an enquiry becomes a site visit, a quote, a deposit, a scheduled job and a final invoice, with stock consumed along the way.',
            'Two facts shaped the brief. Enquiries from the 2014 website and Google campaigns were arriving faster than the business could keep track of, and the off-the-shelf apps SBS tried did not fit that sequence, so leads were lost between tools.',
        ],
        'flow': [
            ('New enquiry', 'Captured once; the customer gets an SMS reference straight away'),
            ('Contacted', 'Every call, email and appointment hangs off the enquiry'),
            ('Site visit', 'Tracked on the same record through to the sale'),
            ('Quoted', 'A few clicks to send; the customer accepts online'),
            ('Won', 'The deposit invoice follows automatically into accounting'),
            ('Project', 'Profit shown per job; stock reorder reminders'),
        ],
        'flow_label': 'The SBS pipeline, from enquiry to project',
        'walk': [
            ('01-enquiry.jpg', 'Every enquiry, tracked', 'An enquiry is captured once, and the customer receives an SMS with a reference number straight away — so nothing arrives faster than it can be recorded.'),
            ('02-pipeline.jpg', 'From first call to the sale', 'New, contacted, site visit, quoted, won: every call, email and appointment is tracked on the enquiry, all the way to the sale.'),
            ('03-deposit.jpg', 'Quote. Accept. Deposit.', 'Quotes go out in a few clicks. When the customer accepts online, the deposit invoice follows automatically, straight into the accounting system.'),
            ('04-profit.jpg', 'Profit, job by job', 'Every project shows whether it made money, because the system holds the costs as well as the sale.'),
            ('05-stock.jpg', 'Stock under control', 'The system sends a reminder when stock needs reordering, before a job stalls.'),
            ('06-system.jpg', 'An operating system for growth', 'Enquiries, pipeline, quotes, invoices, products, projects, stock and staff in one place — in daily use since 2015.'),
        ],
        'decisions': [
            ('Enquiries were arriving faster than anyone could keep track of them.',
             'Make the enquiry the root record, captured once, with an SMS reference sent to the customer immediately.',
             'A single record that every call, email and appointment hangs off means nothing is lost between tools, and the customer has confirmation without a phone call.',
             'Delivered, as shown in the case study; the system has been in daily use since 2015.'),
            ('After a quote was accepted, the deposit and the accounting entry depended on someone remembering to raise them.',
             'Online quote acceptance raises the deposit invoice automatically and posts it into the accounting system.',
             'The hand-offs that leak time are the ones that rely on memory; automating them removes re-keying and the delay before a job can start.',
             'Delivered, as shown in the case study.'),
            ('Nobody could see which jobs made money.',
             'Hold the costs with the sale and show the profit on every project.',
             'Management decisions should come from live job data rather than a reconstruction at year-end.',
             'Delivered, as shown in the case study.'),
            ('A generic package would have forced SBS to work the package’s way.',
             'Design the system around SBS’s own pipeline, but general enough to serve other businesses.',
             'A system that fits the real sequence of work is the one the business keeps using; a general core lets it serve others without a rewrite.',
             'The same system became ManaGEM, which about a dozen companies run on today (facts.md).'),
        ],
        'validation': {
            'record': [
                'The website and campaign work came first (2014); the business system followed in 2015 and has been extended since.',
                'More than ten years on, SBS still runs its business on the system, and has grown many times over (as stated in the case study).',
                'The system was generalised into ManaGEM, which is itself in production.',
            ],
            'not_recorded': [
                'Formal usability testing or user-acceptance records are not in the repository, so none are claimed.',
            ],
        },
    },
    'homeassist': {
        'role_short': 'Designer, builder and long-term support partner',
        'status_short': 'Live — in use for more than ten years',
        'basis': [
            'The record holds no research report for this project. The design follows the four parties a burst geyser involves: the homeowner who reports it, the insurer who logs the claim, the plumber who repairs it, and HomeAssist, which coordinates a national panel.',
            'What each needed is stated in the case study: the homeowner wanted to report in minutes and then know what was happening; the insurer needed the claim logged and the warranty checked; the plumber needed to prove each step met SANS standards; HomeAssist needed to see every job without phoning around.',
        ],
        'flow': [
            ('Reported', 'The homeowner reports online, or the insurer logs the claim'),
            ('One job record', 'Either way, the job lands in the same place'),
            ('Dispatched', 'The next available plumber near the job is assigned automatically'),
            ('Informed', 'SMS or WhatsApp updates to the customer at every step'),
            ('Evidenced', 'The plumber photographs each step in the app — SANS compliance'),
            ('Signed off', 'Insurer and manufacturer links update the claim; one national view'),
        ],
        'flow_label': 'A HomeAssist job, from report to sign-off',
        'walk': [
            ('01-intake.jpg', 'Two ways in. One system.', 'The homeowner reports the burst geyser online in minutes, or the insurer logs the claim for them. Either way the job lands in one place.'),
            ('02-dispatch.jpg', 'The nearest available plumber, found automatically', 'HomeAssist works with a national panel. The system finds the next available plumber near the job and assigns it, without a phone call.'),
            ('03-updates.jpg', 'Updates by SMS or WhatsApp', 'The customer is kept informed at every step, so nobody has to phone around for updates.'),
            ('04-evidence.jpg', 'Photo proof of SANS compliance', 'On site, the plumber uses the app to photograph the work, proving each step meets SANS standards as it is done.'),
            ('05-insurers.jpg', 'Warranties checked. Claims updated.', 'Behind the scenes the system links directly to insurers and manufacturers, checking warranties and updating claims automatically.'),
            ('06-overview.jpg', 'Every job, nationwide, in one view', 'HomeAssist sees every job across the country in one place, from first report to sign-off.'),
        ],
        'decisions': [
            ('Homeowners and insurers reported the same problem through different channels.',
             'One job record with two ways in: the homeowner reports online, or the insurer logs the claim.',
             'Every party then works from the same job rather than reconciling two versions of it by phone and email.',
             'Delivered, as shown in the case study.'),
            ('Assigning a plumber from a national panel meant phoning around.',
             'Assign the next available plumber near the job automatically.',
             'Dispatch by proximity and availability is faster than any phone round, and it does not wait on a person.',
             'Delivered, as shown in the case study.'),
            ('SANS compliance had to be proved after the fact, from paperwork.',
             'The plumber’s app captures a photograph at each step of the repair.',
             'Evidence captured where the work happens is complete and dated; evidence reconstructed afterwards is neither.',
             'Delivered, as shown in the case study.'),
            ('Warranty positions and claim updates meant waiting on manufacturers and insurers.',
             'Link the system directly to insurers and manufacturers.',
             'The checks that used to be a phone call become part of the job’s own record, and the claim stays current.',
             'Delivered, as shown in the case study.'),
        ],
        'validation': {
            'record': [
                'GEMIS and HomeAssist have worked side by side for more than ten years, and the system remains in use (as stated in the case study).',
            ],
            'not_recorded': [
                'Formal usability testing, user-acceptance records and usage figures are not in the repository, so none are claimed.',
            ],
        },
    },
    'wastemart': {
        'role_short': 'Designer, builder and long-term support partner',
        'status_short': 'Live — more than ten years and still growing',
        'basis': [
            'The record holds no research report for this project. The design starts from the four manual jobs that sat behind one phone call at WasteMart: building a quote, attaching the right terms, chasing payment, and then remembering to tell operations.',
            'The constraint was that sales, finance and operations each held part of the picture, so the problem to solve was the chain of hand-offs between the call and the collection.',
        ],
        'flow': [
            ('Service picked', 'The quote is priced automatically, standard terms attached'),
            ('Accepted and paid', 'The customer accepts and pays through a secure link'),
            ('Operations alerted', 'The moment payment lands, the job goes onto the schedule'),
            ('Planned', 'Planners assign the truck and the driver'),
            ('Collected', 'The driver confirms the collection with a scan in the app'),
            ('Tracked', 'Managers and the customer see the order from quote to collection'),
        ],
        'flow_label': 'A WasteMart order, from call to collection',
        'walk': [
            ('01-quote.jpg', 'Quotes in minutes, terms included', 'The sales team picks the service and the quote is priced, with WasteMart’s standard terms and conditions attached automatically.'),
            ('02-payment.jpg', 'Accept and pay in one go', 'The customer receives the quote, accepts it, and gets a secure payment link straight away. No chasing, no waiting for proof of payment.'),
            ('03-schedule.jpg', 'Operations, alerted instantly', 'The moment payment comes through, operations is alerted and the job goes onto the schedule.'),
            ('04-collection.jpg', 'Planned, collected, confirmed', 'Planners assign the truck and driver, and the driver confirms the collection on the mobile app with a quick scan.'),
            ('05-overview.jpg', 'One view, quote to collection', 'Managers see every order from quote to collection in one place, and the customer can track it too.'),
        ],
        'decisions': [
            ('Quotes were built by hand and the right terms attached from memory.',
             'Price the quote automatically from the service picked, with standard terms and conditions attached every time.',
             'A quote that cannot go out without its terms removes a class of errors and most of the time spent building it.',
             'Delivered, as shown in the case study.'),
            ('Payment was chased, and proof of payment waited for.',
             'Send a secure payment link with the quote, and let payment itself trigger the next step.',
             'When payment drives the schedule there is nothing to chase and nothing to remember.',
             'Delivered; the client confirms six hours a week back, per depot (facts.md).'),
            ('Operations found out about jobs late.',
             'Alert operations the moment payment lands and put the job on the schedule automatically.',
             'The hand-off that depended on someone remembering to tell operations is removed entirely.',
             'Delivered, as shown in the case study.'),
            ('Nobody, including the customer, could see where an order stood.',
             'One shared order record, confirmed by the driver’s scan, visible to managers and customers.',
             'The driver’s scan closes the loop at the point of collection, so the view is current without a phone call.',
             'Delivered, as shown in the case study.'),
        ],
        'validation': {
            'record': [
                'The client has confirmed the one quantified result: six hours a week back, per depot (facts.md).',
                'The system has grown with WasteMart for more than ten years (as stated in the case study).',
            ],
            'not_recorded': [
                'Formal usability testing and user-acceptance records are not in the repository, so none are claimed.',
            ],
        },
    },
    'trans-hex': {
        'role_short': 'Stabilised the in-house system, automated the SAP feed, built the reporting into it',
        'status_short': 'Delivered 2017; a second version followed',
        'basis': [
            'The record holds no research report for this project. The brief was management’s own: one clear view across plant, mining, finance, security and people at the Baken mine, in place of a report pieced together in Excel from several sources over weeks, with errors creeping in.',
            'The constraint was that the data already existed in systems the mine depended on — SAP among them — so the problem was getting it into one reliable, repeatable report.',
        ],
        'flow': [
            ('SAP', 'Financial data in the systems the mine already runs on'),
            ('Daily feed', 'Scheduled; duplicates skipped; every run logged'),
            ('Failure email', 'The team is told if anything fails — a missing day is noticed'),
            ('The company MIS', 'Stabilised first, then holds the imported data'),
            ('Integrated report', 'Plant, mining, finance, security and HR; budget against actual'),
            ('Version two', 'Weekly figures, forecasts, variances, exchange rates, mine groups'),
        ],
        'flow_label': 'The Trans Hex data flow, from SAP to the management report',
        'walk': [
            ('01-stabilise.jpg', 'First, make it work', 'GEMIS first got the company’s own information system running reliably, so nothing new was built on an unstable base.'),
            ('02-sap-feed.jpg', 'SAP data, in every morning', 'The daily feed of financial data from SAP runs on schedule, skips duplicates, logs what it did, and emails the team if anything fails.'),
            ('03-budget.jpg', 'Budget against actual', 'Gravel treated, carats, fleet availability and cost per carat, for the month and the year to date, built into the system itself.'),
            ('04-filter.jpg', 'Any mine. Any period.', 'Filter by mine, period or date range, then export to Excel or PDF.'),
            ('05-forecast.jpg', 'Weekly. Forecast. Variance.', 'Version two added weekly figures, forecasts, variances and live exchange rates.'),
            ('06-operations.jpg', 'Every operation, one view', 'Mine groups brought other operations into the same report.'),
        ],
        'decisions': [
            ('The existing information system was not reliable enough to build on.',
             'Stabilise the company’s own system before adding anything to it.',
             'A report is only as trustworthy as the system that holds its data; fixing the foundation first avoided building errors in.',
             'Delivered, as shown in the case study.'),
            ('Financial data was re-keyed from SAP into spreadsheets, and errors crept in.',
             'Automate a daily SAP feed that runs on schedule, skips duplicates and logs every run.',
             'Loading the data once, automatically, removes the manual copy that introduced the errors.',
             'Delivered, as shown in the case study.'),
            ('A silent failure in an automated feed would only be discovered at month-end.',
             'Email the team if any run fails.',
             'Automation that fails loudly is safer than automation that fails quietly; a missing day is noticed the same morning.',
             'Delivered, as shown in the case study.'),
            ('The management report lived outside the system, assembled by hand.',
             'Build the report into the system, with filters by mine and period and export to Excel and PDF.',
             'A report generated from the system is repeatable and current; one assembled beside it is neither.',
             'A report that took weeks became available whenever it was needed (as stated in the case study); version two extended the same structure.'),
        ],
        'validation': {
            'record': [
                'Delivered in 2017 (facts.md).',
                'A second version followed, adding weekly figures, forecasts, variances, live exchange rates and mine groups — evidence that the first version was used and extended.',
            ],
            'not_recorded': [
                'Time-saving figures beyond the case study’s own statement, and user-acceptance records, are not in the repository, so none are claimed.',
            ],
        },
    },
    'sonke': {
        'role_short': 'Designer and builder of the monitoring and evaluation system',
        'status_short': 'Delivered 2018',
        'basis': [
            'The record holds no research report for this project. The design follows the question funders ask — what difference did it make? — and the conditions under which the answer has to be gathered: sessions held far from any office, often without signal, across forty countries.',
            'The problem was both capture and credibility: getting field data in reliably, and making it trustworthy enough to report.',
        ],
        'flow': [
            ('Captured in the field', 'Facilitators record each session on the mobile app, offline'),
            ('Synced', 'When there is signal, the records come in'),
            ('Checked', 'M&E officers review and approve each record'),
            ('Counted', 'Only approved activity counts against targets'),
            ('Seen by role', 'Country teams see their country; leadership the whole picture'),
            ('Reported', 'Donor reports assemble from already-verified data'),
        ],
        'flow_label': 'The Sonke monitoring and evaluation flow',
        'walk': [
            ('01-capture.jpg', 'Captured in the field. Even offline.', 'Facilitators capture each session on a mobile app. It works offline and syncs when there is signal, so a lack of connectivity never means a lost record.'),
            ('02-approve.jpg', 'Checked once, trusted everywhere', 'Back in the office, M&E officers check and approve what comes in, so every number can be traced to a real activity.'),
            ('03-roles.jpg', 'The right view for every role', 'Programme managers see progress against targets by country and programme; each person sees what their role needs.'),
            ('04-donor.jpg', 'Donor reports, ready when you are', 'When reporting time comes the figures are already there, assembled from data that has already been checked.'),
        ],
        'decisions': [
            ('Sessions happen far from any office, often without signal.',
             'An offline-first mobile app that syncs when there is signal.',
             'If capture depends on connectivity, the records that matter most — the remote ones — are the ones lost.',
             'Delivered, as shown in the case study.'),
            ('Funders need to trust that reported numbers correspond to real activities.',
             'Nothing counts until an M&E officer has checked and approved it.',
             'An approval step between capture and counting is what makes every figure traceable to a session.',
             'Delivered, as shown in the case study.'),
            ('Country teams and leadership need different views of the same data.',
             'Role-based views: each role sees what it needs, and progress against targets is live by country and programme.',
             'One system can serve the field, the office and leadership if each sees its own slice rather than everything.',
             'Delivered, as shown in the case study.'),
        ],
        'validation': {
            'record': [
                'Delivered in 2018 (facts.md).',
            ],
            'not_recorded': [
                'Whether the system remains in use, usage figures, usability testing and user-acceptance records are not in the repository, so none are claimed.',
            ],
        },
    },
    'tores-foundation': {
        'role_short': 'Designer and builder, commissioned by the University of Stellenbosch Business School',
        'status_short': 'Delivered',
        'basis': [
            'The record holds no research report for this project. The design follows the programme as it runs: every week, debating for more than 430 learners in 24 schools, each debate with a coach, a competition to run, and expenses and stipends to pay — all of it previously on paper.',
            'The University of Stellenbosch Business School asked for one platform that would run the competition and the money side of the programme together.',
        ],
        'flow': [
            ('Competition set up', 'Schools, rounds, motions and judges, in minutes'),
            ('Results captured', 'As each debate ends'),
            ('Standings live', 'Updated straight away, through to the year-end final'),
            ('Claims from the phone', 'Pick the session, snap the receipt, submit'),
            ('Checked', 'Every claim matched to a session that actually ran'),
            ('Paid', 'One approved payment batch to finance'),
        ],
        'flow_label': 'The Tore’s Foundation platform, from fixtures to payment',
        'walk': [
            ('01-competitions.jpg', 'Competitions set up in minutes', 'Schools, rounds, motions and judges are set up in minutes, for the University of Stellenbosch Business School’s programme.'),
            ('02-standings.jpg', 'Results in, standings live', 'Results are captured as each debate ends and the standings update straight away, right through to the year-end final.'),
            ('03-claims.jpg', 'Coaches claim from their phone', 'Coaches claim expenses and stipends in the same web app: pick the session, snap the receipt, submit.'),
            ('04-approval.jpg', 'Checked, approved, paid', 'The programme team checks every claim against the sessions actually run, approves it, and sends one payment batch to finance.'),
        ],
        'decisions': [
            ('Fixtures, scores and claims were all on paper, and slow for everyone.',
             'One web platform for the debates and the admin behind them, rather than separate tools.',
             'The competition and the money are linked — claims are for sessions — so one system can verify what two cannot.',
             'Delivered, as shown in the case study.'),
            ('Standings lagged because results were compiled after the fact.',
             'Capture results as each debate ends and update the standings straight away.',
             'Results captured at the event are trusted; results compiled later are questioned.',
             'Delivered, as shown in the case study.'),
            ('Coaches’ claims had to be gathered, matched to sessions and paid one by one.',
             'Claims from the phone with the receipt attached, checked against the sessions that ran, paid in one batch.',
             'Matching a claim to a recorded session makes payment both faster and verifiable.',
             'Delivered, as shown in the case study.'),
        ],
        'validation': {
            'record': [
                'Delivered for the University of Stellenbosch Business School (facts.md gives 2014 for the engagement; the case study records the programme at 24 schools and more than 430 learners).',
            ],
            'not_recorded': [
                'Whether the platform remains in use, participation changes, payment-time improvements and testing records are not in the repository, so none are claimed.',
            ],
        },
    },
}

for _k, _v in DETAIL.items():
    CASES[_k].update(_v)


# ── ManaGEM, the product: the same evidence kit, from its own video ───────
MANAGEM = {
    'flow': [
        ('Enquiry', 'Captured once; the customer gets SMS and email updates'),
        ('Pipeline', 'Followed through every contact to the sale'),
        ('Quote', 'Sent in a few clicks; accepted online'),
        ('Deposit invoice', 'Follows automatically on acceptance'),
        ('Project', 'Tracked, with the profit on each job'),
        ('Stock and staff', 'Stock alerts before you run out; products, prices and staff records'),
    ],
    'flow_label': 'ManaGEM, from enquiry to invoice',
    'walk': [
        ('01-pipeline.jpg', 'From enquiry to sale', 'Capture every enquiry and follow it to the sale, with SMS and email updates for the customer.'),
        ('02-quotes.jpg', 'Quotes that close', 'Quotes go out in a few clicks, customers accept online, and deposit invoices follow automatically.'),
        ('03-profit.jpg', 'Know what every job earns', 'Track every project and see the profit on each job.'),
        ('04-stock.jpg', 'Stock under control', 'Keep track of stock, and get an alert before you run out.'),
        ('05-modules.jpg', 'One place for the whole business', 'Enquiries, pipeline, quotes, invoices, products, projects, stock and staff records sit in the same system.'),
        ('06-companies.jpg', 'About a dozen companies, every day', 'Built for one business and designed for many: about a dozen companies run their day-to-day operations on ManaGEM.'),
    ],
}
