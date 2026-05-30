import reflex as rx


def nav_link(label: str, href: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("scissors", class_name="h-5 w-5 text-white"),
                    class_name="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center",
                ),
                rx.el.span(
                    "Salonary", class_name="text-lg font-bold text-gray-900"
                ),
                href="/",
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                nav_link("Discover", "/", "compass"),
                nav_link("Appointments", "/appointments", "calendar"),
                nav_link("Profile", "/profile", "user"),
                nav_link("Manager", "/manager", "briefcase"),
                nav_link("Admin", "/admin", "shield"),
                nav_link("Intelligence", "/intelligence", "brain"),
                class_name="hidden md:flex items-center gap-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", class_name="h-4 w-4"),
                    class_name="h-9 w-9 flex items-center justify-center rounded-lg border border-gray-200 hover:bg-gray-50 text-gray-700",
                ),
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/notionists/svg?seed=emma",
                        class_name="h-9 w-9 rounded-full bg-gray-100",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between",
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-40",
    )