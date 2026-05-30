import reflex as rx
from app.components.layout import page_layout
from app.states.data_state import DataState, Service, Practitioner
from app.states.booking_state import BookingState


def step_indicator(
    num: int, label: str, active: bool, done: bool
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                done,
                rx.icon(
                    "check",
                    class_name="h-4 w-4 text-white",
                ),
                rx.el.span(
                    num,
                    class_name="text-sm font-semibold",
                ),
            ),
            class_name=rx.cond(
                active | done,
                "h-8 w-8 rounded-full bg-blue-600 text-white flex items-center justify-center",
                "h-8 w-8 rounded-full bg-gray-200 text-gray-500 flex items-center justify-center",
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                active,
                "text-sm font-semibold text-gray-900",
                "text-sm font-medium text-gray-500",
            ),
        ),
        class_name="flex items-center gap-2",
    )


def steps_bar() -> rx.Component:
    return rx.el.div(
        step_indicator(
            1, "Service", BookingState.step == 1, BookingState.step > 1
        ),
        rx.el.div(class_name="flex-1 h-px bg-gray-200"),
        step_indicator(
            2, "Practitioner", BookingState.step == 2, BookingState.step > 2
        ),
        rx.el.div(class_name="flex-1 h-px bg-gray-200"),
        step_indicator(
            3, "Time", BookingState.step == 3, BookingState.step > 3
        ),
        rx.el.div(class_name="flex-1 h-px bg-gray-200"),
        step_indicator(4, "Confirm", BookingState.step == 4, False),
        class_name="flex items-center gap-3 mb-8",
    )


def service_option(s: Service) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    s["name"],
                    class_name="text-base font-semibold text-gray-900",
                ),
                rx.el.p(
                    s["description"], class_name="text-sm text-gray-600 mt-1"
                ),
                rx.el.div(
                    rx.icon("clock", class_name="h-3.5 w-3.5 text-gray-400"),
                    rx.el.span(
                        f"{s['duration_min']} min",
                        class_name="text-xs text-gray-600",
                    ),
                    rx.el.span("·", class_name="text-gray-400"),
                    rx.el.span(
                        s["category"], class_name="text-xs text-gray-600"
                    ),
                    class_name="flex items-center gap-1.5 mt-2",
                ),
                class_name="text-left flex-1",
            ),
            rx.el.p(
                f"${s['price']:.0f}",
                class_name="text-lg font-bold text-blue-600",
            ),
            class_name="flex items-start justify-between gap-4 w-full",
        ),
        on_click=lambda: BookingState.select_service(
            s["id"], s["name"], s["price"], s["duration_min"]
        ),
        class_name=rx.cond(
            BookingState.selected_service_id == s["id"],
            "w-full p-4 bg-blue-50 border-2 border-blue-600 rounded-xl",
            "w-full p-4 bg-white border border-gray-200 rounded-xl hover:border-blue-300",
        ),
    )


def practitioner_option(p: Practitioner) -> rx.Component:
    return rx.el.button(
        rx.image(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={p['avatar_seed']}",
            class_name="h-16 w-16 rounded-full bg-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                p["name"], class_name="text-base font-semibold text-gray-900"
            ),
            rx.el.p(p["title"], class_name="text-sm text-gray-500"),
            rx.el.div(
                rx.icon(
                    "star",
                    class_name="h-3.5 w-3.5 fill-amber-400 text-amber-400",
                ),
                rx.el.span(
                    p["rating"].to_string(), class_name="text-xs font-semibold"
                ),
                rx.el.span(
                    f"· {p['years']} yrs · {p['reviews']} reviews",
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex items-center gap-1 mt-1",
            ),
            class_name="text-left flex-1",
        ),
        on_click=lambda: BookingState.select_practitioner(p["id"], p["name"]),
        class_name=rx.cond(
            BookingState.selected_practitioner_id == p["id"],
            "w-full flex items-center gap-4 p-4 bg-blue-50 border-2 border-blue-600 rounded-xl",
            "w-full flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-xl hover:border-blue-300",
        ),
    )


def time_slot(t: str) -> rx.Component:
    status = BookingState.slot_status_map[t]
    is_blocked = status == "blocked"
    is_cant_fit = status == "cant-fit"
    is_selected = BookingState.selected_time == t
    is_disabled = is_blocked | is_cant_fit
    return rx.el.button(
        t,
        on_click=rx.cond(is_disabled, rx.noop(), BookingState.select_time(t)),
        disabled=is_disabled,
        title=rx.cond(
            is_blocked,
            "Booked - adjacent slots blocked",
            rx.cond(is_cant_fit, "Service won't fit", "Available"),
        ),
        class_name=rx.cond(
            is_blocked,
            "px-4 py-3 bg-red-50 border border-red-200 text-red-400 text-sm font-medium rounded-lg line-through cursor-not-allowed",
            rx.cond(
                is_cant_fit,
                "px-4 py-3 bg-gray-100 border border-gray-200 text-gray-400 text-sm font-medium rounded-lg cursor-not-allowed",
                rx.cond(
                    is_selected,
                    "px-4 py-3 bg-blue-600 text-white text-sm font-semibold rounded-lg",
                    "px-4 py-3 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:border-blue-300",
                ),
            ),
        ),
    )


def step_service() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Choose a service",
            class_name="text-xl font-bold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.foreach(DataState.services, service_option),
            class_name="space-y-3",
        ),
    )


def step_practitioner() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Choose a practitioner",
            class_name="text-xl font-bold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.foreach(DataState.practitioners, practitioner_option),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
        ),
    )


def step_time() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Pick a date and time",
            class_name="text-xl font-bold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Date",
                class_name="block text-sm font-semibold text-gray-700 mb-2",
            ),
            rx.el.input(
                type="date",
                default_value=BookingState.selected_date,
                on_change=BookingState.set_date.debounce(300),
                class_name="w-full md:w-64 px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500",
            ),
            class_name="mb-6",
        ),
        rx.el.label(
            "Available times",
            class_name="block text-sm font-semibold text-gray-700 mb-2",
        ),
        rx.el.div(
            rx.foreach(BookingState.time_slots, time_slot),
            class_name="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    class_name="h-3 w-3 rounded bg-red-50 border border-red-200"
                ),
                rx.el.span("Booked", class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.div(
                rx.el.span(
                    class_name="h-3 w-3 rounded bg-gray-100 border border-gray-200"
                ),
                rx.el.span(
                    "Won't fit duration",
                    class_name="text-xs text-gray-600",
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.div(
                rx.el.span(class_name="h-3 w-3 rounded bg-blue-600"),
                rx.el.span("Selected", class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex items-center gap-4 mt-3 flex-wrap",
        ),
        rx.cond(
            BookingState.active_reservation_id != "",
            rx.el.div(
                rx.icon("clock", class_name="h-3.5 w-3.5"),
                rx.el.span(
                    f"Reservation hold active until {BookingState.reservation_expires_at}",
                    class_name="text-xs",
                ),
                class_name="flex items-center gap-1.5 mt-3 px-3 py-2 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg w-fit",
            ),
            rx.el.div(),
        ),
    )


def step_confirm() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Review and confirm",
            class_name="text-xl font-bold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Salon",
                    class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
                ),
                rx.el.p(
                    BookingState.selected_salon_name,
                    class_name="text-base font-semibold text-gray-900 mt-1",
                ),
                class_name="border-b border-gray-200 pb-3 mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Service",
                        class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
                    ),
                    rx.el.p(
                        BookingState.selected_service_name,
                        class_name="text-sm font-medium text-gray-900 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Practitioner",
                        class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
                    ),
                    rx.el.p(
                        BookingState.selected_practitioner_name,
                        class_name="text-sm font-medium text-gray-900 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Date",
                        class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
                    ),
                    rx.el.p(
                        BookingState.selected_date,
                        class_name="text-sm font-medium text-gray-900 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Time",
                        class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
                    ),
                    rx.el.p(
                        BookingState.selected_time,
                        class_name="text-sm font-medium text-gray-900 mt-1",
                    ),
                ),
                class_name="grid grid-cols-2 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Notes for your practitioner (optional)",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.textarea(
                    placeholder="Any preferences or details we should know...",
                    on_change=BookingState.set_notes.debounce(400),
                    class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500",
                    rows="3",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Service", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        f"${BookingState.selected_service_price:.2f}",
                        class_name="text-sm font-medium",
                    ),
                    class_name="flex justify-between mb-1",
                ),
                rx.el.div(
                    rx.el.p(
                        "Deposit (30%)", class_name="text-sm text-gray-600"
                    ),
                    rx.el.p(
                        f"${BookingState.selected_service_price * 0.3:.2f}",
                        class_name="text-sm font-medium",
                    ),
                    class_name="flex justify-between mb-1",
                ),
                rx.el.div(
                    rx.el.p("Due at salon", class_name="text-sm text-gray-600"),
                    rx.el.p(
                        f"${BookingState.selected_service_price * 0.7:.2f}",
                        class_name="text-sm font-medium",
                    ),
                    class_name="flex justify-between mb-3 pb-3 border-b border-gray-200",
                ),
                rx.el.div(
                    rx.el.p(
                        "Total",
                        class_name="text-base font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        f"${BookingState.selected_service_price:.2f}",
                        class_name="text-base font-bold text-blue-600",
                    ),
                    class_name="flex justify-between",
                ),
                class_name="bg-gray-50 border border-gray-200 rounded-lg p-4",
            ),
            class_name="bg-white border border-gray-200 rounded-xl p-5",
        ),
    )


def booking_page() -> rx.Component:
    return page_layout(
        rx.el.h1(
            "Book an appointment",
            class_name="text-2xl font-bold text-gray-900 mb-1",
        ),
        rx.el.p(
            rx.cond(
                BookingState.selected_salon_name != "",
                BookingState.selected_salon_name,
                "Select a salon to begin",
            ),
            class_name="text-gray-600 mb-6",
        ),
        steps_bar(),
        rx.el.div(
            rx.match(
                BookingState.step,
                (1, step_service()),
                (2, step_practitioner()),
                (3, step_time()),
                (4, step_confirm()),
                step_service(),
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", class_name="h-4 w-4"),
                "Back",
                on_click=BookingState.prev_step,
                disabled=BookingState.step == 1,
                class_name="flex items-center gap-1 px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 disabled:opacity-50",
            ),
            rx.cond(
                BookingState.step < 4,
                rx.el.button(
                    "Next",
                    rx.icon("chevron-right", class_name="h-4 w-4"),
                    on_click=BookingState.next_step,
                    class_name="flex items-center gap-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium",
                ),
                rx.el.button(
                    rx.icon("check", class_name="h-4 w-4"),
                    "Confirm booking",
                    on_click=BookingState.confirm_booking,
                    class_name="flex items-center gap-1 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold",
                ),
            ),
            class_name="flex items-center justify-between",
        ),
    )