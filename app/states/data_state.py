import reflex as rx
import uuid
from datetime import datetime, timedelta
from typing import TypedDict
import logging


def slots_for(time: str, duration_min: int) -> list[str]:
    h, m = map(int, time.split(":"))
    start = h * 60 + m
    n = (duration_min + 29) // 30
    return [
        f"{(start + i * 30) // 60:02d}:{(start + i * 30) % 60:02d}"
        for i in range(n)
    ]


class Reservation(TypedDict):
    id: str
    customer: str
    salon_id: str
    salon_name: str
    practitioner: str
    service_id: str
    service_name: str
    date: str
    time: str
    duration_min: int
    price: float
    blocked_slots: list[str]
    status: str
    created_at: str
    expires_at: str


class NotificationItem(TypedDict):
    id: str
    customer: str
    type: str
    title: str
    body: str
    time: str
    read: bool
    related_id: str


class Service(TypedDict):
    id: str
    name: str
    duration_min: int
    price: float
    category: str
    description: str


class Practitioner(TypedDict):
    id: str
    name: str
    title: str
    salon_id: str
    rating: float
    reviews: int
    specialties: list[str]
    bio: str
    years: int
    avatar_seed: str


class Salon(TypedDict):
    id: str
    name: str
    address: str
    city: str
    rating: float
    reviews: int
    image_seed: str
    tags: list[str]
    description: str
    hours: str
    phone: str


class Appointment(TypedDict):
    id: str
    customer: str
    salon_id: str
    salon_name: str
    practitioner: str
    service: str
    date: str
    time: str
    duration_min: int
    price: float
    status: str
    payment_status: str


class Review(TypedDict):
    id: str
    customer: str
    salon_id: str
    practitioner: str
    rating: int
    comment: str
    date: str
    sentiment: str


class WaitlistEntry(TypedDict):
    id: str
    customer: str
    salon: str
    service: str
    requested_date: str
    status: str


class Payment(TypedDict):
    id: str
    customer: str
    amount: float
    type: str
    status: str
    date: str
    appointment_id: str


class ActivityLog(TypedDict):
    id: str
    actor: str
    action: str
    target: str
    time: str


SALONS: list[Salon] = [
    {
        "id": "s1",
        "name": "Lumiere Hair Studio",
        "address": "421 Bowery St",
        "city": "New York, NY",
        "rating": 4.8,
        "reviews": 312,
        "image_seed": "lumiere",
        "tags": ["Hair", "Color", "Bridal"],
        "description": "Modern luxury hair studio specializing in balayage, color correction, and bridal styling.",
        "hours": "Mon-Sat 9:00-19:00",
        "phone": "(212) 555-0142",
    },
    {
        "id": "s2",
        "name": "Maison Bleu Spa",
        "address": "88 Mission St",
        "city": "San Francisco, CA",
        "rating": 4.7,
        "reviews": 248,
        "image_seed": "maisonbleu",
        "tags": ["Spa", "Facial", "Massage"],
        "description": "Tranquil urban spa offering facials, deep tissue massage, and holistic wellness treatments.",
        "hours": "Tue-Sun 10:00-20:00",
        "phone": "(415) 555-0188",
    },
    {
        "id": "s3",
        "name": "The Barber Atelier",
        "address": "12 Shoreditch High St",
        "city": "Brooklyn, NY",
        "rating": 4.9,
        "reviews": 521,
        "image_seed": "atelier",
        "tags": ["Barber", "Beard", "Mens"],
        "description": "Classic barbershop craftsmanship with traditional hot towel shaves and precision cuts.",
        "hours": "Mon-Sat 8:00-20:00",
        "phone": "(718) 555-0167",
    },
    {
        "id": "s4",
        "name": "Aurora Nails & Beauty",
        "address": "55 Lincoln Rd",
        "city": "Miami, FL",
        "rating": 4.6,
        "reviews": 189,
        "image_seed": "aurora",
        "tags": ["Nails", "Beauty", "Lash"],
        "description": "Premium nail bar and beauty lounge with gel manicures, pedicures, and lash extensions.",
        "hours": "Mon-Sun 9:00-21:00",
        "phone": "(305) 555-0124",
    },
    {
        "id": "s5",
        "name": "Ember & Oak Grooming",
        "address": "204 W Loop",
        "city": "Chicago, IL",
        "rating": 4.8,
        "reviews": 276,
        "image_seed": "ember",
        "tags": ["Hair", "Barber", "Grooming"],
        "description": "Contemporary grooming lounge offering precision cuts, beard sculpting, and skincare for all.",
        "hours": "Mon-Sat 9:00-20:00",
        "phone": "(312) 555-0193",
    },
    {
        "id": "s6",
        "name": "Sienna Skin Lab",
        "address": "70 Abbot Kinney Blvd",
        "city": "Los Angeles, CA",
        "rating": 4.9,
        "reviews": 412,
        "image_seed": "sienna",
        "tags": ["Skin", "Facial", "Lash"],
        "description": "Award-winning skincare laboratory with medical-grade facials and lash artistry.",
        "hours": "Tue-Sun 10:00-19:00",
        "phone": "(310) 555-0177",
    },
]

PRACTITIONERS: list[Practitioner] = [
    {
        "id": "p1",
        "name": "Amelia Rivera",
        "title": "Senior Stylist",
        "salon_id": "s1",
        "rating": 4.9,
        "reviews": 142,
        "specialties": ["Balayage", "Color", "Bridal"],
        "bio": "12 years crafting signature color transformations.",
        "years": 12,
        "avatar_seed": "amelia",
    },
    {
        "id": "p2",
        "name": "Daniel Park",
        "title": "Master Colorist",
        "salon_id": "s1",
        "rating": 4.8,
        "reviews": 98,
        "specialties": ["Color Correction", "Highlights"],
        "bio": "Color specialist trained in Paris and Tokyo.",
        "years": 9,
        "avatar_seed": "daniel",
    },
    {
        "id": "p3",
        "name": "Sofia Marin",
        "title": "Lead Esthetician",
        "salon_id": "s2",
        "rating": 4.9,
        "reviews": 187,
        "specialties": ["HydraFacial", "Anti-aging"],
        "bio": "Licensed medical esthetician focused on results.",
        "years": 10,
        "avatar_seed": "sofia",
    },
    {
        "id": "p4",
        "name": "Marcus Vale",
        "title": "Massage Therapist",
        "salon_id": "s2",
        "rating": 4.7,
        "reviews": 134,
        "specialties": ["Deep Tissue", "Sports"],
        "bio": "Sports therapy and recovery specialist.",
        "years": 8,
        "avatar_seed": "marcus",
    },
    {
        "id": "p5",
        "name": "Henry Stone",
        "title": "Master Barber",
        "salon_id": "s3",
        "rating": 4.9,
        "reviews": 312,
        "specialties": ["Hot Towel Shave", "Fades"],
        "bio": "Old-school precision with modern flair.",
        "years": 15,
        "avatar_seed": "henry",
    },
    {
        "id": "p6",
        "name": "Lucia Bennett",
        "title": "Nail Artist",
        "salon_id": "s4",
        "rating": 4.8,
        "reviews": 156,
        "specialties": ["Gel Art", "Extensions"],
        "bio": "Nail artistry with editorial-level detail.",
        "years": 7,
        "avatar_seed": "lucia",
    },
    {
        "id": "p7",
        "name": "Elliot Reyes",
        "title": "Senior Barber",
        "salon_id": "s5",
        "rating": 4.8,
        "reviews": 201,
        "specialties": ["Scissor Cuts", "Beard"],
        "bio": "Modern grooming meets traditional craft.",
        "years": 11,
        "avatar_seed": "elliot",
    },
    {
        "id": "p8",
        "name": "Isabel Chen",
        "title": "Skincare Specialist",
        "salon_id": "s6",
        "rating": 5.0,
        "reviews": 267,
        "specialties": ["Microneedling", "Chemical Peels"],
        "bio": "Medical-grade results with gentle approach.",
        "years": 13,
        "avatar_seed": "isabel",
    },
]

SERVICES: list[Service] = [
    {
        "id": "sv1",
        "name": "Signature Haircut",
        "duration_min": 60,
        "price": 95.0,
        "category": "Hair",
        "description": "Consultation, shampoo, precision cut, and finish.",
    },
    {
        "id": "sv2",
        "name": "Full Balayage",
        "duration_min": 180,
        "price": 285.0,
        "category": "Color",
        "description": "Hand-painted highlights with toner and gloss.",
    },
    {
        "id": "sv3",
        "name": "Color Correction",
        "duration_min": 240,
        "price": 420.0,
        "category": "Color",
        "description": "Multi-step color repair with custom formula.",
    },
    {
        "id": "sv4",
        "name": "Bridal Trial",
        "duration_min": 90,
        "price": 175.0,
        "category": "Bridal",
        "description": "Bridal hair consultation and trial style.",
    },
    {
        "id": "sv5",
        "name": "HydraFacial Premium",
        "duration_min": 75,
        "price": 220.0,
        "category": "Facial",
        "description": "Deep cleanse, exfoliation, and serum infusion.",
    },
    {
        "id": "sv6",
        "name": "Deep Tissue Massage",
        "duration_min": 60,
        "price": 140.0,
        "category": "Massage",
        "description": "Targeted muscle release and recovery.",
    },
    {
        "id": "sv7",
        "name": "Classic Cut & Hot Towel",
        "duration_min": 45,
        "price": 65.0,
        "category": "Barber",
        "description": "Precision cut with traditional hot towel finish.",
    },
    {
        "id": "sv8",
        "name": "Beard Sculpt & Trim",
        "duration_min": 30,
        "price": 45.0,
        "category": "Barber",
        "description": "Beard shaping, trim, and conditioning.",
    },
    {
        "id": "sv9",
        "name": "Gel Manicure",
        "duration_min": 60,
        "price": 55.0,
        "category": "Nails",
        "description": "Long-lasting gel manicure with cuticle care.",
    },
    {
        "id": "sv10",
        "name": "Lash Extensions Full Set",
        "duration_min": 120,
        "price": 195.0,
        "category": "Lash",
        "description": "Custom lash extensions tailored to your eye shape.",
    },
]

APPOINTMENTS: list[Appointment] = [
    {
        "id": "a1",
        "customer": "Emma Carter",
        "salon_id": "s1",
        "salon_name": "Lumiere Hair Studio",
        "practitioner": "Amelia Rivera",
        "service": "Full Balayage",
        "date": "2025-02-14",
        "time": "10:00",
        "duration_min": 180,
        "price": 285.0,
        "status": "Confirmed",
        "payment_status": "Deposit Paid",
    },
    {
        "id": "a2",
        "customer": "Emma Carter",
        "salon_id": "s2",
        "salon_name": "Maison Bleu Spa",
        "practitioner": "Sofia Marin",
        "service": "HydraFacial Premium",
        "date": "2025-02-22",
        "time": "14:30",
        "duration_min": 75,
        "price": 220.0,
        "status": "Confirmed",
        "payment_status": "Pending",
    },
    {
        "id": "a3",
        "customer": "James Wong",
        "salon_id": "s3",
        "salon_name": "The Barber Atelier",
        "practitioner": "Henry Stone",
        "service": "Classic Cut & Hot Towel",
        "date": "2025-01-28",
        "time": "11:15",
        "duration_min": 45,
        "price": 65.0,
        "status": "Completed",
        "payment_status": "Paid",
    },
    {
        "id": "a4",
        "customer": "Olivia Brooks",
        "salon_id": "s1",
        "salon_name": "Lumiere Hair Studio",
        "practitioner": "Daniel Park",
        "service": "Color Correction",
        "date": "2025-02-08",
        "time": "09:00",
        "duration_min": 240,
        "price": 420.0,
        "status": "Confirmed",
        "payment_status": "Paid",
    },
    {
        "id": "a5",
        "customer": "Noah Patel",
        "salon_id": "s5",
        "salon_name": "Ember & Oak Grooming",
        "practitioner": "Elliot Reyes",
        "service": "Beard Sculpt & Trim",
        "date": "2025-02-03",
        "time": "16:00",
        "duration_min": 30,
        "price": 45.0,
        "status": "Cancelled",
        "payment_status": "Refunded",
    },
    {
        "id": "a6",
        "customer": "Ava Lopez",
        "salon_id": "s4",
        "salon_name": "Aurora Nails & Beauty",
        "practitioner": "Lucia Bennett",
        "service": "Gel Manicure",
        "date": "2025-02-11",
        "time": "13:00",
        "duration_min": 60,
        "price": 55.0,
        "status": "Confirmed",
        "payment_status": "Paid",
    },
    {
        "id": "a7",
        "customer": "Liam Foster",
        "salon_id": "s6",
        "salon_name": "Sienna Skin Lab",
        "practitioner": "Isabel Chen",
        "service": "HydraFacial Premium",
        "date": "2025-02-19",
        "time": "11:00",
        "duration_min": 75,
        "price": 220.0,
        "status": "Confirmed",
        "payment_status": "Deposit Paid",
    },
    {
        "id": "a8",
        "customer": "Sophia Wright",
        "salon_id": "s2",
        "salon_name": "Maison Bleu Spa",
        "practitioner": "Marcus Vale",
        "service": "Deep Tissue Massage",
        "date": "2025-01-30",
        "time": "17:30",
        "duration_min": 60,
        "price": 140.0,
        "status": "Completed",
        "payment_status": "Paid",
    },
]

REVIEWS: list[Review] = [
    {
        "id": "r1",
        "customer": "Emma C.",
        "salon_id": "s1",
        "practitioner": "Amelia Rivera",
        "rating": 5,
        "comment": "Amelia transformed my color completely. Best balayage I've ever had.",
        "date": "2025-01-12",
        "sentiment": "Positive",
    },
    {
        "id": "r2",
        "customer": "James W.",
        "salon_id": "s3",
        "practitioner": "Henry Stone",
        "rating": 5,
        "comment": "Old-school perfection. The hot towel shave is unmatched.",
        "date": "2025-01-28",
        "sentiment": "Positive",
    },
    {
        "id": "r3",
        "customer": "Sophia W.",
        "salon_id": "s2",
        "practitioner": "Marcus Vale",
        "rating": 5,
        "comment": "Marcus knew exactly what my back needed. Absolutely incredible.",
        "date": "2025-01-30",
        "sentiment": "Positive",
    },
    {
        "id": "r4",
        "customer": "Olivia B.",
        "salon_id": "s1",
        "practitioner": "Daniel Park",
        "rating": 4,
        "comment": "Great results although the wait was a bit long.",
        "date": "2025-01-15",
        "sentiment": "Mixed",
    },
    {
        "id": "r5",
        "customer": "Noah P.",
        "salon_id": "s5",
        "practitioner": "Elliot Reyes",
        "rating": 5,
        "comment": "Sharpest beard sculpt in Chicago. Booking again next month.",
        "date": "2025-01-22",
        "sentiment": "Positive",
    },
    {
        "id": "r6",
        "customer": "Ava L.",
        "salon_id": "s4",
        "practitioner": "Lucia Bennett",
        "rating": 5,
        "comment": "Lucia's nail art is editorial-level. Stunning work.",
        "date": "2025-02-01",
        "sentiment": "Positive",
    },
]

WAITLIST: list[WaitlistEntry] = [
    {
        "id": "w1",
        "customer": "Mia Hayes",
        "salon": "Lumiere Hair Studio",
        "service": "Full Balayage",
        "requested_date": "2025-02-15",
        "status": "Active",
    },
    {
        "id": "w2",
        "customer": "Ethan Cole",
        "salon": "The Barber Atelier",
        "service": "Classic Cut & Hot Towel",
        "requested_date": "2025-02-09",
        "status": "Active",
    },
    {
        "id": "w3",
        "customer": "Zoe Lin",
        "salon": "Sienna Skin Lab",
        "service": "HydraFacial Premium",
        "requested_date": "2025-02-12",
        "status": "Offered",
    },
]

PAYMENTS: list[Payment] = [
    {
        "id": "pm1",
        "customer": "Emma Carter",
        "amount": 85.0,
        "type": "Deposit",
        "status": "Captured",
        "date": "2025-01-22",
        "appointment_id": "a1",
    },
    {
        "id": "pm2",
        "customer": "Olivia Brooks",
        "amount": 420.0,
        "type": "Full Payment",
        "status": "Captured",
        "date": "2025-01-25",
        "appointment_id": "a4",
    },
    {
        "id": "pm3",
        "customer": "James Wong",
        "amount": 65.0,
        "type": "Full Payment",
        "status": "Captured",
        "date": "2025-01-28",
        "appointment_id": "a3",
    },
    {
        "id": "pm4",
        "customer": "Noah Patel",
        "amount": 45.0,
        "type": "Refund",
        "status": "Refunded",
        "date": "2025-02-02",
        "appointment_id": "a5",
    },
    {
        "id": "pm5",
        "customer": "Ava Lopez",
        "amount": 55.0,
        "type": "Full Payment",
        "status": "Captured",
        "date": "2025-02-04",
        "appointment_id": "a6",
    },
    {
        "id": "pm6",
        "customer": "Liam Foster",
        "amount": 66.0,
        "type": "Deposit",
        "status": "Captured",
        "date": "2025-02-05",
        "appointment_id": "a7",
    },
    {
        "id": "pm7",
        "customer": "Sophia Wright",
        "amount": 140.0,
        "type": "Full Payment",
        "status": "Captured",
        "date": "2025-01-30",
        "appointment_id": "a8",
    },
]

ACTIVITY: list[ActivityLog] = [
    {
        "id": "ac1",
        "actor": "Emma Carter",
        "action": "Booked appointment",
        "target": "Full Balayage @ Lumiere",
        "time": "2 hours ago",
    },
    {
        "id": "ac2",
        "actor": "Manager Riley",
        "action": "Updated practitioner schedule",
        "target": "Amelia Rivera",
        "time": "4 hours ago",
    },
    {
        "id": "ac3",
        "actor": "Admin",
        "action": "Approved new salon",
        "target": "Sienna Skin Lab",
        "time": "1 day ago",
    },
    {
        "id": "ac4",
        "actor": "Noah Patel",
        "action": "Cancelled appointment",
        "target": "Beard Sculpt",
        "time": "1 day ago",
    },
    {
        "id": "ac5",
        "actor": "System",
        "action": "Refund processed",
        "target": "$45.00 to Noah Patel",
        "time": "1 day ago",
    },
    {
        "id": "ac6",
        "actor": "Olivia Brooks",
        "action": "Left review",
        "target": "5 stars - Daniel Park",
        "time": "2 days ago",
    },
]


RESERVATIONS_SEED: list[Reservation] = [
    {
        "id": "rv1",
        "customer": "Mia Hayes",
        "salon_id": "s1",
        "salon_name": "Lumiere Hair Studio",
        "practitioner": "Amelia Rivera",
        "service_id": "sv2",
        "service_name": "Full Balayage",
        "date": "2025-02-25",
        "time": "10:00",
        "duration_min": 180,
        "price": 285.0,
        "blocked_slots": [
            "10:00",
            "10:30",
            "11:00",
            "11:30",
            "12:00",
            "12:30",
        ],
        "status": "Active",
        "created_at": "2025-02-10 09:30",
        "expires_at": (datetime.now() + timedelta(minutes=8)).strftime(
            "%Y-%m-%d %H:%M"
        ),
    },
    {
        "id": "rv2",
        "customer": "Ethan Cole",
        "salon_id": "s3",
        "salon_name": "The Barber Atelier",
        "practitioner": "Henry Stone",
        "service_id": "sv7",
        "service_name": "Classic Cut & Hot Towel",
        "date": "2025-02-20",
        "time": "14:00",
        "duration_min": 45,
        "price": 65.0,
        "blocked_slots": ["14:00", "14:30"],
        "status": "Confirmed",
        "created_at": "2025-02-09 11:15",
        "expires_at": "2025-02-09 11:25",
    },
    {
        "id": "rv3",
        "customer": "Zoe Lin",
        "salon_id": "s6",
        "salon_name": "Sienna Skin Lab",
        "practitioner": "Isabel Chen",
        "service_id": "sv5",
        "service_name": "HydraFacial Premium",
        "date": "2025-02-12",
        "time": "11:00",
        "duration_min": 75,
        "price": 220.0,
        "blocked_slots": ["11:00", "11:30", "12:00"],
        "status": "Expired",
        "created_at": "2025-02-08 08:00",
        "expires_at": "2025-02-08 08:10",
    },
]

NOTIFICATIONS_SEED: list[NotificationItem] = [
    {
        "id": "n1",
        "customer": "Emma Carter",
        "type": "Confirmation",
        "title": "Booking confirmed",
        "body": "Your Full Balayage on Feb 14 at 10:00 with Amelia Rivera is confirmed.",
        "time": "2 days ago",
        "read": False,
        "related_id": "a1",
    },
    {
        "id": "n2",
        "customer": "Emma Carter",
        "type": "Reminder",
        "title": "Upcoming appointment",
        "body": "Reminder: HydraFacial Premium tomorrow at 14:30 at Maison Bleu Spa.",
        "time": "1 day ago",
        "read": False,
        "related_id": "a2",
    },
    {
        "id": "n3",
        "customer": "Emma Carter",
        "type": "Invoice",
        "title": "Deposit invoice",
        "body": "Deposit of $85.00 captured for your Full Balayage booking.",
        "time": "2 days ago",
        "read": True,
        "related_id": "a1",
    },
    {
        "id": "n4",
        "customer": "Noah Patel",
        "type": "Cancellation",
        "title": "Appointment cancelled",
        "body": "Your Beard Sculpt & Trim on Feb 3 has been cancelled.",
        "time": "1 day ago",
        "read": True,
        "related_id": "a5",
    },
    {
        "id": "n5",
        "customer": "Noah Patel",
        "type": "RefundReceipt",
        "title": "Refund processed",
        "body": "$45.00 refunded to your original payment method.",
        "time": "1 day ago",
        "read": True,
        "related_id": "a5",
    },
    {
        "id": "n6",
        "customer": "Zoe Lin",
        "type": "WaitlistOffer",
        "title": "Slot available",
        "body": "A HydraFacial slot opened at Sienna Skin Lab on Feb 12. Reply within 30 min to claim.",
        "time": "3 hours ago",
        "read": False,
        "related_id": "w3",
    },
    {
        "id": "n7",
        "customer": "James Wong",
        "type": "Confirmation",
        "title": "Booking confirmed",
        "body": "Classic Cut & Hot Towel on Jan 28 at 11:15 confirmed.",
        "time": "5 days ago",
        "read": True,
        "related_id": "a3",
    },
]


class DataState(rx.State):
    salons: list[Salon] = SALONS
    practitioners: list[Practitioner] = PRACTITIONERS
    services: list[Service] = SERVICES
    appointments: list[Appointment] = APPOINTMENTS
    reviews: list[Review] = REVIEWS
    waitlist: list[WaitlistEntry] = WAITLIST
    payments: list[Payment] = PAYMENTS
    activity: list[ActivityLog] = ACTIVITY
    reservations: list[Reservation] = RESERVATIONS_SEED
    notifications: list[NotificationItem] = NOTIFICATIONS_SEED

    search_query: str = ""
    category_filter: str = "All"
    categories: list[str] = ["All", "Hair", "Spa", "Barber", "Nails", "Skin"]

    current_user: str = "Emma Carter"
    current_user_email: str = "emma.carter@example.com"

    reschedule_appointment_id: str = ""
    reschedule_date: str = ""
    reschedule_time: str = ""

    waitlist_form_salon: str = ""
    waitlist_form_service: str = ""
    waitlist_form_date: str = ""

    @rx.var
    def filtered_salons(self) -> list[Salon]:
        result = self.salons
        if self.category_filter != "All":
            result = [s for s in result if self.category_filter in s["tags"]]
        if self.search_query:
            q = self.search_query.lower()
            result = [
                s
                for s in result
                if q in s["name"].lower() or q in s["city"].lower()
            ]
        return result

    @rx.var
    def my_appointments(self) -> list[Appointment]:
        return [
            a for a in self.appointments if a["customer"] == self.current_user
        ]

    @rx.var
    def upcoming_count(self) -> int:
        return len([a for a in self.appointments if a["status"] == "Confirmed"])

    @rx.var
    def total_revenue(self) -> float:
        return sum(
            p["amount"] for p in self.payments if p["status"] == "Captured"
        )

    @rx.var
    def total_appointments(self) -> int:
        return len(self.appointments)

    @rx.var
    def avg_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(
            sum(r["rating"] for r in self.reviews) / len(self.reviews), 1
        )

    @rx.event
    def set_search(self, q: str):
        self.search_query = q

    @rx.event
    def set_category(self, c: str):
        self.category_filter = c

    @rx.var
    def my_notifications(self) -> list[NotificationItem]:
        return [
            n for n in self.notifications if n["customer"] == self.current_user
        ]

    @rx.var
    def unread_notifications_count(self) -> int:
        return len([n for n in self.my_notifications if not n["read"]])

    @rx.var
    def active_reservations(self) -> list[Reservation]:
        return [r for r in self.reservations if r["status"] == "Active"]

    @rx.var
    def expired_reservations(self) -> list[Reservation]:
        return [r for r in self.reservations if r["status"] == "Expired"]

    @rx.var
    def confirmed_reservations(self) -> list[Reservation]:
        return [r for r in self.reservations if r["status"] == "Confirmed"]

    @rx.var
    def total_refunds(self) -> float:
        return sum(
            p["amount"]
            for p in self.payments
            if p["type"] in ("Refund", "Partial Refund")
        )

    def _add_notification(
        self,
        customer: str,
        n_type: str,
        title: str,
        body: str,
        related_id: str = "",
    ) -> None:
        self.notifications.insert(
            0,
            {
                "id": f"n{uuid.uuid4().hex[:6]}",
                "customer": customer,
                "type": n_type,
                "title": title,
                "body": body,
                "time": "Just now",
                "read": False,
                "related_id": related_id,
            },
        )

    def _add_payment(
        self,
        customer: str,
        amount: float,
        p_type: str,
        status: str,
        appointment_id: str,
    ) -> None:
        self.payments.insert(
            0,
            {
                "id": f"pm{uuid.uuid4().hex[:6]}",
                "customer": customer,
                "amount": amount,
                "type": p_type,
                "status": status,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "appointment_id": appointment_id,
            },
        )

    def _add_activity(self, actor: str, action: str, target: str) -> None:
        self.activity.insert(
            0,
            {
                "id": f"ac{uuid.uuid4().hex[:6]}",
                "actor": actor,
                "action": action,
                "target": target,
                "time": "Just now",
            },
        )

    @rx.event
    def get_blocked_slots(self, practitioner: str, date: str) -> set[str]:
        blocked: set[str] = set()
        for a in self.appointments:
            if (
                a["practitioner"] == practitioner
                and a["date"] == date
                and (a["status"] != "Cancelled")
            ):
                for s in slots_for(a["time"], a["duration_min"]):
                    blocked.add(s)
        for r in self.reservations:
            if (
                r["practitioner"] == practitioner
                and r["date"] == date
                and (r["status"] == "Active")
            ):
                for s in r["blocked_slots"]:
                    blocked.add(s)
        return blocked

    def _hours_until(self, date_str: str, time_str: str) -> float:
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            return (dt - datetime.now()).total_seconds() / 3600.0
        except Exception:
            logging.exception("Unexpected error")
            return 48.0

    def _refund_for_cancellation(
        self, price: float, hours_until: float
    ) -> tuple[float, str, str]:
        if hours_until >= 24:
            return price, "Full refund", "Refund"
        elif hours_until >= 2:
            return price * 0.5, "50% refund (late cancel)", "Partial Refund"
        else:
            return 0.0, "No refund (within 2h)", "Cancellation Fee"

    @rx.event
    def cancel_appointment(self, aid: str):
        for a in self.appointments:
            if a["id"] == aid and a["status"] != "Cancelled":
                hours = self._hours_until(a["date"], a["time"])
                refund, policy_label, p_type = self._refund_for_cancellation(
                    a["price"], hours
                )
                a["status"] = "Cancelled"
                a["payment_status"] = (
                    "Refunded"
                    if refund == a["price"]
                    else ("Partially Refunded" if refund > 0 else "No Refund")
                )
                if refund > 0:
                    self._add_payment(
                        a["customer"],
                        refund,
                        p_type,
                        "Refunded",
                        aid,
                    )
                    self._add_notification(
                        a["customer"],
                        "RefundReceipt",
                        "Refund processed",
                        f"${refund:.2f} refunded for {a['service']}. Policy: {policy_label}.",
                        aid,
                    )
                else:
                    self._add_payment(
                        a["customer"],
                        0.0,
                        p_type,
                        "Captured",
                        aid,
                    )
                self._add_notification(
                    a["customer"],
                    "Cancellation",
                    "Appointment cancelled",
                    f"{a['service']} on {a['date']} at {a['time']} cancelled. {policy_label}.",
                    aid,
                )
                self._add_activity(
                    a["customer"],
                    "Cancelled appointment",
                    f"{a['service']} ({policy_label})",
                )
                return rx.toast.success(
                    f"Cancelled. {policy_label}: ${refund:.2f}"
                )
        return rx.toast.error("Appointment not found")

    @rx.event
    def open_reschedule(self, aid: str):
        self.reschedule_appointment_id = aid
        for a in self.appointments:
            if a["id"] == aid:
                self.reschedule_date = a["date"]
                self.reschedule_time = a["time"]
                break

    @rx.event
    def close_reschedule(self):
        self.reschedule_appointment_id = ""

    @rx.event
    def set_reschedule_date(self, d: str):
        self.reschedule_date = d

    @rx.event
    def set_reschedule_time(self, t: str):
        self.reschedule_time = t

    @rx.event
    def confirm_reschedule(self):
        aid = self.reschedule_appointment_id
        if not aid:
            return rx.toast.error("No appointment selected")
        for a in self.appointments:
            if a["id"] == aid:
                needed_slots = slots_for(
                    self.reschedule_time, a["duration_min"]
                )
                blocked = self.get_blocked_slots(
                    a["practitioner"], self.reschedule_date
                )
                # Exclude this appointment's own slots
                if a["date"] == self.reschedule_date:
                    for s in slots_for(a["time"], a["duration_min"]):
                        blocked.discard(s)
                conflict = any(s in blocked for s in needed_slots)
                if conflict:
                    return rx.toast.error(
                        "Conflict: requested time overlaps another booking"
                    )
                old = f"{a['date']} {a['time']}"
                a["date"] = self.reschedule_date
                a["time"] = self.reschedule_time
                self._add_notification(
                    a["customer"],
                    "Confirmation",
                    "Appointment rescheduled",
                    f"{a['service']} moved from {old} to {a['date']} {a['time']}.",
                    aid,
                )
                self._add_activity(
                    a["customer"],
                    "Rescheduled appointment",
                    f"{a['service']} → {a['date']} {a['time']}",
                )
                self.reschedule_appointment_id = ""
                return rx.toast.success("Rescheduled successfully")
        return rx.toast.error("Appointment not found")

    @rx.event
    def enroll_waitlist(self, salon: str, service: str, date: str):
        if not (salon and service and date):
            return rx.toast.error("Please fill all waitlist fields")
        wid = f"w{uuid.uuid4().hex[:5]}"
        self.waitlist.append(
            {
                "id": wid,
                "customer": self.current_user,
                "salon": salon,
                "service": service,
                "requested_date": date,
                "status": "Active",
            }
        )
        self._add_notification(
            self.current_user,
            "WaitlistOffer",
            "Added to waitlist",
            f"You're on the waitlist for {service} at {salon} on {date}. We'll notify you when a slot opens.",
            wid,
        )
        self._add_activity(
            self.current_user,
            "Joined waitlist",
            f"{service} @ {salon}",
        )
        self.waitlist_form_salon = ""
        self.waitlist_form_service = ""
        self.waitlist_form_date = ""
        return rx.toast.success("Added to waitlist")

    @rx.event
    def offer_waitlist_slot(self, wid: str):
        for w in self.waitlist:
            if w["id"] == wid:
                w["status"] = "Offered"
                self._add_notification(
                    w["customer"],
                    "WaitlistOffer",
                    "Slot available!",
                    f"A slot opened for {w['service']} at {w['salon']}. Reply within 30 minutes to claim.",
                    wid,
                )
                return rx.toast.success(f"Offer sent to {w['customer']}")
        return rx.noop()

    @rx.event
    def set_waitlist_salon(self, v: str):
        self.waitlist_form_salon = v

    @rx.event
    def set_waitlist_service(self, v: str):
        self.waitlist_form_service = v

    @rx.event
    def set_waitlist_date(self, v: str):
        self.waitlist_form_date = v

    @rx.event
    def mark_notification_read(self, nid: str):
        for n in self.notifications:
            if n["id"] == nid:
                n["read"] = True

    @rx.event
    def expire_reservation(self, rid: str):
        for r in self.reservations:
            if r["id"] == rid and r["status"] == "Active":
                r["status"] = "Expired"
                self._add_activity(
                    "System", "Reservation expired", r["service_name"]
                )
                return rx.toast.info("Reservation hold expired")
        return rx.noop()