import reflex as rx
from app.states.data_state import Salon
from app.states.booking_state import BookingState


def tag_pill(tag: str) -> rx.Component:
    return rx.el.span(
        tag,
        class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full",
    )


def salon_card(s: Salon) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("sparkles", class_name="h-10 w-10 text-blue-300"),
                class_name="h-40 bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        s["name"],
                        class_name="text-base font-semibold text-gray-900",
                    ),
                    rx.el.div(
                        rx.icon(
                            "star",
                            class_name="h-3.5 w-3.5 fill-amber-400 text-amber-400",
                        ),
                        rx.el.span(
                            s["rating"].to_string(),
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.span(
                            f"({s['reviews']})",
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="flex items-start justify-between mb-1",
                ),
                rx.el.div(
                    rx.icon("map-pin", class_name="h-3.5 w-3.5 text-gray-400"),
                    rx.el.span(s["city"], class_name="text-xs text-gray-600"),
                    class_name="flex items-center gap-1 mb-3",
                ),
                rx.el.div(
                    rx.foreach(s["tags"], tag_pill),
                    class_name="flex flex-wrap gap-1.5 mb-4",
                ),
                rx.el.div(
                    rx.el.a(
                        "View details",
                        href=f"/salon/{s['id']}",
                        class_name="text-sm font-medium text-gray-600 hover:text-gray-900",
                    ),
                    rx.el.button(
                        "Book now",
                        rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                        on_click=lambda: BookingState.start_booking(
                            s["id"], s["name"]
                        ),
                        class_name="flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg",
                    ),
                    class_name="flex items-center justify-between",
                ),
                class_name="p-4",
            ),
        ),
        class_name="bg-white border border-gray-200 rounded-xl overflow-hidden hover:border-blue-300 transition-colors",
    )