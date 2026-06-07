from constants import PRIMITIVA, EUROMILLONES
from other_utils.file_utils import need_db_update, actualizacion_db


def update_all() -> bool:
    """
    Actualiza las tablas de resultados de Euromillones y Primitiva si procede.

    Returns:
        True si se ha actualizado al menos un sorteo, False en caso contrario.
    """
    updated = False

    if need_db_update(EUROMILLONES):
        if actualizacion_db(EUROMILLONES):
            print("Euromillones actualizado")
            updated = True
        else:
            print("Error actualizando Euromillones")
    else:
        print("Euromillones al día")

    if need_db_update(PRIMITIVA):
        if actualizacion_db(PRIMITIVA):
            print("Primitiva actualizada")
            updated = True
        else:
            print("Error actualizando Primitiva")
    else:
        print("Primitiva al día")

    return updated


def main() -> int:
    update_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
