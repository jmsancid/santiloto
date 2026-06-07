# webapi/schemas.py
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class WeeklyMetaV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["v1"] = "v1"
    # OJO: opcional para no romper determinismo
    generated_at: Optional[datetime] = Field(
        default=None,
        description="marca de tiempo UTC (opcional; si se usa, rompe determinismo del body)",
    )
    source: Literal["runtime"] = "runtime"


class WeeklyApuestaEntryV1(BaseModel):
    """
    Una apuesta asociada a la fecha del sorteo.
    payload contiene la estructura serializada de Apuesta_* (estable como JSON).
    """
    model_config = ConfigDict(extra="forbid")

    draw_date: date
    payload: dict[str, Any]


class WeeklyResponseV1(BaseModel):
    """
    Contrato público del endpoint /weekly (v1).
    No debe cambiar sin versionado.
    """
    model_config = ConfigDict(extra="forbid")

    version: Literal["v1"] = "v1"
    method_version: str = "v1"

    primitiva_dates: list[date]
    euromillones_dates: list[date]

    apuestas_primitiva: list[WeeklyApuestaEntryV1]
    apuestas_euromillones: list[WeeklyApuestaEntryV1]

    week_start: Optional[date] = None
    week_end: Optional[date] = None

    tol_primitiva: Optional[float] = None
    tol_euro: Optional[float] = None

    meta: WeeklyMetaV1

