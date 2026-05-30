import reflex as rx
from app.components.layout import page_layout
from app.states.data_state import (
    DataState,
    Payment,
    ActivityLog,
    NotificationItem,
    Reservation,
)


def notification_icon_for(n_type: str) -> str:
    return "bell"


def notification_row(n: NotificationItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bell", class_name="h-3.5 w-3.5 text-blue-600"),
            class_name="h-7 w-7 rounded-full bg-blue-50 flex items-center justify-center shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    n["title"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    n["type"],
                    class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                ),
                class_name="flex items-center gap-2 flex-wrap mb-1",
            ),
            rx.el.p(n["body"], class_name="text-xs text-gray-600"),
            rx.el.p(
                f"To: {n['customer']} · {n['time']}",
                class_name="text-xs text-gray-400 mt-1",
            ),
        ),
        class_name="flex items-start gap-3 p-3 bg-white border border-gray-200 rounded-lg",
    )


def reservation_admin_row(r: Reservation) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            r["customer"],
            class_name="px-4 py-3 text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            r["service_name"],
            class_name="px-4 py-3 text-sm text-gray-700",
        ),
        rx.el.td(
            f"{r['date']} {r['time']}",
            class_name="px-4 py-3 text-sm text-gray-700",
        ),
        rx.el.td(
            r["blocked_slots"].length().to_string() + " slots",
            class_name="px-4 py-3 text-sm text-gray-700",
        ),
        rx.el.td(
            r["expires_at"],
            class_name="px-4 py-3 text-sm text-gray-500",
        ),
        rx.el.td(
            rx.match(
                r["status"],
                (
                    "Active",
                    rx.el.span(
                        "Active",
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
                rx.el.span(r["status"], class_name="text-xs"),
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50",
    )


def kpi_card(label: str, value: str, icon: str, accent: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 {accent}"),
            class_name="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center mb-3",
        ),
        rx.el.p(label, class_name="text-xs font-medium text-gray-600 mb-1"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def payment_row(p: Payment) -> rx.Component:
    return rx.el.tr(
        rx.el.td(p["date"], class_name="px-4 py-3 text-sm text-gray-700"),
        rx.el.td(
            p["customer"],
            class_name="px-4 py-3 text-sm font-medium text-gray-900",
        ),
        rx.el.td(p["type"], class_name="px-4 py-3 text-sm text-gray-700"),
        rx.el.td(
            f"${p['amount']:.2f}",
            class_name="px-4 py-3 text-sm font-semibold text-gray-900",
        ),
        rx.el.td(
            rx.match(
                p["status"],
                (
                    "Captured",
                    rx.el.span(
                        "Captured",
                        class_name="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-700 rounded-full w-fit",
                    ),
                ),
                (
                    "Refunded",
                    rx.el.span(
                        "Refunded",
                        class_name="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full w-fit",
                    ),
                ),
                rx.el.span(p["status"], class_name="text-xs"),
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50",
    )


def activity_item(a: ActivityLog) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("activity", class_name="h-3.5 w-3.5 text-blue-600"),
            class_name="h-7 w-7 rounded-full bg-blue-50 flex items-center justify-center shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(a["actor"], class_name="font-semibold"),
                " ",
                a["action"],
                " ",
                rx.el.span(a["target"], class_name="text-gray-600"),
                class_name="text-sm text-gray-900",
            ),
            rx.el.p(a["time"], class_name="text-xs text-gray-500 mt-0.5"),
        ),
        class_name="flex items-start gap-3 p-3 bg-white border border-gray-200 rounded-lg",
    )


def setting_row(label: str, desc: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-semibold text-gray-900"),
            rx.el.p(desc, class_name="text-xs text-gray-500"),
        ),
        rx.el.span(
            value,
            class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full",
        ),
        class_name="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg",
    )


def admin_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h1(
                "Admin workspace", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Platform health, payments, and system configuration.",
                class_name="text-gray-600 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            kpi_card(
                "Total revenue",
                f"${DataState.total_revenue:.2f}",
                "dollar-sign",
                "text-blue-600",
            ),
            kpi_card(
                "Appointments",
                DataState.total_appointments.to_string(),
                "calendar",
                "text-blue-600",
            ),
            kpi_card(
                "Active salons",
                DataState.salons.length().to_string(),
                "store",
                "text-blue-600",
            ),
            kpi_card(
                "Total refunds",
                f"${DataState.total_refunds:.2f}",
                "rotate-ccw",
                "text-blue-600",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Reservation holds",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Customer",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Service",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "When",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Blocked",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Expires",
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
                            rx.foreach(
                                DataState.reservations, reservation_admin_row
                            )
                        ),
                        class_name="table-auto w-full",
                    ),
                    class_name="bg-white border border-gray-200 rounded-xl overflow-hidden overflow-x-auto",
                ),
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Payments & refunds",
                    class_name="text-lg font-bold text-gray-900 mb-4",
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
                                    "Customer",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Type",
                                    class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                                ),
                                rx.el.th(
                                    "Amount",
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
                            rx.foreach(DataState.payments, payment_row)
                        ),
                        class_name="table-auto w-full",
                    ),
                    class_name="bg-white border border-gray-200 rounded-xl overflow-hidden overflow-x-auto mb-8",
                ),
                rx.el.h2(
                    "System settings",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    setting_row(
                        "Default deposit", "Applied to all new bookings", "30%"
                    ),
                    setting_row(
                        "Cancellation window",
                        "Free cancellation period",
                        "24 hours",
                    ),
                    setting_row(
                        "Reminder notifications",
                        "Email & SMS before appointment",
                        "Enabled",
                    ),
                    setting_row(
                        "Waitlist auto-offer",
                        "Automatically offer slots",
                        "Enabled",
                    ),
                    setting_row(
                        "Stylist matching",
                        "Intelligent ranking algorithm",
                        "Active",
                    ),
                    setting_row(
                        "Sentiment analysis",
                        "Review sentiment scoring",
                        "Active",
                    ),
                    class_name="space-y-2",
                ),
                class_name="lg:col-span-2",
            ),
            rx.el.div(
                rx.el.h2(
                    "Recent activity",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.activity, activity_item),
                    class_name="space-y-2 mb-6",
                ),
                rx.el.h2(
                    "Notification history",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.notifications, notification_row),
                    class_name="space-y-2 max-h-96 overflow-y-auto",
                ),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
    )