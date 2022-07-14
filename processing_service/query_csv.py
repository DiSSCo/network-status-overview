import csv
from datetime import datetime as dt


current_month = dt.now().strftime('%B')


# General functions for returning requested data
def create_issues_and_flags_list() -> list:
    """ Takes the csv containing the names of all issues and converts it to a list
        :return: Returns the issues and flags list
    """

    issues_file = './sources/GBIF_issues.csv'
    issues_and_flags_list = []

    with open(issues_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            issue_flag = row[1].lower().replace('_', ' ').capitalize()

            issues_and_flags_list.append(issue_flag)

    return issues_and_flags_list
