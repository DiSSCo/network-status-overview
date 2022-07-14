from sqlalchemy import Table, Column, MetaData, Integer, String, DATETIME, Date, JSON


def countries_model() -> Table:
    """ Model for countries table of database
        :return: Returns the model
    """

    metadata = MetaData()

    countries = Table(
        'countries',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('country_code', String(3), nullable=False),
        Column('country_name', String(60), nullable=False),
        Column('last_updated', DATETIME, nullable=False),
        Column('datasets_count', JSON, nullable=True),
        Column('specimens_count', JSON, nullable=True),
        Column('issues_flags', JSON, nullable=True),
        Column('static_date', Date, nullable=False)
    )

    return countries
