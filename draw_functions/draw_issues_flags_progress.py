import query_database
import calendar


def prepare_draw_issues_flags_progress_country(quarter_months, country_code, issue_flag) -> list:
    x: list = []
    y: list = []
    months = list(calendar.month_name)[1:]

    for month in quarter_months:
        x.append(months[month - 1])
        month_data = query_database.select_countries_data([country_code], month)

        if country_code in month_data:
            # Read csv from month and set values
            y.append(month_data[country_code]['issues_and_flags'][issue_flag]['total'])
        else:
            # Set values to zero
            y.append(0)

    return [x, y]


def prepare_draw_issues_flags_progress_organisation(quarter_months, ror_id, issue_flag) -> list:
    x: list = []
    y: list = []
    months = list(calendar.month_name)[1:]

    for month in quarter_months:
        x.append(months[month - 1])
        month_data = query_database.select_organisations_data([ror_id], month)

        if ror_id in month_data:
            # Read csv from month and set values
            y.append(month_data[ror_id]['issues_and_flags'][issue_flag]['total'])
        else:
            # Set values to zero
            y.append(0)

    return [x, y]
