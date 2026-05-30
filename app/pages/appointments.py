import reflex as rx
from app.components.layout import page_layout
from app.states.data_state import DataState, Appointment
from app.states.booking_state import TIME_SLOTS


def status_pill(status: str) -> rx.Component:
    return rx.match(
        status,
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
        rx.el.span(
            status,
            class_name="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-full w-fit",
        ),
    )


def appointment_row(a: Appointment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", class_name="h-5 w-5 text-blue-600"),
                class_name="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        a["service"],
                        class_name="text-base font-semibold text-gray-900",
                    ),
                    status_pill(a["status"]),
                    class_name="flex items-center gap-2 mb-1 flex-wrap",
                ),
                rx.el.p(
                    f"{a['salon_name']} · with {a['practitioner']}",
                    class_name="text-sm text-gray-600",
                ),
                rx.el.div(
                    rx.icon("calendar", class_name="h-3.5 w-3.5 text-gray-400"),
                    rx.el.span(a["date"], class_name="text-xs text-gray-600"),
                    rx.icon(
                        "clock", class_name="h-3.5 w-3.5 text-gray-400 ml-2"
                    ),
                    rx.el.span(a["time"], class_name="text-xs text-gray-600"),
                    rx.el.span("·", class_name="text-gray-400 mx-1"),
                    rx.el.span(
                        f"{a['duration_min']} min",
                        class_name="text-xs text-gray-600",
                    ),
                    rx.el.span("·", class_name="text-gray-400 mx-1"),
                    rx.el.span(
                        f"${a['price']:.2f}",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    class_name="flex items-center gap-1 mt-2 flex-wrap",
                ),
                class_name="flex-1",
            ),
            class_name="flex items-start gap-3 flex-1",
        ),
        rx.cond(
            a["status"] == "Confirmed",
            rx.el.div(
                rx.el.button(
                    "Reschedule",
                    on_click=lambda: DataState.open_reschedule(a["id"]),
                    class_name="px-3 py-1.5 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50",
                ),
                rx.el.button(
                    "Cancel",
                    on_click=lambda: DataState.cancel_appointment(a["id"]),
                    class_name="px-3 py-1.5 bg-white border border-red-200 text-red-700 text-sm font-medium rounded-lg hover:bg-red-50",
                ),
                class_name="flex gap-2",
            ),
            rx.el.div(),
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 bg-white border border-gray-200 rounded-xl",
    )


def reschedule_time_button(t: str) -> rx.Component:
    is_selected = DataState.reschedule_time == t
    return rx.el.button(
        t,
        on_click=lambda: DataState.set_reschedule_time(t),
        class_name=rx.cond(
            is_selected,
            "px-3 py-2 bg-blue-600 text-white text-xs font-semibold rounded-lg",
            "px-3 py-2 bg-white border border-gray-200 text-gray-700 text-xs font-medium rounded-lg hover:border-blue-300",
        ),
    )


def reschedule_modal() -> rx.Component:
    return rx.cond(
        DataState.reschedule_appointment_id != "",
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Reschedule appointment",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=DataState.close_reschedule,
                        class_name="text-gray-400 hover:text-gray-700",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.label(
                    "New date",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.input(
                    type="date",
                    default_value=DataState.reschedule_date,
                    on_change=DataState.set_reschedule_date.debounce(300),
                    class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 mb-4",
                ),
                rx.el.label(
                    "New time",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.foreach(TIME_SLOTS, reschedule_time_button),
                    class_name="grid grid-cols-4 gap-2 mb-5",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=DataState.close_reschedule,
                        class_name="px-4 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Confirm reschedule",
                        on_click=DataState.confirm_reschedule,
                        class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="bg-white rounded-2xl border border-gray-200 p-6 max-w-md w-full mx-4",
            ),
            class_name="fixed inset-0 z-50 bg-black/40 flex items-center justify-center",
        ),
        rx.el.div(),
    )


def policy_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("info", class_name="h-4 w-4 text-blue-600"),
            rx.el.span(
                "Cancellation policy",
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-2 mb-2",
        ),
        rx.el.ul(
            rx.el.li(
                "Cancel >24h ahead: full refund",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Cancel 2-24h ahead: 50% refund",
                class_name="text-xs text-gray-700",
            ),
            rx.el.li(
                "Cancel <2h ahead: deposit forfeited",
                class_name="text-xs text-gray-700",
            ),
            class_name="list-disc pl-5 space-y-0.5",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-4 mb-6",
    )


def appointments_page() -> rx.Component:
    return page_layout(
        rx.el.h1(
            "My appointments",
            class_name="text-2xl font-bold text-gray-900 mb-1",
        ),
        rx.el.p(
            "Manage your upcoming and past bookings.",
            class_name="text-gray-600 mb-6",
        ),
        policy_card(),
        rx.el.div(
            rx.foreach(DataState.my_appointments, appointment_row),
            class_name="space-y-3",
        ),
        reschedule_modal(),
    )