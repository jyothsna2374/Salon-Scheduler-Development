import reflex as rx
from app.pages.home import home_page
from app.pages.salon_detail import salon_detail_page
from app.pages.booking import booking_page
from app.pages.appointments import appointments_page
from app.pages.profile import profile_page
from app.pages.manager import manager_page
from app.pages.admin import admin_page
from app.pages.intelligence import intelligence_page


def index() -> rx.Component:
    return home_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(salon_detail_page, route="/salon/[id]")
app.add_page(booking_page, route="/book")
app.add_page(appointments_page, route="/appointments")
app.add_page(profile_page, route="/profile")
app.add_page(manager_page, route="/manager")
app.add_page(admin_page, route="/admin")
app.add_page(intelligence_page, route="/intelligence")