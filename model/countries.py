from sqlalchemy import Table, Column, MetaData, Integer, String, DATETIME, JSON


def countries_model():
    metadata = MetaData()

    countries = Table(
        'countries',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('country_code', String(3), nullable=False),
        Column('country_name', String(60), nullable=False),
        Column('last_updated', DATETIME),
        Column('datasets_count', JSON, nullable=True),
        Column('specimens_count', JSON, nullable=True),
        Column('issues_flags', JSON, nullable=True),
        Column('month', String, nullable=False)
    )

    return countries
