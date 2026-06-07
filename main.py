#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scripts.update_db import update_all
from scripts.run_weekly import main as run_weekly_main


def main() -> int:
    update_all()
    return run_weekly_main()


if __name__ == "__main__":
    raise SystemExit(main())
