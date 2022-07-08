from api import query_database
from datetime import datetime as dt


def prepare_draw_issues_flags_progress_country(quarter_months, monthly_progress) -> list:
    x: list = []
    y: list = []

    for month in quarter_months:
        x.append(month)
        month_number = dt.strptime(month, "%B").month

        y.append(monthly_progress['monthly_progress'][str(month_number)])

    return [x, y]


def prepare_draw_issues_flags_progress_organisation(quarter_months, monthly_progress) -> list:
    x: list = []
    y: list = []

    for month in quarter_months:
        x.append(month)
        month_number = dt.strptime(month, "%B").month

        y.append(monthly_progress['monthly_progress'][month_number])

    return [x, y]
