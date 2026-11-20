
import json
import os
from datetime import datetime, timedelta


# ==========================================================
# ORIRI — ALARM MANAGER
# Alarm Scheduling and Management
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")
ALARM_FILE = os.path.join(DATA_DIR, "alarms.json")

DAYS = [
    "Mon", "Tue", "Wed",
    "Thu", "Fri", "Sat", "Sun"
]

SNOOZE_MINUTES = 5


class AlarmManager:

    def __init__(self, file_path=ALARM_FILE):
        self.file_path = file_path
        self.alarms = []
        self.triggered = set()
        self.snoozed = []

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        self.load_alarms()

    # ------------------------------------------------------
    # LOAD ALARMS
    # ------------------------------------------------------

    def load_alarms(self):

        if not os.path.exists(self.file_path):
            self.alarms = []
            self.save_alarms()
            return self.alarms

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            self.alarms = data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            self.alarms = []

        return self.alarms

    # ------------------------------------------------------
    # SAVE ALARMS
    # ------------------------------------------------------

    def save_alarms(self):

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.alarms,
                file,
                indent=4,
                ensure_ascii=False
            )

    # ------------------------------------------------------
    # ADD ALARM
    # ------------------------------------------------------

    def add_alarm(self, alarm):

        validated = self.validate_alarm(alarm)

        self.alarms.append(validated)
        self.save_alarms()

        return validated

    # ------------------------------------------------------
    # UPDATE ALARM
    # ------------------------------------------------------

    def update_alarm(self, index, alarm):

        if not self.valid_index(index):
            return False

        validated = self.validate_alarm(alarm)

        self.alarms[index] = validated
        self.save_alarms()

        return True

    # ------------------------------------------------------
    # DELETE ALARM
    # ------------------------------------------------------

    def delete_alarm(self, index):

        if not self.valid_index(index):
            return False

        del self.alarms[index]
        self.save_alarms()

        return True

    # ------------------------------------------------------
    # ENABLE / DISABLE
    # ------------------------------------------------------

    def toggle_alarm(self, index, enabled):

        if not self.valid_index(index):
            return False

        self.alarms[index]["enabled"] = bool(enabled)
        self.save_alarms()

        return True

    # ------------------------------------------------------
    # VALIDATE ALARM
    # ------------------------------------------------------

    def validate_alarm(self, alarm):

        if not isinstance(alarm, dict):
            raise ValueError("Alarm must be a dictionary.")

        alarm_time = str(
            alarm.get("time", "07:00")
        ).strip()

        try:
            datetime.strptime(alarm_time, "%H:%M")
        except ValueError:
            raise ValueError(
                "Alarm time must use HH:MM format."
            )

        repeat = alarm.get("repeat", [])

        if not isinstance(repeat, list):
            raise ValueError("Repeat days must be a list.")

        repeat = [
            day for day in DAYS
            if day in repeat
        ]

        return {
            "time": alarm_time,
            "label": str(
                alarm.get("label", "Morning Alarm")
            ).strip() or "Morning Alarm",
            "note": str(alarm.get("note", "")).strip(),
            "repeat": repeat,
            "enabled": bool(alarm.get("enabled", True))
        }

    # ------------------------------------------------------
    # INDEX VALIDATION
    # ------------------------------------------------------

    def valid_index(self, index):

        return (
            isinstance(index, int)
            and 0 <= index < len(self.alarms)
        )

    # ------------------------------------------------------
    # GET ALARMS
    # ------------------------------------------------------

    def get_alarms(self):
        return self.alarms.copy()

    def get_active_alarms(self):

        return [
            alarm for alarm in self.alarms
            if alarm.get("enabled", True)
        ]

    # ------------------------------------------------------
    # CHECK REPEAT DAY
    # ------------------------------------------------------

    def should_repeat_today(self, alarm, date=None):

        date = date or datetime.now()
        repeat = alarm.get("repeat", [])

        # No selected days means a one-time alarm.
        # It is not automatically repeated.
        return DAYS[date.weekday()] in repeat

    # ------------------------------------------------------
    # CHECK SCHEDULED ALARMS
    # ------------------------------------------------------

    def check_alarms(self, current_time=None):

        now = current_time or datetime.now()
        triggered_alarms = []

        # Process snoozed alarms first.
        remaining_snoozes = []

        for item in self.snoozed:

            if now >= item["due"]:
                triggered_alarms.append(item["alarm"])
            else:
                remaining_snoozes.append(item)

        self.snoozed = remaining_snoozes

        # Check regular alarms.
        for index, alarm in enumerate(self.alarms):

            if not alarm.get("enabled", True):
                continue

            if alarm.get("repeat"):
                if not self.should_repeat_today(alarm, now):
                    continue

            else:
                # One-time alarms are checked on their saved date.
                # Legacy alarms without a date use today's date.
                saved_date = alarm.get(
                    "date",
                    now.strftime("%Y-%m-%d")
                )

                if saved_date != now.strftime("%Y-%m-%d"):
                    continue

            alarm_key = (
                index,
                now.strftime("%Y-%m-%d"),
                alarm["time"]
            )

            if alarm_key in self.triggered:
                continue

            if now.strftime("%H:%M") == alarm["time"]:

                triggered_alarms.append(alarm.copy())
                self.triggered.add(alarm_key)

        return triggered_alarms

    # ------------------------------------------------------
    # SNOOZE
    # ------------------------------------------------------

    def snooze_alarm(self, alarm, current_time=None):

        now = current_time or datetime.now()

        due_time = now + timedelta(
            minutes=SNOOZE_MINUTES
        )

        self.snoozed.append({
            "alarm": alarm.copy(),
            "due": due_time
        })

        return due_time

    # ------------------------------------------------------
    # CLEAR SNOOZES
    # ------------------------------------------------------

    def clear_snoozes(self):
        self.snoozed.clear()

    # ------------------------------------------------------
    # CLEAR ALL ALARMS
    # ------------------------------------------------------

    def clear_alarms(self):

        self.alarms.clear()
        self.triggered.clear()
        self.snoozed.clear()

        self.save_alarms()

    # ------------------------------------------------------
    # NEXT ALARM
    # ------------------------------------------------------

    def get_next_alarm(self, current_time=None):

        now = current_time or datetime.now()
        upcoming = []

        for alarm in self.alarms:

            if not alarm.get("enabled", True):
                continue

            hour, minute = map(
                int,
                alarm["time"].split(":")
            )

            if not alarm.get("repeat"):
                saved_date = alarm.get(
                    "date",
                    now.strftime("%Y-%m-%d")
                )

                try:
                    alarm_date = datetime.strptime(
                        saved_date,
                        "%Y-%m-%d"
                    ).date()
                except ValueError:
                    continue

                candidate = datetime.combine(
                    alarm_date,
                    datetime.min.time()
                ).replace(hour=hour, minute=minute)

                if candidate > now:
                    upcoming.append(candidate)

                continue

            for offset in range(8):

                candidate_date = (
                    now.date() + timedelta(days=offset)
                )

                if DAYS[candidate_date.weekday()] not in alarm["repeat"]:
                    continue

                candidate = datetime.combine(
                    candidate_date,
                    datetime.min.time()
                ).replace(hour=hour, minute=minute)

                if candidate > now:
                    upcoming.append(candidate)
                    break

        if not upcoming:
            return None

        return min(upcoming)
