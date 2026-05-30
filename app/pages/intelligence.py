import reflex as rx
from app.components.layout import page_layout
from app.states.intelligence_state import (
    IntelligenceState,
    StylistMatch,
    SentimentReview,
    DemandCell,
    WaitlistRanked,
    CacheSource,
    ConcurrencyIncident,
    LockAttempt,
    JobStatus,
    EnvCheck,
    CoverageItem,
)


def section_header(title: str, subtitle: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-blue-600"),
            rx.el.h2(title, class_name="text-lg font-bold text-gray-900"),
            class_name="flex items-center gap-2 mb-1",
        ),
        rx.el.p(subtitle, class_name="text-sm text-gray-600"),
        class_name="mb-4",
    )


def stylist_match_card(m: StylistMatch) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={m['avatar_seed']}",
                class_name="h-12 w-12 rounded-full bg-gray-100 shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        m["name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        f"Score {m['total_score']:.2f}",
                        class_name="px-2 py-0.5 text-xs font-semibold bg-blue-600 text-white rounded-full w-fit",
                    ),
                    class_name="flex items-center gap-2 mb-0.5 flex-wrap",
                ),
                rx.el.p(m["title"], class_name="text-xs text-gray-500"),
                rx.el.p(m["reason"], class_name="text-xs text-gray-600 mt-1"),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex items-start gap-3 mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Expertise",
                    class_name="text-[10px] uppercase tracking-wide text-gray-500 font-semibold",
                ),
                rx.el.p(
                    f"{m['expertise_score']:.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Rating",
                    class_name="text-[10px] uppercase tracking-wide text-gray-500 font-semibold",
                ),
                rx.el.p(
                    f"{m['rating_score']:.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Preference",
                    class_name="text-[10px] uppercase tracking-wide text-gray-500 font-semibold",
                ),
                rx.el.p(
                    f"{m['preference_score']:.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Workload",
                    class_name="text-[10px] uppercase tracking-wide text-gray-500 font-semibold",
                ),
                rx.el.p(
                    f"{m['workload_score']:.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Available",
                    class_name="text-[10px] uppercase tracking-wide text-gray-500 font-semibold",
                ),
                rx.el.p(
                    f"{m['availability_score']:.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
            ),
            class_name="grid grid-cols-5 gap-2 pt-3 border-t border-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def practitioner_option(p: dict[str, str]) -> rx.Component:
    return rx.el.option(p["name"], value=p["id"])


def category_option(c: str) -> rx.Component:
    return rx.el.option(c, value=c)


def stylist_matching_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Intelligent stylist alternatives",
            "Weighted ranking across expertise, rating, customer preference, workload, and availability.",
            "users",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Preferred stylist",
                    class_name="block text-xs font-semibold text-gray-700 mb-1",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            IntelligenceState.practitioner_options,
                            practitioner_option,
                        ),
                        value=IntelligenceState.target_practitioner_id,
                        on_change=IntelligenceState.set_target_practitioner,
                        class_name="appearance-none w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm pr-8",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Service category",
                    class_name="block text-xs font-semibold text-gray-700 mb-1",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            IntelligenceState.category_options,
                            category_option,
                        ),
                        value=IntelligenceState.target_service_category,
                        on_change=IntelligenceState.set_target_category,
                        class_name="appearance-none w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm pr-8",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Date",
                    class_name="block text-xs font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="date",
                    default_value=IntelligenceState.target_date,
                    on_change=IntelligenceState.set_target_date.debounce(300),
                    class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Time",
                    class_name="block text-xs font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="time",
                    default_value=IntelligenceState.target_time,
                    on_change=IntelligenceState.set_target_time.debounce(300),
                    class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm",
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4 p-4 bg-white border border-gray-200 rounded-xl",
        ),
        rx.el.div(
            rx.foreach(
                IntelligenceState.stylist_alternatives, stylist_match_card
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
        ),
        class_name="mb-10",
    )


def sentiment_pill(sentiment: str) -> rx.Component:
    return rx.match(
        sentiment,
        (
            "Positive",
            rx.el.span(
                "Positive",
                class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
            ),
        ),
        (
            "Negative",
            rx.el.span(
                "Negative",
                class_name="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full w-fit",
            ),
        ),
        rx.el.span(
            "Neutral",
            class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-full w-fit",
        ),
    )


def indicator_chip(s: str) -> rx.Component:
    return rx.el.span(
        s,
        class_name="px-2 py-0.5 text-[10px] font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
    )


def review_sentiment_card(r: SentimentReview) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    r["customer"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"with {r['practitioner']}",
                    class_name="text-xs text-gray-500",
                ),
            ),
            rx.el.div(
                sentiment_pill(r["sentiment"]),
                rx.el.span(
                    f"{r['score']:.2f}",
                    class_name="text-xs font-mono text-gray-500",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-start justify-between mb-2",
        ),
        rx.el.p(r["comment"], class_name="text-sm text-gray-700 mb-2"),
        rx.cond(
            r["indicators"].length() > 0,
            rx.el.div(
                rx.el.span(
                    "Indicators:",
                    class_name="text-[10px] uppercase tracking-wide text-gray-500 font-semibold",
                ),
                rx.foreach(r["indicators"], indicator_chip),
                class_name="flex items-center gap-1.5 flex-wrap",
            ),
            rx.el.div(),
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def sentiment_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Review sentiment analysis",
            "Local positive/neutral/negative classification with extracted indicators.",
            "message-square-heart",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Positive",
                    class_name="text-xs font-semibold text-gray-600 mb-1",
                ),
                rx.el.p(
                    IntelligenceState.sentiment_summary["Positive"].to_string(),
                    class_name="text-2xl font-bold text-green-600",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Neutral",
                    class_name="text-xs font-semibold text-gray-600 mb-1",
                ),
                rx.el.p(
                    IntelligenceState.sentiment_summary["Neutral"].to_string(),
                    class_name="text-2xl font-bold text-gray-700",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Negative",
                    class_name="text-xs font-semibold text-gray-600 mb-1",
                ),
                rx.el.p(
                    IntelligenceState.sentiment_summary["Negative"].to_string(),
                    class_name="text-2xl font-bold text-red-600",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-4",
            ),
            class_name="grid grid-cols-3 gap-3 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                IntelligenceState.sentiment_reviews, review_sentiment_card
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
        ),
        class_name="mb-10",
    )


def waitlist_rank_row(w: WaitlistRanked) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    w["customer"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    w["loyalty"],
                    class_name="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full w-fit",
                ),
                class_name="flex items-center gap-2 mb-1",
            ),
            rx.el.p(
                f"{w['service']} · {w['salon']}",
                class_name="text-xs text-gray-600",
            ),
            rx.el.p(
                f"Requested {w['requested_date']} · {w['reason']}",
                class_name="text-xs text-gray-500 mt-1",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.span(
                f"Score {w['score']:.2f}",
                class_name="px-2 py-0.5 text-xs font-semibold bg-blue-600 text-white rounded-full w-fit",
            ),
            rx.el.button(
                "Send offer",
                on_click=lambda: IntelligenceState.offer_to_waitlist(w["id"]),
                class_name="px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-medium rounded-lg",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between gap-3 p-3 bg-white border border-gray-200 rounded-lg",
    )


def waitlist_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Waitlist optimization",
            "Ranked candidates for instant offers when slots open.",
            "list-plus",
        ),
        rx.el.div(
            rx.foreach(IntelligenceState.ranked_waitlist, waitlist_rank_row),
            class_name="space-y-2",
        ),
        class_name="mb-10",
    )


def demand_cell(c: DemandCell) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(c["hour"], class_name="text-xs text-gray-600"),
            rx.el.span(
                f"{c['demand']}%",
                class_name="text-xs font-bold text-gray-900",
            ),
            class_name="flex items-center justify-between mb-1.5",
        ),
        rx.el.div(
            rx.el.div(
                class_name=rx.match(
                    c["level"],
                    (
                        "Peak",
                        "h-1.5 rounded-full bg-red-500",
                    ),
                    (
                        "Steady",
                        "h-1.5 rounded-full bg-blue-500",
                    ),
                    "h-1.5 rounded-full bg-emerald-500",
                ),
                style={"width": c["demand"].to_string() + "%"},
            ),
            class_name="h-1.5 rounded-full bg-gray-100 overflow-hidden mb-2",
        ),
        rx.el.div(
            rx.el.span(
                c["level"],
                class_name=rx.match(
                    c["level"],
                    (
                        "Peak",
                        "px-2 py-0.5 text-[10px] font-medium bg-red-100 text-red-700 rounded-full w-fit",
                    ),
                    (
                        "Steady",
                        "px-2 py-0.5 text-[10px] font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                    ),
                    "px-2 py-0.5 text-[10px] font-medium bg-emerald-100 text-emerald-700 rounded-full w-fit",
                ),
            ),
            rx.el.span(
                c["pricing"],
                class_name="text-[10px] text-gray-600 font-medium",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white border border-gray-200 rounded-lg p-3",
    )


def demand_day_button(d: str) -> rx.Component:
    return rx.el.button(
        d,
        on_click=lambda: IntelligenceState.set_demand_day(d),
        class_name=rx.cond(
            IntelligenceState.selected_demand_day == d,
            "px-3 py-1.5 bg-blue-600 text-white text-xs font-semibold rounded-lg",
            "px-3 py-1.5 bg-white border border-gray-200 text-gray-700 text-xs font-medium rounded-lg hover:border-blue-300",
        ),
    )


def demand_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Demand prediction & dynamic pricing",
            "Day/hour demand grid with peak surge and off-peak incentives.",
            "trending-up",
        ),
        rx.el.div(
            rx.foreach(IntelligenceState.demand_days, demand_day_button),
            class_name="flex flex-wrap gap-2 mb-4",
        ),
        rx.el.div(
            rx.foreach(IntelligenceState.demand_for_selected_day, demand_cell),
            class_name="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3",
        ),
        class_name="mb-10",
    )


def cache_row(c: CacheSource) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    c["name"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.match(
                    c["status"],
                    (
                        "Active",
                        rx.el.span(
                            "Active",
                            class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                        ),
                    ),
                    (
                        "Unavailable",
                        rx.el.span(
                            "Unavailable",
                            class_name="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full w-fit",
                        ),
                    ),
                    rx.el.span(
                        c["status"],
                        class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-full w-fit",
                    ),
                ),
                class_name="flex items-center gap-2 mb-1 flex-wrap",
            ),
            rx.el.p(c["note"], class_name="text-xs text-gray-600"),
            rx.el.p(
                f"Last sync: {c['last_sync']} · {c['records']} records",
                class_name="text-xs text-gray-400 mt-1",
            ),
        ),
        class_name="p-3 bg-white border border-gray-200 rounded-lg",
    )


def cache_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Google Places cache fallback",
            "Live API unavailable - serving from local deterministic cache.",
            "database",
        ),
        rx.el.div(
            rx.foreach(IntelligenceState.cache_sources, cache_row),
            class_name="space-y-2",
        ),
        class_name="mb-10",
    )


def incident_row(i: ConcurrencyIncident) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    i["resource"],
                    class_name="text-sm font-mono font-semibold text-gray-900",
                ),
                rx.match(
                    i["severity"],
                    (
                        "High",
                        rx.el.span(
                            "High",
                            class_name="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full w-fit",
                        ),
                    ),
                    (
                        "Medium",
                        rx.el.span(
                            "Medium",
                            class_name="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full w-fit",
                        ),
                    ),
                    rx.el.span(
                        "Low",
                        class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                    ),
                ),
                class_name="flex items-center gap-2 mb-1 flex-wrap",
            ),
            rx.el.p(i["detail"], class_name="text-xs text-gray-700"),
            rx.el.p(
                f"Resolution: {i['resolution']}",
                class_name="text-xs text-gray-500 mt-1",
            ),
            rx.el.p(i["time"], class_name="text-xs text-gray-400 mt-0.5"),
        ),
        class_name="p-3 bg-white border border-gray-200 rounded-lg",
    )


def lock_row(l: LockAttempt) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            l["time"], class_name="px-3 py-2 text-xs font-mono text-gray-700"
        ),
        rx.el.td(
            l["resource"],
            class_name="px-3 py-2 text-xs font-mono text-gray-700",
        ),
        rx.el.td(l["actor"], class_name="px-3 py-2 text-xs text-gray-700"),
        rx.el.td(
            rx.cond(
                l["result"].contains("Acquired"),
                rx.el.span(
                    l["result"],
                    class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                ),
                rx.el.span(
                    l["result"],
                    class_name="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full w-fit",
                ),
            ),
            class_name="px-3 py-2",
        ),
        rx.el.td(
            f"{l['duration_ms']} ms",
            class_name="px-3 py-2 text-xs text-gray-700",
        ),
        class_name="border-t border-gray-100",
    )


def job_row(j: JobStatus) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    j["name"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.match(
                    j["status"],
                    (
                        "Healthy",
                        rx.el.span(
                            "Healthy",
                            class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                        ),
                    ),
                    (
                        "Idle",
                        rx.el.span(
                            "Idle",
                            class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                        ),
                    ),
                    (
                        "Suspended",
                        rx.el.span(
                            "Suspended",
                            class_name="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full w-fit",
                        ),
                    ),
                    rx.el.span(
                        j["status"],
                        class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-full w-fit",
                    ),
                ),
                class_name="flex items-center gap-2 mb-1",
            ),
            rx.el.p(j["note"], class_name="text-xs text-gray-600"),
            rx.el.p(
                f"Last: {j['last_run']} · Next: {j['next_run']} · Every {j['interval']}",
                class_name="text-xs text-gray-400 mt-1",
            ),
        ),
        class_name="p-3 bg-white border border-gray-200 rounded-lg",
    )


def env_row(e: EnvCheck) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                e["label"],
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p(e["key"], class_name="text-xs font-mono text-gray-500"),
        ),
        rx.el.div(
            rx.match(
                e["status"],
                (
                    "Configured",
                    rx.el.span(
                        "Configured",
                        class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                    ),
                ),
                (
                    "Missing",
                    rx.el.span(
                        "Missing",
                        class_name="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full w-fit",
                    ),
                ),
                rx.el.span(
                    e["status"],
                    class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-full w-fit",
                ),
            ),
            rx.el.p(
                e["note"], class_name="text-xs text-gray-500 mt-1 text-right"
            ),
            class_name="text-right",
        ),
        class_name="flex items-start justify-between gap-3 p-3 bg-white border border-gray-200 rounded-lg",
    )


def coverage_row(c: CoverageItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                c["area"], class_name="text-sm font-semibold text-gray-900"
            ),
            rx.el.span(
                f"{c['coverage']}%",
                class_name="text-sm font-bold text-blue-600",
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-1.5 rounded-full bg-blue-500",
                style={"width": c["coverage"].to_string() + "%"},
            ),
            class_name="h-1.5 rounded-full bg-gray-100 overflow-hidden mb-2",
        ),
        rx.el.p(
            f"{c['tests']} tests · {c['note']}",
            class_name="text-xs text-gray-600",
        ),
        class_name="p-3 bg-white border border-gray-200 rounded-lg",
    )


def architecture_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("layers", class_name="h-4 w-4 text-blue-600"),
            rx.el.h3(
                "Architecture notes",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.ul(
            rx.el.li(
                "Stateless Reflex frontend backed by typed state classes per concern.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Reservation holds use optimistic concurrency with conflict revalidation at confirm time.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Adjacent-slot blocking computed from service duration in 30-min buckets.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Local cache fallback for salon catalog when external Places API unavailable.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Background jobs (expirer, reminder, matcher) modeled in-process; production uses queue.",
                class_name="text-xs text-gray-700",
            ),
            class_name="list-disc pl-5 space-y-1",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def deployment_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("rocket", class_name="h-4 w-4 text-blue-600"),
            rx.el.h3(
                "Deployment guidance",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.ul(
            rx.el.li(
                "Run reflex export and serve frontend behind CDN.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Run backend on autoscaling container; configure Redis for cross-instance locks.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Provision Postgres for durable state; replace seeded lists.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Configure Stripe / Twilio / Resend keys to flip from local modeling to live delivery.",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Rotate Google Places API key into env to enable live salon discovery sync.",
                class_name="text-xs text-gray-700",
            ),
            class_name="list-disc pl-5 space-y-1",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def operations_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Operational readiness",
            "Concurrency, jobs, audit, environment, deployment, and test coverage.",
            "shield-check",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Concurrency incidents",
                    class_name="text-sm font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        IntelligenceState.concurrency_incidents, incident_row
                    ),
                    class_name="space-y-2 mb-6",
                ),
                rx.el.h3(
                    "Booking lock attempts",
                    class_name="text-sm font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Time",
                                    class_name="px-3 py-2 text-left text-[10px] font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Resource",
                                    class_name="px-3 py-2 text-left text-[10px] font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Actor",
                                    class_name="px-3 py-2 text-left text-[10px] font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Result",
                                    class_name="px-3 py-2 text-left text-[10px] font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Duration",
                                    class_name="px-3 py-2 text-left text-[10px] font-semibold text-gray-600 uppercase",
                                ),
                                class_name="bg-gray-50",
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                IntelligenceState.lock_attempts, lock_row
                            )
                        ),
                        class_name="table-auto w-full",
                    ),
                    class_name="bg-white border border-gray-200 rounded-xl overflow-hidden mb-6",
                ),
                rx.el.h3(
                    "Background jobs",
                    class_name="text-sm font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.foreach(IntelligenceState.background_jobs, job_row),
                    class_name="space-y-2",
                ),
                class_name="lg:col-span-2",
            ),
            rx.el.div(
                rx.el.h3(
                    "Environment readiness",
                    class_name="text-sm font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.foreach(IntelligenceState.env_checks, env_row),
                    class_name="space-y-2 mb-6",
                ),
                rx.el.h3(
                    "Test coverage",
                    class_name="text-sm font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Average",
                            class_name="text-xs font-semibold text-gray-700",
                        ),
                        rx.el.span(
                            f"{IntelligenceState.avg_coverage}%",
                            class_name="text-sm font-bold text-blue-600",
                        ),
                        class_name="flex items-center justify-between mb-3 px-1",
                    ),
                    rx.foreach(IntelligenceState.coverage_items, coverage_row),
                    class_name="space-y-2 mb-6",
                ),
                architecture_card(),
                rx.el.div(class_name="h-3"),
                deployment_card(),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
        class_name="mb-6",
    )


def intelligence_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h1(
                "Intelligence & Operations",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Stylist matching, sentiment, demand, cache fallback, and platform health.",
                class_name="text-gray-600 mt-1",
            ),
            class_name="mb-6",
        ),
        stylist_matching_section(),
        sentiment_section(),
        waitlist_section(),
        demand_section(),
        cache_section(),
        operations_section(),
    )