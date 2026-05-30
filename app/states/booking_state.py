import reflex as rx
import uuid
from datetime import datetime, timedelta
from app.states.data_state import DataState, slots_for


TIME_SLOTS: list[str] = [
    f"{h:02d}:{m:02d}" for h in range(9, 18) for m in (0, 30)
]


class BookingState(rx.State):
    step: int = 1
    selected_salon_id: str = ""
    selected_salon_name: str = ""
    selected_service_id: str = ""
    selected_service_name: str = ""
    selected_service_price: float = 0.0
    selected_service_duration: int = 0
    selected_practitioner_id: str = ""
    selected_practitioner_name: str = ""
    selected_date: str = "2025-02-20"
    selected_time: str = ""
    notes: str = ""
    active_reservation_id: str = ""
    reservation_expires_at: str = ""

    time_slots: list[str] = TIME_SLOTS

    @rx.var
    async def blocked_slots(self) -> list[str]:
        if not self.selected_practitioner_name:
            return []
        data = await self.get_state(DataState)
        return list(
            data.get_blocked_slots(
                self.selected_practitioner_name, self.selected_date
            )
        )

    @rx.var
    async def slot_status_map(self) -> dict[str, str]:
        """Returns slot -> 'available' | 'blocked' | 'cant-fit'"""
        if not self.selected_practitioner_name:
            return {s: "available" for s in TIME_SLOTS}
        data = await self.get_state(DataState)
        blocked = data.get_blocked_slots(
            self.selected_practitioner_name, self.selected_date
        )
        result: dict[str, str] = {}
        duration = self.selected_service_duration or 30
        needed = (duration + 29) // 30
        for i, s in enumerate(TIME_SLOTS):
            if s in blocked:
                result[s] = "blocked"
            else:
                # Check if remaining slots fit the service
                ok = i + needed <= len(TIME_SLOTS)
                if ok:
                    needed_slots = slots_for(s, duration)
                    for ns in needed_slots:
                        if ns not in TIME_SLOTS:
                            ok = False
                            break
                        if ns in blocked:
                            ok = False
                            break
                result[s] = "available" if ok else "cant-fit"
        return result

    @rx.event
    def start_booking(self, salon_id: str, salon_name: str):
        self.selected_salon_id = salon_id
        self.selected_salon_name = salon_name
        self.step = 1
        self.selected_service_id = ""
        self.selected_practitioner_id = ""
        self.selected_time = ""
        self.active_reservation_id = ""
        return rx.redirect("/book")

    @rx.event
    def select_service(self, sid: str, name: str, price: float, duration: int):
        self.selected_service_id = sid
        self.selected_service_name = name
        self.selected_service_price = price
        self.selected_service_duration = duration
        self.step = 2

    @rx.event
    def select_practitioner(self, pid: str, name: str):
        self.selected_practitioner_id = pid
        self.selected_practitioner_name = name
        self.step = 3

    @rx.event
    async def select_time(self, t: str):
        self.selected_time = t
        # Create or update reservation hold
        data = await self.get_state(DataState)
        # Release any prior active reservation by this user
        for r in data.reservations:
            if (
                r["customer"] == data.current_user
                and r["status"] == "Active"
                and r["id"] == self.active_reservation_id
            ):
                r["status"] = "Released"
        # Validate conflict
        needed = slots_for(t, self.selected_service_duration)
        blocked = data.get_blocked_slots(
            self.selected_practitioner_name, self.selected_date
        )
        if any(s in blocked for s in needed) or any(
            s not in TIME_SLOTS for s in needed
        ):
            yield rx.toast.error("That time conflicts with another booking")
            return
        rid = f"rv{uuid.uuid4().hex[:6]}"
        expires = (datetime.now() + timedelta(minutes=10)).strftime(
            "%Y-%m-%d %H:%M"
        )
        data.reservations.insert(
            0,
            {
                "id": rid,
                "customer": data.current_user,
                "salon_id": self.selected_salon_id,
                "salon_name": self.selected_salon_name,
                "practitioner": self.selected_practitioner_name,
                "service_id": self.selected_service_id,
                "service_name": self.selected_service_name,
                "date": self.selected_date,
                "time": t,
                "duration_min": self.selected_service_duration,
                "price": self.selected_service_price,
                "blocked_slots": needed,
                "status": "Active",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "expires_at": expires,
            },
        )
        self.active_reservation_id = rid
        self.reservation_expires_at = expires

    @rx.event
    def set_date(self, d: str):
        self.selected_date = d

    @rx.event
    def set_notes(self, n: str):
        self.notes = n

    @rx.event
    def go_to_step(self, s: int):
        self.step = s

    @rx.event
    def next_step(self):
        if self.step < 4:
            self.step += 1

    @rx.event
    def prev_step(self):
        if self.step > 1:
            self.step -= 1

    @rx.event
    async def confirm_booking(self):
        data = await self.get_state(DataState)
        if not self.selected_time:
            yield rx.toast.error("Please select a time slot")
            return
        # Final conflict revalidation
        needed = slots_for(self.selected_time, self.selected_service_duration)
        blocked = data.get_blocked_slots(
            self.selected_practitioner_name, self.selected_date
        )
        # Exclude our own active reservation slots from blocked check
        for r in data.reservations:
            if r["id"] == self.active_reservation_id:
                for s in r["blocked_slots"]:
                    blocked.discard(s)
        if any(s in blocked for s in needed):
            yield rx.toast.error(
                "That time was just taken. Please pick another slot."
            )
            return
        new_id = f"a{uuid.uuid4().hex[:6]}"
        deposit = round(self.selected_service_price * 0.3, 2)
        data.appointments.append(
            {
                "id": new_id,
                "customer": data.current_user,
                "salon_id": self.selected_salon_id,
                "salon_name": self.selected_salon_name,
                "practitioner": self.selected_practitioner_name,
                "service": self.selected_service_name,
                "date": self.selected_date,
                "time": self.selected_time,
                "duration_min": self.selected_service_duration,
                "price": self.selected_service_price,
                "status": "Confirmed",
                "payment_status": "Deposit Paid",
            }
        )
        # Confirm reservation
        for r in data.reservations:
            if r["id"] == self.active_reservation_id:
                r["status"] = "Confirmed"
        # Payment record
        data._add_payment(
            data.current_user,
            deposit,
            "Deposit",
            "Captured",
            new_id,
        )
        # Notifications: confirmation, invoice, reminder
        data._add_notification(
            data.current_user,
            "Confirmation",
            "Booking confirmed",
            f"{self.selected_service_name} with {self.selected_practitioner_name} on {self.selected_date} at {self.selected_time}.",
            new_id,
        )
        data._add_notification(
            data.current_user,
            "Invoice",
            "Deposit invoice",
            f"Deposit of ${deposit:.2f} captured for your booking. Balance ${self.selected_service_price - deposit:.2f} due at salon.",
            new_id,
        )
        data._add_notification(
            data.current_user,
            "Reminder",
            "Reminder set",
            f"We'll remind you 24 hours before your {self.selected_date} appointment.",
            new_id,
        )
        data._add_activity(
            data.current_user,
            "Booked appointment",
            f"{self.selected_service_name} @ {self.selected_salon_name}",
        )
        self.step = 1
        self.selected_service_id = ""
        self.selected_practitioner_id = ""
        self.selected_time = ""
        self.active_reservation_id = ""
        yield rx.toast.success("Appointment booked successfully!")
        yield rx.redirect("/appointments")