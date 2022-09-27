"""Add all cards

Revision ID: de5e2abdd9de
Revises: e3055eae9271
Create Date: 2022-09-25 21:54:01.737123

"""
from alembic import op
import sqlalchemy as sa
import pandas as pd
from botm.cartes.models import Cartes


# revision identifiers, used by Alembic.
revision = 'de5e2abdd9de'
down_revision = 'e3055eae9271'
branch_labels = None
depends_on = None

import numpy
from psycopg2.extensions import register_adapter, AsIs

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    cartes = pd.read_csv('cartes.tsv', sep='\t')
    for i in range(len(cartes)):
        c = Cartes(i, cartes['Nom'][i], cartes['Univers'][i], cartes['Niveau'][i], cartes['Force'][i],
                   cartes['Mana'][i], cartes['Vitesse'][i], cartes['Popularité'][i], cartes['Prix'][i],
                   cartes['Image'][i])
        session.add(c)

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    cartes = pd.read_csv('cartes.tsv', sep='\t')
    for i in range(len(cartes)):
        j = session.query(Cartes).filter(Cartes.id_j == i).first()
        session.delete(j)

    session.commit()
