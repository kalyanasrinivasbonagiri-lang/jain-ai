from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


try:
    IST_TIMEZONE = ZoneInfo("Asia/Kolkata")
except ZoneInfoNotFoundError:
    IST_TIMEZONE = timezone(timedelta(hours=5, minutes=30))
MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def get_today(tz=IST_TIMEZONE):
    return datetime.now(tz).date()


def format_date_label(value):
    return f"{value.day} {MONTH_NAMES[value.month]} {value.year}"


def month_year_label(value):
    return f"{MONTH_NAMES[value.month]} {value.year}"


def expand_temporal_query(query, today=None):
    normalized = " ".join((query or "").split()).strip()
    if not normalized:
        return normalized

    lower_query = normalized.lower()
    today = today or get_today()
    additions = []

    if "this week" in lower_query:
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        additions.extend((
            f"week from {format_date_label(week_start)} to {format_date_label(week_end)}",
            month_year_label(week_start),
        ))
        if week_end.month != week_start.month or week_end.year != week_start.year:
            additions.append(month_year_label(week_end))

    if "next week" in lower_query:
        week_start = today - timedelta(days=today.weekday()) + timedelta(days=7)
        week_end = week_start + timedelta(days=6)
        additions.extend((
            f"week from {format_date_label(week_start)} to {format_date_label(week_end)}",
            month_year_label(week_start),
        ))
        if week_end.month != week_start.month or week_end.year != week_start.year:
            additions.append(month_year_label(week_end))

    if "this month" in lower_query:
        additions.append(month_year_label(today))

    if "next month" in lower_query:
        if today.month == 12:
            next_month = date(today.year + 1, 1, 1)
        else:
            next_month = date(today.year, today.month + 1, 1)
        additions.append(month_year_label(next_month))

    if "today" in lower_query:
        additions.extend((format_date_label(today), month_year_label(today)))

    if "tomorrow" in lower_query:
        tomorrow = today + timedelta(days=1)
        additions.extend((format_date_label(tomorrow), month_year_label(tomorrow)))

    if "yesterday" in lower_query:
        yesterday = today - timedelta(days=1)
        additions.extend((format_date_label(yesterday), month_year_label(yesterday)))

    deduped = []
    seen = set()
    existing_text = lower_query

    for addition in additions:
        lowered = addition.lower()
        if lowered in existing_text or lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(addition)

    if not deduped:
        return normalized

    return f"{normalized} ({'; '.join(deduped)})"
