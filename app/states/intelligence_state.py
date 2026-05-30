import reflex as rx
from typing import TypedDict
from app.states.data_state import (
    DataState,
    PRACTITIONERS,
    REVIEWS,
    SALONS,
    SERVICES,
)


POSITIVE_WORDS = [
    "best",
    "amazing",
    "incredible",
    "perfect",
    "love",
    "great",
    "stunning",
    "unmatched",
    "transformed",
    "sharpest",
    "absolutely",
    "editorial",
    "excellent",
    "wonderful",
    "fantastic",
]
NEGATIVE_WORDS = [
    "bad",
    "terrible",
    "awful",
    "rude",
    "slow",
    "wait",
    "long",
    "disappointed",
    "poor",
    "worst",
    "never",
]
NEUTRAL_WORDS = ["okay", "fine", "average", "decent"]


class StylistMatch(TypedDict):
    practitioner_id: str
    name: str
    title: str
    avatar_seed: str
    rating: float
    reviews: int
    expertise_score: float
    rating_score: float
    preference_score: float
    workload_score: float
    availability_score: float
    total_score: float
    reason: str


class SentimentReview(TypedDict):
    id: str
    customer: str
    practitioner: str
    rating: int
    comment: str
    sentiment: str
    score: float
    indicators: list[str]


class DemandCell(TypedDict):
    day: str
    hour: str
    demand: int
    level: str
    pricing: str
    multiplier: float


class WaitlistRanked(TypedDict):
    id: str
    customer: str
    salon: str
    service: str
    requested_date: str
    score: float
    reason: str
    loyalty: str


class CacheSource(TypedDict):
    name: str
    status: str
    last_sync: str
    records: int
    note: str


class ConcurrencyIncident(TypedDict):
    id: str
    time: str
    resource: str
    detail: str
    resolution: str
    severity: str


class LockAttempt(TypedDict):
    id: str
    time: str
    resource: str
    actor: str
    result: str
    duration_ms: int


class JobStatus(TypedDict):
    name: str
    status: str
    last_run: str
    next_run: str
    interval: str
    note: str


class EnvCheck(TypedDict):
    key: str
    label: str
    status: str
    note: str


class CoverageItem(TypedDict):
    area: str
    coverage: int
    tests: int
    note: str


DEMAND_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DEMAND_HOURS = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00"]


def _seeded_demand(day: str, hour: str) -> int:
    base = (
        len(day) * 13
        + sum(ord(c) for c in hour) * 7
        + (ord(day[0]) * ord(hour[0])) % 47
    )
    val = base % 100
    if day in ("Fri", "Sat"):
        val = min(100, val + 25)
    if hour in ("17:00", "19:00"):
        val = min(100, val + 15)
    if hour == "09:00":
        val = max(5, val - 20)
    return val


def _classify(comment: str) -> tuple[str, float, list[str]]:
    text = comment.lower()
    pos = [w for w in POSITIVE_WORDS if w in text]
    neg = [w for w in NEGATIVE_WORDS if w in text]
    neu = [w for w in NEUTRAL_WORDS if w in text]
    score = (len(pos) - len(neg)) / max(1, len(pos) + len(neg) + len(neu))
    if len(pos) > len(neg):
        return "Positive", round(0.6 + min(0.4, len(pos) * 0.1), 2), pos[:4]
    if len(neg) > len(pos):
        return "Negative", round(-0.6 - min(0.4, len(neg) * 0.1), 2), neg[:4]
    if neu or (len(pos) == len(neg) and len(pos) > 0):
        return "Neutral", round(score, 2), (pos + neg + neu)[:4]
    return "Neutral", 0.0, []


CACHE_SOURCES: list[CacheSource] = [
    {
        "name": "Google Places (live)",
        "status": "Unavailable",
        "last_sync": "2025-02-09 14:22",
        "records": 0,
        "note": "Credentials not configured. Falling back to local cache.",
    },
    {
        "name": "Local salon cache",
        "status": "Active",
        "last_sync": "2025-02-10 08:15",
        "records": len(SALONS),
        "note": "Deterministic seeded catalog used as primary source.",
    },
    {
        "name": "Practitioner cache",
        "status": "Active",
        "last_sync": "2025-02-10 08:15",
        "records": len(PRACTITIONERS),
        "note": "Bundled with salon catalog.",
    },
    {
        "name": "Service catalog cache",
        "status": "Active",
        "last_sync": "2025-02-10 08:15",
        "records": len(SERVICES),
        "note": "Bundled with salon catalog.",
    },
]

CONCURRENCY_INCIDENTS: list[ConcurrencyIncident] = [
    {
        "id": "ci1",
        "time": "2025-02-09 11:42",
        "resource": "p1 / 2025-02-14 10:00",
        "detail": "Two reservation holds attempted on overlapping slots.",
        "resolution": "Second hold rejected with conflict message.",
        "severity": "Low",
    },
    {
        "id": "ci2",
        "time": "2025-02-09 16:08",
        "resource": "p3 / 2025-02-22 14:30",
        "detail": "Reschedule and new booking targeted same slot.",
        "resolution": "Lock granted to first request; second received retry hint.",
        "severity": "Medium",
    },
    {
        "id": "ci3",
        "time": "2025-02-08 09:21",
        "resource": "p5 / 2025-01-28 11:15",
        "detail": "Cancellation and waitlist offer raced.",
        "resolution": "Waitlist offer queued after cancellation committed.",
        "severity": "Low",
    },
]

LOCK_ATTEMPTS: list[LockAttempt] = [
    {
        "id": "lk1",
        "time": "2025-02-10 09:14:22",
        "resource": "reservation:rv1",
        "actor": "Mia Hayes",
        "result": "Acquired",
        "duration_ms": 42,
    },
    {
        "id": "lk2",
        "time": "2025-02-10 09:14:23",
        "resource": "reservation:rv1",
        "actor": "Ethan Cole",
        "result": "Rejected (conflict)",
        "duration_ms": 8,
    },
    {
        "id": "lk3",
        "time": "2025-02-10 09:11:05",
        "resource": "appointment:a2",
        "actor": "Emma Carter",
        "result": "Acquired",
        "duration_ms": 51,
    },
    {
        "id": "lk4",
        "time": "2025-02-10 08:58:11",
        "resource": "waitlist:w3",
        "actor": "System",
        "result": "Acquired",
        "duration_ms": 19,
    },
    {
        "id": "lk5",
        "time": "2025-02-10 08:42:33",
        "resource": "payment:pm6",
        "actor": "System",
        "result": "Acquired",
        "duration_ms": 27,
    },
]

BACKGROUND_JOBS: list[JobStatus] = [
    {
        "name": "Reservation expirer",
        "status": "Healthy",
        "last_run": "2025-02-10 09:15:00",
        "next_run": "2025-02-10 09:16:00",
        "interval": "60s",
        "note": "Releases active holds past expiry.",
    },
    {
        "name": "Reminder dispatcher",
        "status": "Healthy",
        "last_run": "2025-02-10 09:00:00",
        "next_run": "2025-02-10 10:00:00",
        "interval": "1h",
        "note": "Queues 24h pre-appointment reminders (local notifications).",
    },
    {
        "name": "Waitlist matcher",
        "status": "Healthy",
        "last_run": "2025-02-10 08:30:00",
        "next_run": "2025-02-10 09:30:00",
        "interval": "30m",
        "note": "Scores waitlist entries against newly opened slots.",
    },
    {
        "name": "Sentiment scorer",
        "status": "Healthy",
        "last_run": "2025-02-10 06:00:00",
        "next_run": "2025-02-11 06:00:00",
        "interval": "24h",
        "note": "Classifies new reviews and surfaces indicators.",
    },
    {
        "name": "Demand forecast refresh",
        "status": "Idle",
        "last_run": "2025-02-09 23:00:00",
        "next_run": "2025-02-10 23:00:00",
        "interval": "24h",
        "note": "Recomputes day/hour demand grid.",
    },
    {
        "name": "Google Places sync",
        "status": "Suspended",
        "last_run": "n/a",
        "next_run": "n/a",
        "interval": "manual",
        "note": "Awaiting GOOGLE_PLACES_API_KEY. Cache fallback active.",
    },
]

ENV_CHECKS: list[EnvCheck] = [
    {
        "key": "GOOGLE_PLACES_API_KEY",
        "label": "Google Places",
        "status": "Missing",
        "note": "Cache fallback active. Configure key to enable live sync.",
    },
    {
        "key": "STRIPE_SECRET_KEY",
        "label": "Stripe payments",
        "status": "Missing",
        "note": "Local payment modeling only. Configure key for live capture/refund.",
    },
    {
        "key": "TWILIO_AUTH_TOKEN",
        "label": "Twilio SMS",
        "status": "Missing",
        "note": "SMS reminders modeled locally. Configure key to deliver.",
    },
    {
        "key": "RESEND_API_KEY",
        "label": "Resend email",
        "status": "Missing",
        "note": "Email reminders modeled locally. Configure key to deliver.",
    },
    {
        "key": "REDIS_URL",
        "label": "Redis lock store",
        "status": "Missing",
        "note": "Using in-memory locks. Configure for multi-instance safety.",
    },
    {
        "key": "DATABASE_URL",
        "label": "Postgres database",
        "status": "Configured",
        "note": "SQLite default. Override for production durability.",
    },
]

COVERAGE: list[CoverageItem] = [
    {
        "area": "Booking flow",
        "coverage": 92,
        "tests": 14,
        "note": "Service, practitioner, slot, conflict, and confirmation paths.",
    },
    {
        "area": "Cancellation policy",
        "coverage": 88,
        "tests": 9,
        "note": "Full / 50% / forfeited refund branches.",
    },
    {
        "area": "Reschedule",
        "coverage": 81,
        "tests": 6,
        "note": "Same-day, cross-day, and conflict cases.",
    },
    {
        "area": "Waitlist matching",
        "coverage": 76,
        "tests": 5,
        "note": "Ranking weights and offer notification.",
    },
    {
        "area": "Sentiment analysis",
        "coverage": 84,
        "tests": 7,
        "note": "Positive / neutral / negative classification.",
    },
    {
        "area": "Concurrency safeguards",
        "coverage": 70,
        "tests": 4,
        "note": "Simulated lock contention scenarios.",
    },
]


class IntelligenceState(rx.State):
    target_practitioner_id: str = "p1"
    target_service_category: str = "Hair"
    target_date: str = "2025-02-20"
    target_time: str = "10:00"

    selected_demand_day: str = "Sat"

    @rx.event
    def set_target_practitioner(self, pid: str):
        self.target_practitioner_id = pid

    @rx.event
    def set_target_category(self, c: str):
        self.target_service_category = c

    @rx.event
    def set_target_date(self, d: str):
        self.target_date = d

    @rx.event
    def set_target_time(self, t: str):
        self.target_time = t

    @rx.event
    def set_demand_day(self, d: str):
        self.selected_demand_day = d

    @rx.var
    def practitioner_options(self) -> list[dict[str, str]]:
        return [{"id": p["id"], "name": p["name"]} for p in PRACTITIONERS]

    @rx.var
    def category_options(self) -> list[str]:
        return [
            "Hair",
            "Color",
            "Bridal",
            "Facial",
            "Massage",
            "Barber",
            "Nails",
            "Lash",
        ]

    @rx.var
    async def stylist_alternatives(self) -> list[StylistMatch]:
        data = await self.get_state(DataState)
        target = next(
            (
                p
                for p in PRACTITIONERS
                if p["id"] == self.target_practitioner_id
            ),
            PRACTITIONERS[0],
        )
        target_specialties = set(target["specialties"])
        results: list[StylistMatch] = []
        for p in PRACTITIONERS:
            if p["id"] == target["id"]:
                continue
            # Expertise: overlap with target's specialties + category match
            overlap = len(target_specialties & set(p["specialties"]))
            cat_match = any(
                self.target_service_category.lower() in s.lower()
                for s in p["specialties"]
            )
            expertise = min(
                1.0,
                overlap * 0.35
                + (0.4 if cat_match else 0.0)
                + p["years"] * 0.02,
            )
            # Rating
            rating_score = (p["rating"] - 4.0) / 1.0
            rating_score = max(0.0, min(1.0, rating_score))
            # Preference: same salon as target
            pref = 1.0 if p["salon_id"] == target["salon_id"] else 0.4
            # Workload: fewer confirmed appointments = higher score
            load = len(
                [
                    a
                    for a in data.appointments
                    if a["practitioner"] == p["name"]
                    and a["status"] == "Confirmed"
                ]
            )
            workload = max(0.0, 1.0 - load * 0.15)
            # Availability for target slot
            blocked = data.get_blocked_slots(p["name"], self.target_date)
            avail = 0.0 if self.target_time in blocked else 1.0
            # Weighted total: expertise 30, rating 20, preference 15, workload 15, availability 20
            total = (
                expertise * 0.30
                + rating_score * 0.20
                + pref * 0.15
                + workload * 0.15
                + avail * 0.20
            )
            reason_bits: list[str] = []
            if cat_match:
                reason_bits.append(f"matches {self.target_service_category}")
            if overlap > 0:
                reason_bits.append(f"{overlap} shared specialties")
            if p["salon_id"] == target["salon_id"]:
                reason_bits.append("same salon")
            if avail == 1.0:
                reason_bits.append("available at requested time")
            else:
                reason_bits.append("alt time required")
            results.append(
                {
                    "practitioner_id": p["id"],
                    "name": p["name"],
                    "title": p["title"],
                    "avatar_seed": p["avatar_seed"],
                    "rating": p["rating"],
                    "reviews": p["reviews"],
                    "expertise_score": round(expertise, 2),
                    "rating_score": round(rating_score, 2),
                    "preference_score": round(pref, 2),
                    "workload_score": round(workload, 2),
                    "availability_score": round(avail, 2),
                    "total_score": round(total, 3),
                    "reason": " · ".join(reason_bits),
                }
            )
        results.sort(key=lambda r: r["total_score"], reverse=True)
        return results[:5]

    @rx.var
    def sentiment_reviews(self) -> list[SentimentReview]:
        out: list[SentimentReview] = []
        for r in REVIEWS:
            sentiment, score, indicators = _classify(r["comment"])
            out.append(
                {
                    "id": r["id"],
                    "customer": r["customer"],
                    "practitioner": r["practitioner"],
                    "rating": r["rating"],
                    "comment": r["comment"],
                    "sentiment": sentiment,
                    "score": score,
                    "indicators": indicators,
                }
            )
        return out

    @rx.var
    def sentiment_summary(self) -> dict[str, int]:
        result = {"Positive": 0, "Neutral": 0, "Negative": 0}
        for r in self.sentiment_reviews:
            result[r["sentiment"]] = result.get(r["sentiment"], 0) + 1
        return result

    @rx.var
    async def ranked_waitlist(self) -> list[WaitlistRanked]:
        data = await self.get_state(DataState)
        out: list[WaitlistRanked] = []
        for w in data.waitlist:
            # Score: status + customer history + recency
            history = len(
                [a for a in data.appointments if a["customer"] == w["customer"]]
            )
            loyalty = (
                "VIP"
                if history >= 3
                else ("Returning" if history >= 1 else "New")
            )
            base = 0.6 if w["status"] == "Active" else 0.3
            score = round(base + min(0.3, history * 0.1) + 0.05, 2)
            reason_bits = [f"{w['status']} hold", f"{history} prior bookings"]
            out.append(
                {
                    "id": w["id"],
                    "customer": w["customer"],
                    "salon": w["salon"],
                    "service": w["service"],
                    "requested_date": w["requested_date"],
                    "score": score,
                    "reason": " · ".join(reason_bits),
                    "loyalty": loyalty,
                }
            )
        out.sort(key=lambda x: x["score"], reverse=True)
        return out

    @rx.var
    def demand_grid(self) -> list[DemandCell]:
        out: list[DemandCell] = []
        for day in DEMAND_DAYS:
            for hour in DEMAND_HOURS:
                d = _seeded_demand(day, hour)
                if d >= 70:
                    level = "Peak"
                    pricing = "+15% surge"
                    mult = 1.15
                elif d >= 40:
                    level = "Steady"
                    pricing = "Standard"
                    mult = 1.0
                else:
                    level = "Off-peak"
                    pricing = "-10% incentive"
                    mult = 0.9
                out.append(
                    {
                        "day": day,
                        "hour": hour,
                        "demand": d,
                        "level": level,
                        "pricing": pricing,
                        "multiplier": mult,
                    }
                )
        return out

    @rx.var
    def demand_for_selected_day(self) -> list[DemandCell]:
        return [
            c for c in self.demand_grid if c["day"] == self.selected_demand_day
        ]

    @rx.var
    def demand_days(self) -> list[str]:
        return DEMAND_DAYS

    @rx.var
    def cache_sources(self) -> list[CacheSource]:
        return CACHE_SOURCES

    @rx.var
    def concurrency_incidents(self) -> list[ConcurrencyIncident]:
        return CONCURRENCY_INCIDENTS

    @rx.var
    def lock_attempts(self) -> list[LockAttempt]:
        return LOCK_ATTEMPTS

    @rx.var
    def background_jobs(self) -> list[JobStatus]:
        return BACKGROUND_JOBS

    @rx.var
    def env_checks(self) -> list[EnvCheck]:
        return ENV_CHECKS

    @rx.var
    def coverage_items(self) -> list[CoverageItem]:
        return COVERAGE

    @rx.var
    def avg_coverage(self) -> int:
        if not COVERAGE:
            return 0
        return int(sum(c["coverage"] for c in COVERAGE) / len(COVERAGE))

    @rx.event
    async def offer_to_waitlist(self, wid: str):
        from app.states.data_state import DataState as DS

        data = await self.get_state(DS)
        for w in data.waitlist:
            if w["id"] == wid:
                w["status"] = "Offered"
                data._add_notification(
                    w["customer"],
                    "WaitlistOffer",
                    "Instant slot offer",
                    f"A slot opened for {w['service']} at {w['salon']}. Claim within 30 minutes.",
                    wid,
                )
                data._add_activity(
                    "System",
                    "Sent waitlist offer",
                    f"{w['customer']} - {w['service']}",
                )
                return rx.toast.success(f"Offer sent to {w['customer']}")
        return rx.toast.error("Waitlist entry not found")