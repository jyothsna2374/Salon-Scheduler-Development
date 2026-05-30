import reflex as rx
from app.components.layout import page_layout
from app.states.data_state import DataState, NotificationItem


def notification_card(n: NotificationItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                rx.match(
                    n["type"],
                    ("Confirmation", "check-circle"),
                    ("Reminder", "bell"),
                    ("Cancellation", "x-circle"),
                    ("WaitlistOffer", "list-plus"),
                    ("Invoice", "file-text"),
                    ("RefundReceipt", "rotate-ccw"),
                    "bell",
                ),
                class_name="h-4 w-4 text-blue-600",
            ),
            class_name="h-8 w-8 rounded-full bg-blue-50 flex items-center justify-center shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    n["title"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.cond(
                    ~n["read"],
                    rx.el.span(class_name="h-2 w-2 rounded-full bg-blue-600"),
                    rx.el.div(),
                ),
                class_name="flex items-center justify-between gap-2 mb-0.5",
            ),
            rx.el.p(n["body"], class_name="text-xs text-gray-600"),
            rx.el.p(n["time"], class_name="text-xs text-gray-400 mt-1"),
            class_name="flex-1",
        ),
        on_click=lambda: DataState.mark_notification_read(n["id"]),
        class_name="flex items-start gap-3 p-3 bg-white border border-gray-200 rounded-lg cursor-pointer hover:border-blue-300",
    )


def profile_field(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-gray-400"),
            rx.el.label(
                label,
                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
            ),
            class_name="flex items-center gap-1.5 mb-1",
        ),
        rx.el.p(value, class_name="text-sm font-medium text-gray-900"),
        class_name="p-4 bg-white border border-gray-200 rounded-xl",
    )


def profile_page() -> rx.Component:
    return page_layout(
        rx.el.h1("Profile", class_name="text-2xl font-bold text-gray-900 mb-1"),
        rx.el.p(
            "Manage your account, preferences, and notifications.",
            class_name="text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=emma",
                    class_name="h-20 w-20 rounded-full bg-gray-100",
                ),
                rx.el.div(
                    rx.el.h2(
                        DataState.current_user,
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        DataState.current_user_email,
                        class_name="text-sm text-gray-600",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Loyalty: Gold",
                            class_name="px-2 py-0.5 text-xs font-medium bg-amber-100 text-amber-700 rounded-full",
                        ),
                        rx.el.span(
                            "Member since 2023",
                            class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full",
                        ),
                        class_name="flex gap-2 mt-2",
                    ),
                ),
                rx.el.button(
                    "Edit profile",
                    class_name="ml-auto px-4 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50",
                ),
                class_name="flex items-center gap-4 p-5 bg-white border border-gray-200 rounded-xl mb-6",
            ),
            rx.el.div(
                profile_field("Email", DataState.current_user_email, "mail"),
                profile_field("Phone", "(212) 555-0117", "phone"),
                profile_field("Location", "New York, NY", "map-pin"),
                profile_field("Preferred stylist", "Amelia Rivera", "user"),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
            ),
            rx.el.div(
                rx.el.h3(
                    "Preferences",
                    class_name="text-base font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        [
                            "Email reminders",
                            "SMS reminders",
                            "Marketing emails",
                            "Waitlist alerts",
                        ],
                        lambda label: rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                default_checked=True,
                                class_name="h-4 w-4 rounded border-gray-300 text-blue-600",
                            ),
                            rx.el.span(
                                label, class_name="text-sm text-gray-700"
                            ),
                            class_name="flex items-center gap-2",
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                ),
                class_name="p-5 bg-white border border-gray-200 rounded-xl mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Notifications",
                        class_name="text-base font-bold text-gray-900",
                    ),
                    rx.el.span(
                        f"{DataState.unread_notifications_count} unread",
                        class_name="px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full w-fit",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.foreach(DataState.my_notifications, notification_card),
                    class_name="space-y-2",
                ),
            ),
        ),
    )