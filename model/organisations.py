from sqlalchemy import Table, Column, MetaData, Integer, String, DATETIME, Date, JSON


def organisations_model():
    metadata = MetaData()

    organisations = Table(
        'organisations',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('ror_id', String(50), nullable=False),
        Column('organisation_name', String(200), nullable=False),
        Column('last_updated', DATETIME, nullable=False),
        Column('datasets_count', JSON, nullable=True),
        Column('specimens_count', JSON, nullable=True),
        Column('issues_flags', JSON, nullable=True),
        Column('static_date', Date, nullable=False)
    )

    return organisations
