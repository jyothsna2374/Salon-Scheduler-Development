import reflex as rx
from app.components.layout import page_layout
from app.components.salon_card import salon_card
from app.states.data_state import DataState


def category_chip(cat: str) -> rx.Component:
    return rx.el.button(
        cat,
        on_click=lambda: DataState.set_category(cat),
        class_name=rx.cond(
            DataState.category_filter == cat,
            "px-4 py-2 text-sm font-medium rounded-lg bg-blue-600 text-white",
            "px-4 py-2 text-sm font-medium rounded-lg bg-white text-gray-700 border border-gray-200 hover:border-gray-300",
        ),
    )


def stat_card(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
            rx.el.span(label, class_name="text-xs font-medium text-gray-600"),
            class_name="flex items-center gap-1.5 mb-1",
        ),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        class_name="bg-white border border-gray-200 rounded-xl p-4",
    )


def home_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Find your next appointment",
                    class_name="text-3xl sm:text-4xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Discover top salons, spas, and barbershops near you.",
                    class_name="text-gray-600 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Search salons or cities...",
                            default_value=DataState.search_query,
                            on_change=DataState.set_search.debounce(300),
                            class_name="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm",
                        ),
                        class_name="relative flex-1",
                    ),
                    class_name="flex gap-3 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.categories, category_chip),
                    class_name="flex flex-wrap gap-2 mb-8",
                ),
            ),
            rx.el.div(
                stat_card(
                    "Salons", DataState.salons.length().to_string(), "store"
                ),
                stat_card(
                    "Practitioners",
                    DataState.practitioners.length().to_string(),
                    "users",
                ),
                stat_card(
                    "Services", DataState.services.length().to_string(), "list"
                ),
                stat_card(
                    "Avg rating", DataState.avg_rating.to_string(), "star"
                ),
                class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Featured salons",
                    class_name="text-xl font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.filtered_salons, salon_card),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5",
                ),
            ),
        ),
    )