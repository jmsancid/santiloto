from __future__ import annotations
from datetime import date
from .types import WeeklyResult  # lo creamos en el siguiente paso si aún no existe


_ES_DAYS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

def _fmt_day(d: date) -> str:
    return f"{_ES_DAYS[d.weekday()]} {d.isoformat()}"

def _fmt_nums(nums) -> str:
    return " ".join(f"{n:02d}" for n in nums)

def _fmt_euro_combo(combo) -> str:
    nums, stars = combo
    nums_s = _fmt_nums(sorted(nums))
    e1, e2 = sorted(stars)
    return f"{nums_s} ⭐ {e1:02d} {e2:02d}"

def _fmt_reintegro(value) -> str:
    if value is None:
        return "Sin reintegro"
    return str(int(value))

def format_weekly_result(weekly: WeeklyResult) -> str:
    ws = weekly.week_start.isoformat() if weekly.week_start else "?"
    we = weekly.week_end.isoformat() if weekly.week_end else "?"
    lines = [f"🗓 Semana {ws} → {we}", ""]

    lines.append("🎯 PRIMITIVA (Madrid)")
    if weekly.apuestas_primitiva:
        for d, ap in weekly.apuestas_primitiva:
            lines.append(f"📌 {_fmt_day(d)}  |  Reintegro: {_fmt_reintegro(ap.reintegro)}")
            for i, combo in enumerate(ap.combinaciones, 1):
                lines.append(f"  {i}) {_fmt_nums(combo)}")
            lines.append("")
    else:
        lines.append("  (sin apuestas generadas)")
        lines.append("")

    lines.append("🎯 EUROMILLONES (París)")
    if weekly.apuestas_euromillones:
        for d, ap in weekly.apuestas_euromillones:
            lines.append(f"📌 {_fmt_day(d)}")
            for i, combo in enumerate(ap.combinaciones, 1):
                lines.append(f"  {i}) {_fmt_euro_combo(combo)}")
            lines.append("")
    else:
        lines.append("  (sin apuestas generadas)")
        lines.append("")

    return "\n".join(lines).rstrip()
