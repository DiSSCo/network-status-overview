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
    z: list = []
    y_values: dict = {}

    print(publishing_country)

    for issue_flag in publishing_country['issues_and_flags']:
        # Check if issue flag number is high enough
        if len(y_values) < return_length:
            y_values[issue_flag] = int(publishing_country['issues_and_flags'][issue_flag]['total'])
        else:
            # Check if some value in y is lower, if true remove and add new one
            y_values = check_for_hottest_issues(y_values, publishing_country, issue_flag)

    sorted_y = sorted(y_values.items(), key=lambda t: t[1], reverse=True)

    # Refactoring y values to list and setting x values
    for issue_flag in sorted_y:
        percentage = round(int(publishing_country['issues_and_flags'][issue_flag[0]]['total']) / int(publishing_country['Total']) * 100, 2)

        x.append(issue_flag[0])
        y.append(issue_flag[1])
        z.append(f"{issue_flag[1]} ({percentage}%)")

    return [x, y, z]


def prepare_draw_issues_flags_organisation(publisher, return_length) -> list:
    # Set y values
    x: list = []
    y: list = []
    z: list = []
    y_values: dict = {}

    for issue_flag in publisher['issues_and_flags']:
        # Check if issue flag number is high enough
        if len(y_values) < return_length:
            y_values[issue_flag] = int(publisher['issues_and_flags'][issue_flag]['total'])
        else:
            y_values =check_for_hottest_issues(y_values, publisher, issue_flag)

    sorted_y = sorted(y_values.items(), key=lambda t: t[1], reverse=True)

    # Refactoring y values to list and setting x values
    for issue_flag in sorted_y:
        percentage = round(int(publisher['issues_and_flags'][issue_flag[0]]['total']) / int(
            publisher['Total']) * 100, 2)

        x.append(issue_flag[0])
        y.append(issue_flag[1])
        z.append(f"{issue_flag[1]} ({percentage}%)")

    return [x, y, z]
