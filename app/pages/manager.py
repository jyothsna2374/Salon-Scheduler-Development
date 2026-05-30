import reflex as rx
from app.components.layout import page_layout
from app.states.data_state import (
    DataState,
    Appointment,
    Practitioner,
    WaitlistEntry,
    Reservation,
)


def metric(
    label: str, value: str, change: str, icon: str, positive: bool
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
                rx.el.span(
                    label, class_name="text-xs font-medium text-gray-600"
                ),
                class_name="flex items-center gap-1.5 mb-2",
            ),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
            rx.el.div(
                rx.icon(
                    rx.cond(positive, "trending-up", "trending-down"),
                    class_name="h-3 w-3",
                ),
                rx.el.span(change, class_name="text-xs font-medium"),
                class_name=rx.cond(
                    positive,
                    "flex items-center gap-1 text-green-600 mt-1",
                    "flex items-center gap-1 text-red-600 mt-1",
                ),
            ),
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def appt_table_row(a: Appointment) -> rx.Component:
    return rx.el.tr(
        rx.el.td(a["date"], class_name="px-4 py-3 text-sm text-gray-700"),
        rx.el.td(a["time"], class_name="px-4 py-3 text-sm text-gray-700"),
        rx.el.td(
            a["customer"],
            class_name="px-4 py-3 text-sm font-medium text-gray-900",
        ),
        rx.el.td(a["service"], class_name="px-4 py-3 text-sm text-gray-700"),
        rx.el.td(
            a["practitioner"], class_name="px-4 py-3 text-sm text-gray-700"
        ),
        rx.el.td(
            f"${a['price']:.2f}",
            class_name="px-4 py-3 text-sm font-semibold text-gray-900",
        ),
        rx.el.td(
            rx.match(
                a["status"],
                (
                    "Confirmed",
                    rx.el.span(
                        "Confirmed",
                        class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                    ),
                ),
                (
                    "Completed",
                    rx.el.span(
                        "Completed",
                        class_name="px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-700 rounded-full w-fit",
                    ),
                ),
                (
                    "Cancelled",
                    rx.el.span(
                        "Cancelled",
                        class_name="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full w-fit",
                    ),
                ),
                rx.el.span(a["status"], class_name="text-xs"),
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50",
    )


def practitioner_row(p: Practitioner) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={p['avatar_seed']}",
            class_name="h-12 w-12 rounded-full bg-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                p["name"], class_name="text-sm font-semibold text-gray-900"
            ),
            rx.el.p(p["title"], class_name="text-xs text-gray-500"),
        ),
        rx.el.div(
            rx.icon(
                "star", class_name="h-3.5 w-3.5 fill-amber-400 text-amber-400"
            ),
            rx.el.span(
                p["rating"].to_string(), class_name="text-sm font-semibold"
            ),
            class_name="flex items-center gap-1 ml-auto",
        ),
        rx.el.span(
            f"{p['reviews']} reviews", class_name="text-xs text-gray-500"
        ),
        class_name="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg",
    )


def waitlist_row(w: WaitlistEntry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                w["customer"], class_name="text-sm font-semibold text-gray-900"
            ),
            rx.el.p(
                f"{w['service']} · {w['salon']}",
                class_name="text-xs text-gray-600",
            ),
            rx.el.p(
                f"Requested: {w['requested_date']}",
                class_name="text-xs text-gray-500 mt-1",
            ),
        ),
        rx.el.div(
            rx.el.span(
                w["status"],
                class_name=rx.cond(
                    w["status"] == "Active",
                    "px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                    "px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full w-fit",
                ),
            ),
            rx.cond(
                w["status"] == "Active",
                rx.el.button(
                    "Offer slot",
                    on_click=lambda: DataState.offer_waitlist_slot(w["id"]),
                    class_name="ml-2 px-2 py-0.5 text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-full",
                ),
                rx.el.div(),
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg",
    )


def reservation_row(r: Reservation) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    r["customer"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.match(
                    r["status"],
                    (
                        "Active",
                        rx.el.span(
                            "Active hold",
                            class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                        ),
                    ),
                    (
                        "Confirmed",
                        rx.el.span(
                            "Confirmed",
                            class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                        ),
                    ),
                    (
                        "Expired",
                        rx.el.span(
                            "Expired",
                            class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-600 rounded-full w-fit",
                        ),
                    ),
                    rx.el.span(
                        r["status"],
                        class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-full w-fit",
                    ),
                ),
                class_name="flex items-center gap-2 mb-1",
            ),
            rx.el.p(
                f"{r['service_name']} · {r['practitioner']}",
                class_name="text-xs text-gray-600",
            ),
            rx.el.p(
                f"{r['date']} {r['time']} · {r['duration_min']} min · ${r['price']:.0f}",
                class_name="text-xs text-gray-500 mt-0.5",
            ),
            rx.el.p(
                rx.el.span(
                    "Adjacent slots blocked: ",
                    class_name="text-xs font-semibold text-gray-700",
                ),
                rx.el.span(
                    r["blocked_slots"].join(", "),
                    class_name="text-xs text-gray-600",
                ),
                class_name="mt-1",
            ),
            rx.el.p(
                f"Expires: {r['expires_at']}",
                class_name="text-xs text-gray-400 mt-0.5",
            ),
        ),
        class_name="p-3 bg-white border border-gray-200 rounded-lg",
    )


def manager_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h1(
                "Manager workspace",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Lumiere Hair Studio · Daily operations dashboard",
                class_name="text-gray-600 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            metric(
                "Today's bookings",
                "12",
                "+3 from yesterday",
                "calendar-check",
                True,
            ),
            metric("Revenue (week)", "$8,420", "+12.4%", "dollar-sign", True),
            metric("Avg utilization", "78%", "+5%", "activity", True),
            metric("No-shows", "2", "-1", "user-x", True),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Upcoming appointments",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("download", class_name="h-3.5 w-3.5"),
                        "Export",
                        class_name="flex items-center gap-1 px-3 py-1.5 bg-white border border-gray-200 text-gray-700 text-xs font-medium rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Date",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Time",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Customer",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Service",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Stylist",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Price",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                class_name="bg-gray-50",
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(DataState.appointments, appt_table_row)
                        ),
                        class_name="table-auto w-full",
                    ),
                    class_name="bg-white border border-gray-200 rounded-xl overflow-hidden overflow-x-auto",
                ),
                class_name="lg:col-span-2",
            ),
            rx.el.div(
                rx.el.h2(
                    "Practitioners",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.practitioners, practitioner_row),
                    class_name="space-y-2 mb-6",
                ),
                rx.el.h2(
                    "Waitlist",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.waitlist, waitlist_row),
                    class_name="space-y-2 mb-6",
                ),
                rx.el.h2(
                    "Reservation holds",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.reservations, reservation_row),
                    class_name="space-y-2",
                ),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
    )