"""Утилиты для генерации тестовых периодов."""
from datetime import datetime, timedelta
from typing import Dict


def tz_offset() -> str:
    """Смещение локального часового пояса в формате +HH:MM."""
    offset: str = datetime.now().astimezone().strftime("%z")
    return f"{offset[:3]}:{offset[3:]}"


def next_day_period() -> Dict[str, str]:
    """Диапазон на завтра: дата, время начала/окончания и границы периода."""
    day: str = (datetime.now().astimezone() + timedelta(days=1)).strftime("%Y-%m-%d")
    tz: str = tz_offset()
    return {
        "date": day,
        "start": f"{day}T10:00:00{tz}",
        "end": f"{day}T11:00:00{tz}",
        "from": f"{day}T00:00:00{tz}",
        "till": f"{day}T23:59:59{tz}",
    }