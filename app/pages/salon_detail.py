import reflex as rx
from app.components.layout import page_layout
from app.states.data_state import DataState
from app.states.booking_state import BookingState


class SalonDetailState(rx.State):
    @rx.var
    def salon_id(self) -> str:
        return self.router.page.params.get("id", "s1")

    @rx.var
    async def salon(self) -> dict:
        data = await self.get_state(DataState)
        for s in data.salons:
            if s["id"] == self.salon_id:
                return dict(s)
        return dict(data.salons[0])

    @rx.var
    async def salon_practitioners(self) -> list[dict]:
        data = await self.get_state(DataState)
        return [
            dict(p)
            for p in data.practitioners
            if p["salon_id"] == self.salon_id
        ]

    @rx.var
    async def salon_reviews(self) -> list[dict]:
        data = await self.get_state(DataState)
        return [dict(r) for r in data.reviews if r["salon_id"] == self.salon_id]


def practitioner_mini(p: dict) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={p['avatar_seed']}",
            class_name="h-14 w-14 rounded-full bg-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                p["name"], class_name="text-sm font-semibold text-gray-900"
            ),
            rx.el.p(p["title"], class_name="text-xs text-gray-500"),
            rx.el.div(
                rx.icon(
                    "star", class_name="h-3 w-3 fill-amber-400 text-amber-400"
                ),
                rx.el.span(
                    p["rating"].to_string(), class_name="text-xs font-medium"
                ),
                rx.el.span(
                    f"· {p['reviews']} reviews",
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex items-center gap-1 mt-0.5",
            ),
        ),
        class_name="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg",
    )


def review_item(r: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    r["customer"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"with {r['practitioner']}",
                    class_name="text-xs text-gray-500",
                ),
            ),
            rx.el.div(
                rx.icon(
                    "star",
                    class_name="h-3.5 w-3.5 fill-amber-400 text-amber-400",
                ),
                rx.el.span(
                    r["rating"].to_string(), class_name="text-sm font-semibold"
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-start justify-between mb-2",
        ),
        rx.el.p(r["comment"], class_name="text-sm text-gray-700"),
        rx.el.p(r["date"], class_name="text-xs text-gray-400 mt-2"),
        class_name="bg-white border border-gray-200 rounded-lg p-4",
    )


def salon_detail_page() -> rx.Component:
    return page_layout(
        rx.el.a(
            rx.icon("arrow-left", class_name="h-4 w-4"),
            "Back to discovery",
            href="/",
            class_name="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("sparkles", class_name="h-16 w-16 text-blue-300"),
                class_name="h-56 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl flex items-center justify-center mb-6 border border-gray-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        SalonDetailState.salon["name"],
                        class_name="text-3xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.div(
                        rx.icon("map-pin", class_name="h-4 w-4 text-gray-400"),
                        rx.el.span(
                            SalonDetailState.salon["address"],
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.span("·", class_name="text-gray-400"),
                        rx.el.span(
                            SalonDetailState.salon["city"],
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="flex items-center gap-2 mb-2",
                    ),
                    rx.el.div(
                        rx.icon("clock", class_name="h-4 w-4 text-gray-400"),
                        rx.el.span(
                            SalonDetailState.salon["hours"],
                            class_name="text-sm text-gray-600",
                        ),
                        rx.el.span("·", class_name="text-gray-400"),
                        rx.el.span(
                            SalonDetailState.salon["phone"],
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="flex items-center gap-2 mb-3",
                    ),
                    rx.el.p(
                        SalonDetailState.salon["description"],
                        class_name="text-gray-700",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("calendar-plus", class_name="h-4 w-4"),
                        "Book now",
                        on_click=lambda: BookingState.start_booking(
                            SalonDetailState.salon["id"].to(str),
                            SalonDetailState.salon["name"].to(str),
                        ),
                        class_name="flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg",
                    ),
                    rx.el.button(
                        rx.icon("list-plus", class_name="h-4 w-4"),
                        "Join waitlist",
                        on_click=lambda: DataState.enroll_waitlist(
                            SalonDetailState.salon["name"].to(str),
                            "Any service",
                            "2025-02-25",
                        ),
                        class_name="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 font-medium rounded-lg",
                    ),
                    class_name="flex gap-2",
                ),
                class_name="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Practitioners",
                        class_name="text-xl font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            SalonDetailState.salon_practitioners,
                            practitioner_mini,
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Recent reviews",
                        class_name="text-xl font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(SalonDetailState.salon_reviews, review_item),
                        class_name="space-y-3",
                    ),
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
        ),
    )