from datetime import date
import os

from db_utils.db_management import DBManager
from other_utils.weekly import generate_weekly, format_weekly
from other_utils.file_utils import check_results_db_file


def _today() -> date:
    if "SANTILOTO_TODAY" in os.environ:
        return date.fromisoformat(os.environ["SANTILOTO_TODAY"])
    return date.today()


def main() -> int:
    db_path = check_results_db_file()
    if not db_path:
        raise FileNotFoundError("DB no encontrada")

    db = DBManager(db_path)
    today = _today()

    with db:
        db.sync_sorteo_influencers()

    result = generate_weekly(db=db, today=today)

    print("===WEEKLY_RESULT_BEGIN===")
    print(format_weekly(result))
    print("===WEEKLY_RESULT_END===")

    with db:
        db.upsert_santi_primitiva(
            result.apuestas_primitiva,
            week_start=result.week_start,
            week_end=result.week_end,
            tol_frac=result.tol_primitiva,
            method_version="v1",
            city="Madrid",
        )
        db.upsert_santi_euromillones(
            result.apuestas_euromillones,
            week_start=result.week_start,
            week_end=result.week_end,
            tol_frac=result.tol_euro,
            method_version="v1",
            city="Paris",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
