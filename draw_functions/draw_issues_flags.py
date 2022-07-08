def check_for_hottest_issues(y_values, data, issue_flag) -> dict:
    # Check if some value in y is lower, if true remove and add new one
    difference = {}

    for value in y_values:
        if y_values[value] < int(data['issues_and_flags'][issue_flag]['total']):
            difference[value] = int(y_values[value]) - int(data['issues_and_flags'][issue_flag]['total'])

    # Check if any issue or flag is greater than existing value
    if len(difference) != 0:
        smallest = 0
        smallest_issue_flag = ''

        for value in difference:
            if smallest == 0 or smallest > difference[value]:
                smallest = difference[value]
                smallest_issue_flag = value

        del y_values[smallest_issue_flag]
        y_values[issue_flag] = int(data['issues_and_flags'][issue_flag]['total'])

    return y_values


def prepare_draw_issues_flags_countries(publishing_country, return_length) -> list:
    x: list = []
    y: list = []
    y_values: dict = {}

    for issue_flag in publishing_country['issues_and_flags']:
        # Check if issue flag number is high enough
        if len(y_values) < return_length:
            y_values[issue_flag] = int(publishing_country['issues_and_flags'][issue_flag]['total'])
        else:
            # Check if some value in y is lower, if true remove and add new one
            y_values = check_for_hottest_issues(y_values, publishing_country, issue_flag)

    # Refactoring y values to list and setting x values
    for issue_flag in y_values:
        x.append(issue_flag)
        y.append(y_values[issue_flag])

    return [x, y]


def prepare_draw_issues_flags_organisation(publisher, return_length) -> list:
    # Set y values
    x: list = []
    y: list = []
    y_values: dict = {}

    for issue_flag in publisher['issues_and_flags']:
        # Check if issue flag number is high enough
        if len(y_values) < return_length:
            y_values[issue_flag] = int(publisher['issues_and_flags'][issue_flag]['total'])
        else:
            y_values =check_for_hottest_issues(y_values, publisher, issue_flag)

    # Refactoring y values to list and setting x values
    for issue_flag in y_values:
        x.append(issue_flag)
        y.append(y_values[issue_flag])

    return [x, y]
