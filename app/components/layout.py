import reflex as rx
from app.components.navbar import navbar


def page_layout(*content) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                *content,
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )