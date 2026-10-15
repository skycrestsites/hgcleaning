"""Generates the static H&G Cleaning Co. site.

Run from the project root:  python tools/build.py
Edit business details in BUSINESS and service copy in SERVICES, then rebuild.
"""
import json
import os
import re
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUSINESS = {
    "name": "H&G Cleaning Co.",
    "short": "H&G Cleaning",
    "tagline": "Elevating Clean",
    "domain": "https://hgcleaningco.com",
    "phone": "(801) 555-0142",
    "phone_href": "+18015550142",
    "email": "hello@hgcleaningco.com",
    "city": "Salt Lake City",
    "region": "UT",
    "region_long": "Utah",
    "area_label": "Salt Lake City & Surrounding Areas",
    "lat": 40.7608,
    "lng": -111.8910,
    "hours": "Mon to Sat, 8:00 AM to 6:00 PM",
}

AREAS = [
    "Salt Lake City", "Sandy", "Draper", "West Jordan", "South Jordan", "Murray",
    "Holladay", "Millcreek", "Cottonwood Heights", "Midvale", "Taylorsville", "West Valley City",
    "Riverton", "Herriman", "Bountiful",
]

REVIEWS = [
    ("Sarah M.", "Recurring client", "Super easy to book and the cleaning team did an amazing job. They showed up on time, were professional, and left the entire house looking spotless. I've already signed up for recurring cleanings!"),
    ("Jessica R.", "Standard cleaning", "I've tried a few cleaning companies before and this has easily been the best experience. Communication was great, pricing was straightforward, and my home looked incredible afterward."),
    ("Michael T.", "Deep cleaning", "We booked a deep clean and were extremely impressed. They paid attention to the little details and got areas cleaner than we expected. Definitely using them again."),
    ("Amanda L.", "Bi-weekly plan", "Having them come every two weeks has been a lifesaver. They're reliable, consistent, and it's so nice coming home to a clean house without having to worry about it."),
    ("David K.", "Move-out cleaning", "Great experience from start to finish. Booking was simple, they kept me updated, and the cleaners did a fantastic job. Professional, dependable, and absolutely worth it."),
]

# --------------------------------------------------------------------------- icons
_I = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "chev-down": '<path d="m6 9 6 6 6-6"/>',
    "chev-right": '<path d="m9 18 6-6-6-6"/>',
    "plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "star": '<path d="M11.48 3.5a.56.56 0 0 1 1.04 0l2.13 5.11a.56.56 0 0 0 .48.35l5.52.44c.5.04.7.66.32.99l-4.2 3.6a.56.56 0 0 0-.18.56l1.28 5.39a.56.56 0 0 1-.84.61l-4.72-2.89a.56.56 0 0 0-.59 0l-4.73 2.89a.56.56 0 0 1-.84-.61l1.28-5.39a.56.56 0 0 0-.18-.56l-4.2-3.6a.56.56 0 0 1 .32-.99l5.52-.44a.56.56 0 0 0 .47-.35z"/>',
    "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .71-1.53l7-6a2 2 0 0 1 2.58 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "sparkles": '<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.13-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.13a.5.5 0 0 1 .96 0L14.06 8.5A2 2 0 0 0 15.5 9.94l6.13 1.58a.5.5 0 0 1 0 .96L15.5 14.06a2 2 0 0 0-1.44 1.44l-1.58 6.13a.5.5 0 0 1-.96 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    "hardhat": '<path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M14 6a6 6 0 0 1 6 6v3"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><rect x="2" y="15" width="20" height="4" rx="1"/>',
    "key": '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    "plus-square": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 12h8"/><path d="M12 8v8"/>',
    "spray": '<path d="M3 3h.01"/><path d="M7 5h.01"/><path d="M11 7h.01"/><path d="M3 7h.01"/><path d="M7 9h.01"/><path d="M3 11h.01"/><rect x="15" y="5" width="4" height="4"/><path d="m19 9 2 2v10c0 .6-.4 1-1 1h-6c-.6 0-1-.4-1-1V11l2-2"/><path d="m13 14 8-2"/><path d="m13 19 8-2"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "message": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01"/><path d="M15 9h.01"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>',
    "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect x="2" y="6" width="20" height="14" rx="2"/>',
    "hammer": '<path d="m15 12-8.37 8.37a2.12 2.12 0 1 1-3-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25v-.86L16.01 4.6a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/>',
    "bed": '<path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/>',
    "star-outline": '<path d="M11.48 3.5a.56.56 0 0 1 1.04 0l2.13 5.11a.56.56 0 0 0 .48.35l5.52.44c.5.04.7.66.32.99l-4.2 3.6a.56.56 0 0 0-.18.56l1.28 5.39a.56.56 0 0 1-.84.61l-4.72-2.89a.56.56 0 0 0-.59 0l-4.73 2.89a.56.56 0 0 1-.84-.61l1.28-5.39a.56.56 0 0 0-.18-.56l-4.2-3.6a.56.56 0 0 1 .32-.99l5.52-.44a.56.56 0 0 0 .47-.35z"/>',
    "fridge": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M5 10h14"/><path d="M9 6v1"/><path d="M9 13v3"/>',
    "oven": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><rect x="7" y="12" width="10" height="6" rx="1"/><path d="M7 6h.01"/><path d="M11 6h.01"/>',
    "window": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18"/><path d="M3 12h18"/>',
    "cabinet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18"/><path d="M9 11v2"/><path d="M15 11v2"/>',
    "dishes": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/>',
    "shirt": '<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>',
    "blinds": '<path d="M3 3h18"/><path d="M20 7H8"/><path d="M20 11H8"/><path d="M10 19h10"/><path d="M8 15h12"/><path d="M4 3v14"/><circle cx="4" cy="19" r="2"/>',
    "wall": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/><path d="M9 3v6"/><path d="M15 9v6"/><path d="M9 15v6"/>',
}


def icon(name, cls=""):
    fill = ' fill="currentColor" stroke="none"' if name == "star" else ' fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24"{fill} aria-hidden="true" focusable="false">{_I[name]}</svg>'


def stars(n=5):
    return f'<span class="stars" aria-label="{n} out of 5 stars">' + icon("star") * n + "</span>"


# --------------------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "standard-cleaning",
        "name": "Standard Cleaning",
        "nav": "Routine upkeep for a fresh, tidy home",
        "icon": "home",
        "card": "Routine cleaning that keeps your home fresh and maintained: dusting, vacuuming, mopping, kitchens, bathrooms and general tidying.",
        "title": "Standard House Cleaning in Salt Lake City, UT",
        "desc": "Professional standard house cleaning in Salt Lake City and nearby areas. Dusting, vacuuming, mopping, kitchens and bathrooms done right by a background-checked team.",
        "h1": "Standard Cleaning",
        "lead": "Routine cleaning designed to keep your home fresh, comfortable and guest-ready. We take care of the everyday work so your evenings and weekends stay yours.",
        "facts": ["Kitchens and bathrooms", "Floors vacuumed and mopped", "Same team, consistent results"],
        "chip": ("Most booked", "Ideal for regular upkeep"),
        "hero": ("standard-kitchen-island", "Bright, freshly cleaned kitchen with a granite island and stainless appliances"),
        "overview": [
            "Our standard cleaning is the reliable reset your home needs. Every visit follows a clear checklist so you know exactly what is covered, from wiped kitchen counters and polished fixtures to vacuumed rugs and mopped floors.",
            "It is the perfect fit for homes that are already in good shape and simply need consistent care. Pair it with a recurring plan and your home stays clean week after week without you having to think about it.",
        ],
        "included": [
            ("Kitchen", ["Countertops and backsplash wiped and sanitized", "Exterior of appliances, microwave and cabinet fronts", "Sink scrubbed and faucet polished", "Floors vacuumed and mopped"]),
            ("Bathrooms", ["Toilets, tubs and showers cleaned and disinfected", "Mirrors and glass streak-free", "Vanities, sinks and fixtures shined", "Floors washed and trash emptied"]),
            ("Living Areas and Bedrooms", ["Dusting of reachable surfaces, shelves and decor", "Carpets and rugs vacuumed", "Hard floors mopped", "Beds made and general tidying"]),
        ],
        "gallery": [
            ("standard-white-kitchen", "White kitchen with clean counters and cabinetry", "Kitchens"),
            ("standard-mopping-floor", "Cleaner mopping a hardwood floor", "Floors"),
            ("standard-wiping-counter", "Gloved hand wiping a kitchen counter", "Surfaces"),
        ],
        "ideal": [
            ("users", "Busy families", "Keep up with the everyday mess without giving up your free time."),
            ("briefcase", "Working professionals", "Come home to a clean, calm space at the end of a long day."),
            ("calendar", "Recurring clients", "The go-to service for weekly, bi-weekly and monthly plans."),
        ],
        "review": 1,
        "faqs": [
            ("How long does a standard cleaning take?", "Most homes take two to four hours depending on size, number of bathrooms and the condition of the home. You will see clear pricing when you book online."),
            ("Do I need to be home during the cleaning?", "Not at all. Many clients give us entry instructions and come home to a finished clean. We will confirm arrival and let you know when we are done."),
            ("What is the difference between standard and deep cleaning?", "Standard cleaning maintains a home that is already in good shape. Deep cleaning goes further into buildup, baseboards, fixtures and hard-to-reach areas. If it has been a while, we usually recommend starting with a deep clean."),
        ],
    },
    {
        "slug": "deep-cleaning",
        "name": "Deep Cleaning",
        "nav": "Top-to-bottom detail for buildup",
        "icon": "sparkles",
        "card": "A detailed, top-to-bottom clean that targets buildup, baseboards, fixtures and the hard-to-reach areas that are often overlooked.",
        "title": "Deep Cleaning Services in Salt Lake City, UT",
        "desc": "Top-to-bottom deep cleaning in Salt Lake City. We target buildup, baseboards, fixtures, grout and hard-to-reach areas so your home feels truly clean again.",
        "h1": "Deep Cleaning",
        "lead": "A detailed, top-to-bottom clean that reaches the places routine cleaning cannot. We target buildup, grime and the commonly overlooked surfaces so your home feels brand new again.",
        "facts": ["Baseboards and trim", "Fixtures and grout detailed", "Ideal first visit"],
        "chip": ("Detail focused", "Every corner covered"),
        "hero": ("deep-steam-cleaning", "Cleaner steam cleaning a radiator during a detailed deep clean"),
        "overview": [
            "Over time, dust, soap scum and grease settle into the corners of every home. Our deep cleaning service is built to remove that buildup. We slow down, work room by room and give attention to the details that make a home feel genuinely clean.",
            "Deep cleaning is the best starting point for new clients, seasonal refreshes and homes preparing for guests or special occasions. Once your home is reset, a recurring standard clean keeps it that way.",
        ],
        "included": [
            ("Everything in a Standard Clean, plus", ["Baseboards, door frames and trim hand-wiped", "Light switches, outlets and door handles sanitized", "Window sills and tracks detailed", "Ceiling fans, vents and light fixtures dusted"]),
            ("Kitchen Detail", ["Stovetop degreased and burner areas scrubbed", "Cabinet fronts and handles detailed", "Backsplash grout and edges cleaned", "Small appliances wiped inside and out"]),
            ("Bathroom Detail", ["Soap scum and hard water buildup removed", "Grout lines scrubbed", "Behind and around toilets detailed", "Fixtures descaled and polished"]),
        ],
        "gallery": [
            ("deep-stovetop-detail", "Hand wiping down a gas stovetop with a microfiber cloth", "Stovetops"),
            ("deep-grout-scrubbing", "Brush scrubbing tile grout during a deep clean", "Tile and grout"),
            ("deep-carpet-extraction", "Carpet being cleaned with an extraction tool", "Carpets"),
        ],
        "ideal": [
            ("sparkles", "First-time clients", "Start fresh with a thorough reset before moving to routine care."),
            ("refresh", "Seasonal refreshes", "Spring cleaning, holiday prep or a long overdue catch-up."),
            ("users", "Hosting and events", "Get every room ready before family or guests arrive."),
        ],
        "review": 2,
        "faqs": [
            ("How often should I book a deep clean?", "Most homes benefit from a deep clean every three to six months, with standard cleanings in between to maintain the results."),
            ("How long does a deep clean take?", "A deep clean typically takes longer than a standard visit, often four to eight hours depending on the size and condition of the home. Larger homes may have a bigger team assigned."),
            ("Do you bring your own supplies?", "Yes. Our team arrives with professional-grade supplies and equipment. If you prefer a specific product in your home, just let us know."),
        ],
    },
    {
        "slug": "recurring-cleaning",
        "name": "Recurring Cleaning",
        "nav": "Weekly, bi-weekly or monthly plans",
        "icon": "calendar",
        "card": "Weekly, bi-weekly or monthly visits that keep your home consistently clean without the hassle of scheduling each visit.",
        "title": "Recurring House Cleaning Plans in Salt Lake City, UT",
        "desc": "Weekly, bi-weekly and monthly house cleaning plans in Salt Lake City. A consistent, background-checked team keeps your home clean without the scheduling hassle.",
        "h1": "Recurring Cleaning",
        "lead": "Weekly, bi-weekly or monthly cleaning that keeps your home consistently clean. Set your schedule once and enjoy a fresh home without booking every visit.",
        "facts": ["Weekly, bi-weekly or monthly", "Consistent, familiar team", "Flexible rescheduling"],
        "chip": ("Set it and forget it", "Your schedule, handled"),
        "hero": ("recurring-made-bedroom", "Neatly made bed in a calm, freshly cleaned bedroom"),
        "overview": [
            "A clean home should not depend on finding time in your week. With a recurring plan, we show up on your schedule and keep everything maintained, so the mess never has a chance to build up.",
            "Your plan is built around your home. We learn your preferences, focus on the rooms that matter most and keep communication simple. Need to skip a week or move a visit? Just let us know.",
        ],
        "included": [
            ("Every Visit", ["Kitchen counters, sink and appliance exteriors cleaned", "Bathrooms cleaned and disinfected", "Dusting throughout the home", "Floors vacuumed and mopped"]),
            ("Plan Options", ["Weekly: best for busy households, pets and kids", "Bi-weekly: our most popular balance of value and upkeep", "Monthly: a reliable reset to stay on top of things"]),
            ("Plan Benefits", ["Priority scheduling on your preferred day", "Same team whenever possible", "Notes on your preferences kept on file"]),
        ],
        "gallery": [
            ("recurring-vacuuming-bedroom", "Cleaner vacuuming the floor beside a bed", "Bedrooms"),
            ("recurring-tidy-living-room", "Tidy, bright living room with a sofa and natural light", "Living spaces"),
            ("recurring-bright-bedroom", "Bright bedroom with fresh linens", "Fresh linens"),
        ],
        "ideal": [
            ("users", "Families with kids", "Stay ahead of daily messes with weekly or bi-weekly care."),
            ("heart", "Pet owners", "Regular visits keep fur, dander and paw prints under control."),
            ("briefcase", "Busy professionals", "One less thing to manage, every single week."),
        ],
        "review": 3,
        "faqs": [
            ("Am I locked into a contract?", "No. Our recurring plans are flexible. You can pause, skip or change your frequency with notice."),
            ("Will I have the same cleaners each time?", "We do our best to send the same team for every visit so they learn your home and your preferences."),
            ("Should I start with a deep clean?", "If your home has not been professionally cleaned recently, we usually recommend a deep clean first. It makes every recurring visit after that more effective."),
        ],
    },
    {
        "slug": "move-in-move-out-cleaning",
        "name": "Move-In / Move-Out Cleaning",
        "nav": "Empty-home cleaning for a smooth handover",
        "icon": "key",
        "card": "Thorough cleaning for empty or transitioning homes, preparing the space for new occupants, landlords or property managers.",
        "title": "Move-In and Move-Out Cleaning in Salt Lake City, UT",
        "desc": "Move-in and move-out cleaning in Salt Lake City for tenants, homeowners, landlords and property managers. Inside cabinets, appliances, baseboards and more.",
        "h1": "Move-In / Move-Out Cleaning",
        "lead": "A thorough clean for empty and transitioning homes. Whether you are handing back the keys or settling into a new place, we get every room ready for its next chapter.",
        "facts": ["Inside cabinets and drawers", "Appliances inside and out", "Landlord-ready results"],
        "chip": ("Handover ready", "For tenants and owners"),
        "hero": ("move-home-exterior", "Classic two-story family home ready for new occupants"),
        "overview": [
            "Moving is stressful enough. Our move-in and move-out service takes cleaning off your list. With the home empty, we can reach every surface, including the inside of cabinets, closets and appliances that are usually hidden.",
            "We work with renters hoping to get their deposit back, homeowners preparing to list or move in, and landlords and property managers turning over units between tenants.",
        ],
        "included": [
            ("Kitchen", ["Inside and outside of all cabinets and drawers", "Inside refrigerator, oven and microwave", "Counters, sink and backsplash scrubbed", "Floors detailed along edges and corners"]),
            ("Bathrooms", ["Toilets, tubs and showers deep cleaned", "Inside vanities and medicine cabinets", "Mirrors, fixtures and tile polished", "Floors scrubbed and baseboards wiped"]),
            ("Whole Home", ["Closets, shelves and storage spaces wiped", "Baseboards, doors and frames cleaned", "Light switches and outlets sanitized", "All floors vacuumed and mopped"]),
        ],
        "gallery": [
            ("move-moving-day-boxes", "Woman unpacking moving boxes with her dog on moving day", "Moving day"),
            ("move-empty-carpet-vacuum", "Carpet being vacuumed in an empty room", "Empty rooms"),
            ("move-spray-and-wipe", "Gloved hands spraying and wiping a surface", "Surfaces"),
        ],
        "ideal": [
            ("key", "Renters moving out", "Leave your rental spotless and give yourself the best shot at your deposit."),
            ("home", "New homeowners", "Move into a home that is clean, fresh and truly yours from day one."),
            ("building", "Landlords and property managers", "Fast, dependable turnovers between tenants."),
        ],
        "review": 4,
        "faqs": [
            ("Does the home need to be empty?", "For the best results, yes. An empty home lets us reach inside cabinets, closets and behind where furniture used to be."),
            ("Do you clean inside appliances?", "Yes. Move-in and move-out cleanings include the inside of the refrigerator, oven and microwave."),
            ("Can you work with my property manager?", "Absolutely. We regularly coordinate access and timing with landlords and property managers."),
        ],
    },
    {
        "slug": "commercial-cleaning",
        "name": "Commercial Cleaning",
        "nav": "Offices, retail and commercial spaces",
        "icon": "building",
        "card": "Customized cleaning for offices, retail spaces and commercial properties that keeps your workplace clean and professional.",
        "title": "Commercial and Office Cleaning in Salt Lake City, UT",
        "desc": "Commercial cleaning for offices, retail stores and commercial properties in Salt Lake City. Customized schedules and a dependable, background-checked team.",
        "h1": "Commercial Cleaning",
        "lead": "Customized cleaning for offices, retail spaces and commercial properties. We help you maintain a clean, healthy and professional environment for your team and your clients.",
        "facts": ["Custom cleaning scopes", "After-hours scheduling", "Reliable, vetted team"],
        "chip": ("Built around you", "Daily, weekly or custom"),
        "hero": ("commercial-office-glass", "Commercial cleaning team vacuuming and wiping glass in a modern office"),
        "overview": [
            "Your space says a lot about your business. We build a cleaning plan around how your space is actually used, from high-traffic entryways and restrooms to shared kitchens, workstations and conference rooms.",
            "We schedule around your hours to keep disruption to a minimum, and we keep communication clear so you always know what was done and when.",
        ],
        "included": [
            ("Workspaces", ["Desks, workstations and shared surfaces wiped", "Trash and recycling emptied", "Glass doors and partitions cleaned", "Carpets vacuumed and hard floors mopped"]),
            ("Restrooms and Break Rooms", ["Restrooms cleaned, disinfected and restocked", "Kitchenette counters, sinks and appliances wiped", "High-touch points sanitized", "Floors washed"]),
            ("Common Areas", ["Reception and lobby areas detailed", "Conference rooms reset", "Entryways and doors cleaned", "Dusting of ledges, sills and fixtures"]),
        ],
        "gallery": [
            ("commercial-office-plants", "Clean, bright open office with plants and desks", "Open offices"),
            ("commercial-office-corridor", "Polished office hallway with glass walls", "Hallways"),
            ("commercial-office-lounge", "Clean office lounge and meeting space", "Shared spaces"),
        ],
        "ideal": [
            ("briefcase", "Offices", "Clean, healthy workspaces that help your team do their best work."),
            ("store", "Retail stores", "A spotless storefront that makes a strong first impression."),
            ("building", "Commercial properties", "Dependable care for common areas, lobbies and shared spaces."),
        ],
        "review": 1,
        "faqs": [
            ("Can you clean outside of business hours?", "Yes. We offer early morning, evening and weekend scheduling so cleaning never interrupts your day."),
            ("Do you offer custom cleaning plans?", "Every commercial plan is customized. We walk through your space, learn your priorities and build a scope and schedule that fits."),
            ("What types of businesses do you clean?", "We clean offices, retail spaces, studios and other commercial properties throughout the Salt Lake City area."),
        ],
    },
    {
        "slug": "post-construction-cleaning",
        "name": "Post-Construction Cleaning",
        "nav": "Dust and debris removal after a build",
        "icon": "hardhat",
        "card": "Detailed removal of construction dust, debris and residue to get newly built or renovated spaces ready for use.",
        "title": "Post-Construction Cleaning in Salt Lake City, UT",
        "desc": "Post-construction and renovation cleaning in Salt Lake City. We remove fine dust, debris and residue so new builds and remodels are move-in ready.",
        "h1": "Post-Construction Cleaning",
        "lead": "Detailed removal of construction dust, debris and residue. We turn newly built and renovated spaces into clean, finished rooms that are ready to use and enjoy.",
        "facts": ["Fine dust removal", "Residue and stickers removed", "Builder and homeowner friendly"],
        "chip": ("Move-in ready", "From job site to finished"),
        "hero": ("construction-dust-vacuum", "Worker vacuuming construction dust from a newly renovated floor"),
        "overview": [
            "Renovations and new builds leave behind a layer of fine dust that settles on every surface, inside cabinets and in vents. Standard cleaning simply is not built for it. Our post-construction service is.",
            "We work top to bottom, removing dust, debris, paint specks and adhesive residue so the finished space looks the way it was meant to. We coordinate with homeowners, contractors and builders to fit your timeline.",
        ],
        "included": [
            ("Dust and Debris", ["Fine construction dust removed from all surfaces", "Vents, fans and light fixtures dusted", "Loose debris cleared and floors vacuumed", "Window sills, ledges and trim detailed"]),
            ("Finishing Details", ["Stickers, labels and adhesive residue removed", "Light paint and grout haze cleaned where safe", "Cabinets and drawers wiped inside and out", "Fixtures, hardware and glass polished"]),
            ("Final Clean", ["Kitchens and bathrooms fully cleaned", "Hard floors washed and detailed", "Carpets vacuumed thoroughly", "Final walkthrough for a move-in ready finish"]),
        ],
        "gallery": [
            ("construction-floor-machine", "Floor cleaning machine polishing a new tile floor", "Floor care"),
            ("construction-site-renovation", "Construction crew working on a building site", "Active builds"),
            ("deep-grout-scrubbing", "Tile being scrubbed clean after installation", "New tile"),
        ],
        "ideal": [
            ("hammer", "Home renovations", "Kitchen remodels, basement finishes and whole-home updates."),
            ("hardhat", "Builders and contractors", "Hand over a clean, finished project to your client."),
            ("home", "New construction", "Make your brand new home feel ready from the first night."),
        ],
        "review": 2,
        "faqs": [
            ("When should post-construction cleaning be scheduled?", "Once major work, painting and installations are complete. If trades are still finishing small items, we can schedule a rough clean and a final clean."),
            ("Do you remove large construction debris?", "We remove dust, light debris and residue. Large debris such as lumber, drywall scraps and dumpster loads should be cleared by the contractor first."),
            ("Do you work with contractors directly?", "Yes. We are happy to coordinate timing and access with your builder or general contractor."),
        ],
    },
    {
        "slug": "airbnb-vacation-rental-cleaning",
        "name": "Vacation Rental / Airbnb Cleaning",
        "nav": "Guest-ready turnovers between stays",
        "icon": "bed",
        "card": "Reliable turnover cleaning between guests, including cleaning and resetting your property so it is ready for the next stay.",
        "title": "Airbnb and Vacation Rental Cleaning in Salt Lake City, UT",
        "desc": "Reliable Airbnb and vacation rental turnover cleaning in Salt Lake City. Fresh linens, restocking and a guest-ready reset between every stay.",
        "h1": "Vacation Rental / Airbnb Cleaning",
        "lead": "Reliable turnover cleaning between guests. We clean and reset your property to the same high standard every time, so every guest walks into a five-star stay.",
        "facts": ["Fast turnovers", "Linens and bed reset", "Consistent, photo-ready results"],
        "chip": ("Guest ready", "Between every stay"),
        "hero": ("rental-guest-bedroom", "Hotel-style guest bedroom with crisp white linens"),
        "overview": [
            "In short-term rentals, cleanliness drives reviews, and reviews drive bookings. Our turnover service gives hosts a dependable team that cleans, resets and checks every detail between guests.",
            "We follow your checklist and house standards, work within check-out and check-in windows and let you know right away if we spot damage or anything that needs attention.",
        ],
        "included": [
            ("Turnover Clean", ["Full kitchen and bathroom cleaning", "Dusting, vacuuming and mopping throughout", "Trash removed and bins relined", "Dishes washed and put away"]),
            ("Guest Reset", ["Beds made with fresh linens", "Towels replaced and staged", "Furniture and decor reset to your photos", "Toiletries and essentials restocked from your supply"]),
            ("Host Support", ["Follows your custom checklist", "Damage or missing items reported", "Flexible same-day turnovers", "Clear communication after every clean"]),
        ],
        "gallery": [
            ("rental-apartment-living", "Stylish, clean rental apartment living room", "Living spaces"),
            ("rental-cozy-bedroom", "Cozy rental bedroom with neatly made bed", "Bedrooms"),
            ("rental-spotless-bathroom", "Spotless modern bathroom with glass shower", "Bathrooms"),
        ],
        "ideal": [
            ("bed", "Airbnb and VRBO hosts", "Protect your ratings with consistent, guest-ready turnovers."),
            ("building", "Property managers", "One dependable team across multiple rental units."),
            ("star-outline", "Superhost hopefuls", "Cleanliness is the review category guests notice first."),
        ],
        "review": 0,
        "faqs": [
            ("Can you handle same-day turnovers?", "Yes. We work within your check-out and check-in times to have the property ready for the next guest."),
            ("Do you provide linens?", "We launder, change and stage the linens and towels you provide. Let us know your setup and we will build it into your checklist."),
            ("Will you follow my checklist?", "Absolutely. We use your house standards and photos so every guest sees the same polished space."),
        ],
    },
    {
        "slug": "add-on-services",
        "name": "Add-On Services",
        "nav": "Fridges, ovens, windows, laundry and more",
        "icon": "plus-square",
        "card": "Optional extras like inside refrigerators and ovens, interior windows, cabinets, dishes and laundry, added to any service.",
        "title": "Cleaning Add-On Services in Salt Lake City, UT",
        "desc": "Add inside fridge and oven cleaning, interior windows, cabinets, dishes, laundry and more to any H&G Cleaning Co. service in Salt Lake City.",
        "h1": "Add-On Services",
        "lead": "Customize any clean with the extras that matter most to you. From inside the fridge to a fresh load of laundry, simply add what you need when you book.",
        "facts": ["Add to any service", "Mix and match", "Priced upfront"],
        "chip": ("Tailored clean", "Pick what you need"),
        "hero": ("addon-kitchen-appliances", "Clean white kitchen with refrigerator, oven and cabinets"),
        "overview": [
            "Every home is different, and so is every to-do list. Our add-on services let you go beyond the standard checklist and take care of the tasks that are easy to put off.",
            "Add-ons can be included with a standard, deep, recurring, move-in or move-out cleaning. Simply select the extras you want when you book online and we will build them into your visit.",
        ],
        "included": [],
        "addons": [
            ("fridge", "Inside Refrigerator", "Shelves, drawers and walls emptied, wiped and sanitized."),
            ("oven", "Inside Oven", "Baked-on grease and residue removed from racks and interior."),
            ("window", "Interior Windows", "Glass, sills and tracks cleaned for clear, streak-free views."),
            ("cabinet", "Inside Cabinets", "Interior shelves and drawers wiped clean, ideal before a move."),
            ("dishes", "Dishes", "Dishes washed, dried and put away so the kitchen is fully reset."),
            ("shirt", "Laundry", "Wash, dry and fold one or more loads while we clean."),
            ("blinds", "Blinds", "Slats dusted and wiped to remove built-up dust."),
            ("wall", "Walls and Baseboards", "Spot cleaning of scuffs, marks and fingerprints on walls."),
        ],
        "gallery": [
            ("addon-laundry-room", "Neat laundry room with a washing machine and folded towels", "Laundry"),
            ("addon-interior-windows", "Cleaner washing the inside of a window", "Interior windows"),
            ("addon-inside-oven", "Clean oven interior", "Inside ovens"),
        ],
        "ideal": [
            ("sparkles", "Deep clean upgrades", "Make your deep clean even more complete with appliance interiors."),
            ("key", "Moving homes", "Inside cabinets, closets and windows for a full handover."),
            ("clock", "Time savers", "Hand off dishes and laundry so your day stays free."),
        ],
        "review": 3,
        "faqs": [
            ("Can I book an add-on by itself?", "Add-ons are designed to be paired with one of our cleaning services. Reach out and we will recommend the best fit for what you need."),
            ("How are add-ons priced?", "Each add-on is priced individually based on size and scope. You will see the price of each add-on when you book, so there are no surprises."),
            ("Can I add services on the day of my clean?", "If time allows, our team is happy to help. For guaranteed availability, add them when you book."),
        ],
    },
]

SERVICE_CARD_IMG = {
    "standard-cleaning": "standard-kitchen-island",
    "deep-cleaning": "deep-stovetop-detail",
    "recurring-cleaning": "recurring-made-bedroom",
    "move-in-move-out-cleaning": "move-moving-day-boxes",
    "commercial-cleaning": "commercial-office-glass",
    "post-construction-cleaning": "construction-dust-vacuum",
    "airbnb-vacation-rental-cleaning": "rental-guest-bedroom",
    "add-on-services": "addon-kitchen-appliances",
}

HOME_FAQS = [
    ("What areas do you serve?", f"We serve {BUSINESS['city']}, {BUSINESS['region_long']} and the surrounding areas, including Sandy, Draper, Murray, Holladay, Millcreek, South Jordan, West Jordan and more. Not sure if we cover your area? Just ask."),
    ("Are your cleaners background-checked?", "Yes. Every member of our team is background-checked before they ever step into a client's home or business."),
    ("Do you bring your own cleaning supplies?", "Yes. We arrive with professional-grade supplies and equipment. If you prefer specific products, we are happy to use them."),
    ("How do I get a price?", "Book online for instant pricing or give us a call. We will ask a few questions about your space and the service you need, then provide clear, upfront pricing."),
    ("Do you offer recurring cleaning?", "Yes. We offer weekly, bi-weekly and monthly plans with flexible scheduling and the same team whenever possible."),
    ("Do you clean both homes and businesses?", "We do. Residential cleaning is our focus, and we also provide commercial cleaning for offices, retail spaces and commercial properties."),
]

# --------------------------------------------------------------------------- shared layout
FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap"


def head(p, *, title, desc, path, image, schema, keywords=""):
    url = BUSINESS["domain"] + path
    img = f"{BUSINESS['domain']}/assets/img/{image}"
    kw = f'\n<meta name="keywords" content="{escape(keywords)}">' if keywords else ""
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>' for s in schema)
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">{kw}
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{escape(BUSINESS['name'])}">
<meta name="theme-color" content="#011729">
<meta name="format-detection" content="telephone=yes">
<meta name="geo.region" content="US-{BUSINESS['region']}">
<meta name="geo.placename" content="{BUSINESS['city']}">
<meta name="geo.position" content="{BUSINESS['lat']};{BUSINESS['lng']}">
<meta name="ICBM" content="{BUSINESS['lat']}, {BUSINESS['lng']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{escape(BUSINESS['name'])}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BUSINESS['domain']}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(BUSINESS['name'])}, {BUSINESS['tagline']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{BUSINESS['domain']}/assets/og-image.jpg">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{p}assets/favicon-16.png">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{p}css/styles.css">
<link rel="preload" as="image" href="{p}assets/img/{image}" fetchpriority="high">
{ld}
</head>
"""


def header(p, active, book="#book"):
    def cur(slug):
        return ' aria-current="page"' if active == slug else ""

    drop = "\n".join(
        f'<a href="{p}services/{s["slug"]}/"{cur(s["slug"])}><span class="dropdown__icon">{icon(s["icon"])}</span>'
        f'<span><strong>{escape(s["name"])}</strong><span class="desc">{escape(s["nav"])}</span></span></a>'
        for s in SERVICES
    )
    mob = "\n".join(f'<li><a href="{p}services/{s["slug"]}/"{cur(s["slug"])}>{escape(s["name"])}</a></li>' for s in SERVICES)
    home_cur = ' aria-current="page"' if active == "home" else ""
    services_open = " open" if active not in ("home", "") else ""
    return f"""<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="container">
    <a class="brand" href="{p}" aria-label="{escape(BUSINESS['name'])} home">
      <img src="{p}assets/img/logo.png" alt="{escape(BUSINESS['name'])} logo" width="640" height="229">
    </a>
    <nav class="nav" aria-label="Main">
      <a class="nav__link" href="{p}"{home_cur}>Home</a>
      <div class="nav__item">
        <button class="nav__link" type="button" aria-expanded="false" aria-haspopup="true">Services {icon("chev-down")}</button>
        <div class="dropdown">
{drop}
        </div>
      </div>
      <a class="nav__link" href="{p}#about">About</a>
      <a class="nav__link" href="{p}#reviews">Reviews</a>
      <a class="nav__link" href="{book}">Contact</a>
    </nav>
    <div class="header__actions">
      <a class="btn btn--primary header__cta" href="{book}">Book Now</a>
      <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">{icon("menu", "ico-open")}{icon("x", "ico-close")}</button>
    </div>
  </div>
</header>
<nav class="mobile-menu" id="mobile-menu" aria-label="Mobile">
  <a href="{p}">Home</a>
  <details{services_open}>
    <summary>Services {icon("chev-down")}</summary>
    <ul>
{mob}
    </ul>
  </details>
  <a href="{p}#about">About</a>
  <a href="{p}#reviews">Reviews</a>
  <a href="{p}#areas">Service Areas</a>
  <a href="{book}">Book and Contact</a>
  <div class="mobile-menu__cta">
    <a class="btn btn--primary btn--block" href="{book}">Book Now</a>
    <a class="btn btn--outline btn--block" href="tel:{BUSINESS['phone_href']}">{icon("phone")}Call {BUSINESS['phone']}</a>
  </div>
</nav>
"""


def footer(p, book="#book"):
    svc = "\n".join(f'<li><a href="{p}services/{s["slug"]}/">{escape(s["name"])}</a></li>' for s in SERVICES)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <img src="{p}assets/img/logo-white.png" alt="{escape(BUSINESS['name'])}" width="640" height="229" loading="lazy">
        <p>Reliable, high-quality residential and commercial cleaning for homeowners, families, professionals and businesses across {BUSINESS['area_label']}.</p>
        <div class="footer__badges"><span>Background-Checked</span><span>5-Star Rated</span><span>Locally Owned</span></div>
      </div>
      <div>
        <h3>Services</h3>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h3>Company</h3>
        <ul>
          <li><a href="{p}#about">About Us</a></li>
          <li><a href="{p}services/recurring-cleaning/">Recurring Plans</a></li>
          <li><a href="{p}#reviews">Reviews</a></li>
          <li><a href="{p}#areas">Service Areas</a></li>
          <li><a href="{p}#faq">FAQ</a></li>
          <li><a href="{book}">Book Online</a></li>
        </ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul class="footer__contact">
          <li>{icon("phone")}<a href="tel:{BUSINESS['phone_href']}">{BUSINESS['phone']}</a></li>
          <li>{icon("mail")}<a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a></li>
          <li>{icon("pin")}<span>{BUSINESS['city']}, {BUSINESS['region_long']} and surrounding areas</span></li>
          <li>{icon("clock")}<span>{BUSINESS['hours']}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span data-year>2026</span> {escape(BUSINESS['name'])} All rights reserved.</span>
      <span>{BUSINESS['tagline']}. Professional cleaning in {BUSINESS['city']}, {BUSINESS['region']}.</span>
    </div>
  </div>
</footer>
<div class="mobile-bar">
  <a class="btn btn--outline" href="tel:{BUSINESS['phone_href']}">{icon("phone")}Call</a>
  <a class="btn btn--primary" href="{book}">Book Now</a>
</div>
<script src="{p}js/main.js" defer></script>
</body>
</html>
"""


BOOKING_URL = "https://hgcleaningco.bookingkoala.com/booknow?embed=true"


def booking_section(eyebrow, heading, lead, soft=True):
    # BookingKoala's embed.js is intentionally not loaded: a fixed-height iframe with
    # internal scrolling keeps BK's modals inside the visible viewport on all devices.
    return f"""<section class="section{' section--soft' if soft else ''} booking" id="book">
  <div class="container">
    <div class="booking__head">
      <div class="section-head">
        <span class="eyebrow">{escape(eyebrow)}</span>
        <h2>{escape(heading)}</h2>
        <p>{escape(lead)}</p>
      </div>
      <div class="booking__contact">
        <a href="tel:{BUSINESS['phone_href']}"><span class="ico">{icon('phone')}</span><span><small>Prefer to call?</small><strong>{BUSINESS['phone']}</strong></span></a>
        <a href="mailto:{BUSINESS['email']}"><span class="ico">{icon('mail')}</span><span><small>Email</small><strong>{BUSINESS['email']}</strong></span></a>
      </div>
    </div>
    <div class="booking__frame">
      <iframe src="{BOOKING_URL}" title="Book a cleaning with {escape(BUSINESS['name'])}" width="100%" scrolling="yes" loading="lazy" allow="payment"></iframe>
    </div>
  </div>
</section>"""


def faq_block(items):
    return "\n".join(
        f'<details><summary>{escape(q)}<span class="pm">{icon("plus")}</span></summary><div><p>{escape(a)}</p></div></details>'
        for q, a in items
    )


def faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }


def business_schema():
    d = BUSINESS["domain"]
    return {
        "@context": "https://schema.org",
        "@type": "HouseCleaningService",
        "@id": f"{d}/#business",
        "name": BUSINESS["name"],
        "slogan": BUSINESS["tagline"],
        "description": "Reliable, high-quality residential and commercial cleaning services in Salt Lake City, Utah and surrounding areas.",
        "url": f"{d}/",
        "logo": f"{d}/assets/img/logo.png",
        "image": f"{d}/assets/og-image.jpg",
        "telephone": BUSINESS["phone_href"],
        "email": BUSINESS["email"],
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": BUSINESS["city"], "addressRegion": BUSINESS["region"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": BUSINESS["lat"], "longitude": BUSINESS["lng"]},
        "areaServed": [{"@type": "City", "name": f"{a}, {BUSINESS['region']}"} for a in AREAS],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "18:00"}],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "reviewCount": str(len(REVIEWS))},
        "review": [{"@type": "Review", "author": {"@type": "Person", "name": n}, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "reviewBody": t} for n, _, t in REVIEWS],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Cleaning Services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{d}/services/{s['slug']}/"}} for s in SERVICES],
        },
    }


def initials(name):
    return "".join(w[0] for w in name.replace(".", "").split()[:2])


def review_card(r):
    n, label, t = r
    return f"""<article class="review">
        {stars()}
        <blockquote>&ldquo;{escape(t)}&rdquo;</blockquote>
        <footer><span class="review__avatar">{initials(n)}</span><span><strong>{escape(n)}</strong><span>{escape(label)}</span></span></footer>
      </article>"""


# --------------------------------------------------------------------------- home
HOME_REVIEWS = [REVIEWS[0], REVIEWS[2], REVIEWS[3]]


def build_home():
    p = ""
    tiles = "\n".join(
        f"""<a class="tile" href="services/{s['slug']}/">
        <div class="tile__media"><img src="assets/img/{SERVICE_CARD_IMG[s['slug']]}.webp" alt="{escape(s['name'])} by {escape(BUSINESS['name'])}" width="800" height="600" loading="lazy"></div>
        <h3>{escape(s['name'])} {icon('arrow')}</h3>
        <p>{escape(s['nav'])}</p>
      </a>"""
        for s in SERVICES
    )
    areas = "\n".join(f"<li>{a}</li>" for a in AREAS)
    reviews = "\n".join(review_card(r) for r in HOME_REVIEWS)
    map_q = f"{BUSINESS['city']}, {BUSINESS['region']}".replace(" ", "+")
    schema = [
        business_schema(),
        {"@context": "https://schema.org", "@type": "WebSite", "name": BUSINESS["name"], "url": BUSINESS["domain"] + "/"},
        faq_schema(HOME_FAQS),
    ]
    html = head(
        p,
        title=f"{BUSINESS['name']} | House and Commercial Cleaning in Salt Lake City, UT",
        desc="H&G Cleaning Co. provides reliable residential and commercial cleaning in Salt Lake City and surrounding areas. Background-checked, 5-star rated and locally owned. Book online today.",
        path="/",
        image="bright-clean-living-room.webp",
        keywords="cleaning service Salt Lake City, house cleaning Salt Lake City, maid service Salt Lake City, deep cleaning Utah, move out cleaning Salt Lake City, commercial cleaning Salt Lake City, Airbnb cleaning Salt Lake City, recurring house cleaning",
        schema=schema,
    ) + header(p, "home") + f"""<main id="main">

<section class="hero-split">
  <div class="hero-split__content">
    <span class="eyebrow">{BUSINESS['tagline']} in {BUSINESS['city']}</span>
    <h1>Professional cleaning you can count on.</h1>
    <p class="lead">Reliable, detail-focused cleaning for homes and businesses, from a background-checked and locally owned team.</p>
    <div class="hero-split__actions">
      <a class="btn btn--primary" href="#book">Book Now {icon('arrow')}</a>
      <a class="btn btn--outline" href="#services">View Services</a>
    </div>
    <ul class="hero-split__trust">
      <li>{stars()}<span>5-star rated</span></li>
      <li>{icon('shield')}<span>Background-checked</span></li>
      <li>{icon('home')}<span>Locally owned</span></li>
    </ul>
  </div>
  <div class="hero-split__media">
    <img src="assets/img/bright-clean-living-room.webp" alt="Bright, spotless living room after a professional cleaning" width="1400" height="933" fetchpriority="high">
    <div class="book-panel">
      <span class="book-panel__label">Online booking</span>
      <h2>Book your clean in minutes</h2>
      <p>Choose your service, pick a date and see your price instantly.</p>
      <a class="btn btn--primary btn--block" href="#book">Book Now {icon('arrow')}</a>
      <a class="book-panel__call" href="tel:{BUSINESS['phone_href']}">or call {BUSINESS['phone']}</a>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">Our Services</span>
      <h2>How we can help</h2>
      <p>Residential and commercial cleaning, delivered with the same care and attention to detail.</p>
    </div>
    <div class="tiles">
{tiles}
    </div>
  </div>
</section>

<section class="section section--soft" id="about">
  <div class="container split">
    <div class="split__media">
      <div class="about-media"><img src="assets/img/team-cleaning-living-room.webp" alt="H&amp;G Cleaning Co. team cleaning a bright living room" width="1024" height="574" loading="lazy"></div>
    </div>
    <div class="split__content">
      <span class="eyebrow">About Us</span>
      <h2>A dependable team you can trust in your space</h2>
      <p>We serve busy homeowners, families, professionals and businesses who want a cleaning team they can rely on. We show up on time, communicate clearly and take pride in the details.</p>
      <ul class="simple-checks">
        <li>{icon('check')}Background-checked professionals</li>
        <li>{icon('check')}Consistent, checklist-driven results</li>
        <li>{icon('check')}Simple online booking with upfront pricing</li>
      </ul>
      <a class="text-link" href="#book">Book your clean {icon('arrow')}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">How It Works</span>
      <h2>Three simple steps</h2>
    </div>
    <ol class="steps-inline">
      <li><span class="steps-inline__num">1</span><h3>Book online</h3><p>Choose your service and see your price right away.</p></li>
      <li><span class="steps-inline__num">2</span><h3>We clean</h3><p>Our team arrives on time with everything needed.</p></li>
      <li><span class="steps-inline__num">3</span><h3>You relax</h3><p>Come home to a fresh, spotless space.</p></li>
    </ol>
  </div>
</section>

<section class="section section--soft" id="reviews">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">Client Reviews</span>
      <h2>Loved by our clients</h2>
      <p class="rating-line">{stars()}<strong>5.0</strong> average rating</p>
    </div>
    <div class="reviews">
{reviews}
    </div>
  </div>
</section>

<section class="section section--navy" id="areas">
  <div class="container areas">
    <div>
      <span class="eyebrow eyebrow--light">Service Areas</span>
      <h2>Serving Salt Lake City and nearby</h2>
      <p>A locally owned team cleaning homes and businesses across the Salt Lake Valley. Not sure if we cover your area? Just ask.</p>
      <ul class="area-chips">
{areas}
      </ul>
    </div>
    <div class="areas__map">
      <iframe title="Map of the {BUSINESS['city']} service area" src="https://www.google.com/maps?q={map_q}&amp;z=10&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">FAQ</span>
      <h2>Common questions</h2>
    </div>
    <div class="faq">
{faq_block(HOME_FAQS)}
    </div>
  </div>
</section>

{booking_section("Book Online", "Ready for a cleaner space?", "Choose your service, pick a date and see your price instantly. Booking takes just a few minutes.")}

</main>
""" + footer(p)
    write("index.html", html)


# --------------------------------------------------------------------------- service pages
def build_service(s):
    p = "../../"
    path = f"/services/{s['slug']}/"
    hero_img, hero_alt = s["hero"]
    facts = "".join(f"<li>{icon('check-circle')}{escape(f)}</li>" for f in s["facts"])
    overview = "\n".join(f"<p>{escape(x)}</p>" for x in s["overview"])
    gallery = "\n".join(
        f'<figure><img src="{p}assets/img/{img}.webp" alt="{escape(alt)}" width="1000" height="667" loading="lazy"><figcaption>{escape(cap)}</figcaption></figure>'
        for img, alt, cap in s["gallery"]
    )
    ideal = "\n".join(
        f'<div class="ideal__card"><span class="ico">{icon(ic)}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for ic, t, d in s["ideal"]
    )
    rv = REVIEWS[s["review"]]
    others = "\n".join(
        f'<a class="mini-card" href="../{o["slug"]}/"><img src="{p}assets/img/{SERVICE_CARD_IMG[o["slug"]]}.webp" alt="" width="64" height="64" loading="lazy"><span><strong>{escape(o["name"])}</strong><span>Learn more {icon("arrow")}</span></span></a>'
        for o in SERVICES if o["slug"] != s["slug"]
    )

    if s.get("addons"):
        addons = "\n".join(
            f'<div class="addon"><span class="ico">{icon(ic)}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for ic, t, d in s["addons"]
        )
        detail = f"""<section class="section">
  <div class="container">
    <div class="detail" style="margin-bottom:clamp(48px,6vw,72px)">
      <div>
        <span class="eyebrow">Overview</span>
        <h2>Go beyond the standard checklist</h2>
        {overview}
      </div>
      <div class="included">
        <h3>How add-ons work</h3>
        <p>Simple, flexible and priced upfront.</p>
        <ul>
          <li>{icon('check')}Select any add-ons when you book online</li>
          <li>{icon('check')}Pair them with any residential cleaning service</li>
          <li>{icon('check')}Each add-on is priced clearly before you confirm</li>
          <li>{icon('check')}Completed during the same visit as your clean</li>
        </ul>
      </div>
    </div>
    <div class="section-head">
      <span class="eyebrow">Available Add-Ons</span>
      <h2>Popular extras</h2>
    </div>
    <div class="addon-grid">
{addons}
    </div>
  </div>
</section>"""
    else:
        groups = "\n".join(
            f'<div class="included__group"><h4>{escape(g)}</h4><ul>' + "".join(f"<li>{icon('check')}{escape(i)}</li>" for i in items) + "</ul></div>"
            for g, items in s["included"]
        )
        detail = f"""<section class="section">
  <div class="container detail">
    <div>
      <span class="eyebrow">Overview</span>
      <h2>What to expect from your {escape(s['name'].lower().replace('airbnb', 'Airbnb'))}</h2>
      {overview}
      <ul class="check-list">
        <li><span class="check-list__icon">{icon('check')}</span><div><strong>Background-checked team</strong><span class="d">Trusted professionals in your space.</span></div></li>
        <li><span class="check-list__icon">{icon('check')}</span><div><strong>Professional supplies included</strong><span class="d">We arrive with everything needed to do the job right.</span></div></li>
        <li><span class="check-list__icon">{icon('check')}</span><div><strong>Clear, upfront pricing</strong><span class="d">Know exactly what you are paying before we start.</span></div></li>
      </ul>
      <a class="btn btn--navy" href="#book">Book Now {icon('arrow')}</a>
    </div>
    <div class="included">
      <h3>What's included</h3>
      <p>A clear checklist so you always know what is covered.</p>
      {groups}
    </div>
  </div>
</section>"""

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BUSINESS["domain"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": BUSINESS["domain"] + "/#services"},
            {"@type": "ListItem", "position": 3, "name": s["name"], "item": BUSINESS["domain"] + path},
        ],
    }
    service_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["name"],
        "serviceType": s["name"],
        "description": s["desc"],
        "url": BUSINESS["domain"] + path,
        "image": f"{BUSINESS['domain']}/assets/img/{hero_img}.webp",
        "provider": {"@type": "HouseCleaningService", "@id": f"{BUSINESS['domain']}/#business", "name": BUSINESS["name"], "telephone": BUSINESS["phone_href"], "url": BUSINESS["domain"] + "/"},
        "areaServed": [{"@type": "City", "name": f"{a}, {BUSINESS['region']}"} for a in AREAS],
    }

    chip_t, chip_s = s["chip"]
    html = head(
        p,
        title=f"{s['title']} | {BUSINESS['name']}",
        desc=s["desc"],
        path=path,
        image=f"{hero_img}.webp",
        keywords=f"{s['name'].lower()} Salt Lake City, {s['name'].lower()} Utah, {s['name'].lower()} near me, {BUSINESS['name']}",
        schema=[service_ld, breadcrumb, faq_schema(s["faqs"])],
    ) + header(p, s["slug"]) + f"""<main id="main">

<section class="page-hero">
  <div class="container">
    <div>
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{p}">Home</a>{icon('chev-right')}<a href="{p}#services">Services</a>{icon('chev-right')}<span aria-current="page">{escape(s['name'])}</span></nav>
      <span class="eyebrow">{escape(BUSINESS['city'])} Cleaning Services</span>
      <h1>{escape(s['h1'])}</h1>
      <p class="lead">{escape(s['lead'])}</p>
      <div class="page-hero__actions">
        <a class="btn btn--primary" href="#book">Book Now {icon('arrow')}</a>
        <a class="btn btn--outline" href="tel:{BUSINESS['phone_href']}">{icon('phone')}{BUSINESS['phone']}</a>
      </div>
      <ul class="page-hero__facts">{facts}</ul>
    </div>
    <div class="page-hero__media">
      <img src="{p}assets/img/{hero_img}.webp" alt="{escape(hero_alt)}" width="1400" height="933" fetchpriority="high">
      <div class="page-hero__chip"><span class="ico">{icon(s['icon'])}</span><span><strong>{escape(chip_t)}</strong><span>{escape(chip_s)}</span></span></div>
    </div>
  </div>
</section>

{detail}

<section class="section section--soft" style="padding-top:clamp(56px,7vw,88px);padding-bottom:clamp(56px,7vw,88px)">
  <div class="container">
    <div class="gallery">
{gallery}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">Who It's For</span>
      <h2>Ideal for</h2>
    </div>
    <div class="ideal">
{ideal}
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="feature-quote">
      <div class="feature-quote__mark" aria-hidden="true">&ldquo;</div>
      <div>
        {stars()}
        <blockquote style="margin-top:18px">{escape(rv[2])}</blockquote>
        <cite><strong>{escape(rv[0])}</strong> {escape(rv[1])}</cite>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">How It Works</span>
      <h2>Booking is simple</h2>
    </div>
    <div class="steps">
      <div class="step"><div class="step__num">STEP 01</div><div class="step__icon">{icon('message')}</div><h3>Book online</h3><p>Select this service and share a few details about your space to see your price.</p></div>
      <div class="step"><div class="step__num">STEP 02</div><div class="step__icon">{icon('calendar')}</div><h3>Choose a time</h3><p>Pick the date that works for you. We confirm everything ahead of your visit.</p></div>
      <div class="step"><div class="step__num">STEP 03</div><div class="step__icon">{icon('smile')}</div><h3>Relax</h3><p>Our team arrives on time, follows the checklist and leaves your space spotless.</p></div>
    </div>
  </div>
</section>

{booking_section("Book Online", "Book your " + s['name'].lower().replace('airbnb', 'Airbnb'), "Select your service, choose a date and see your price instantly. It only takes a few minutes.")}

<section class="section" id="faq">
  <div class="container">
    <div class="section-head section-head--center">
      <span class="eyebrow">FAQ</span>
      <h2>{escape(s['name'])} questions</h2>
    </div>
    <div class="faq">
{faq_block(s['faqs'])}
    </div>
  </div>
</section>

<section class="section section--soft" style="padding-top:clamp(56px,7vw,88px);padding-bottom:clamp(56px,7vw,88px)">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Explore More</span>
      <h2>Other services</h2>
    </div>
    <div class="other-services">
{others}
    </div>
  </div>
</section>

</main>
""" + footer(p)
    write(f"services/{s['slug']}/index.html", html)


def build_404():
    p = "/"
    html = head(p, title=f"Page Not Found | {BUSINESS['name']}", desc="The page you are looking for could not be found.", path="/404", image="home-hero.webp", schema=[]).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">'
    ) + header(p, "", book="/#book") + f"""<main id="main">
<section class="notfound">
  <div class="container">
    <span class="eyebrow">Error 404</span>
    <h1>This page could not be found</h1>
    <p class="lead" style="max-width:520px;margin:0 auto 32px">The page may have moved. Head back home or explore our cleaning services.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap"><a class="btn btn--primary" href="/">Back to Home</a><a class="btn btn--outline" href="/#services">View Services</a></div>
  </div>
</section>
</main>
""" + footer(p, book="/#book")
    write("404.html", html)


def build_seo_files():
    d = BUSINESS["domain"]
    urls = [("/", "1.0", "weekly")] + [(f"/services/{s['slug']}/", "0.8", "monthly") for s in SERVICES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{d}{u}</loc><lastmod>2026-10-14</lastmod><changefreq>{f}</changefreq><priority>{pr}</priority></url>\n" for u, pr, f in urls
    ) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {d}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": BUSINESS["name"], "short_name": BUSINESS["short"], "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#011729",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=2) + "\n")


DASHES = re.compile("[\u2013\u2014\u2015\u2212]")


def write(rel, text):
    if DASHES.search(text):
        raise SystemExit(f"Dash character found in {rel}: {DASHES.search(text).group()!r}")
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", rel)


if __name__ == "__main__":
    build_home()
    for s in SERVICES:
        build_service(s)
    build_404()
    build_seo_files()
