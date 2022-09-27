"""Add all players

Revision ID: e3055eae9271
Revises: 27cd3992716a
Create Date: 2022-09-25 21:45:30.278506

"""
from alembic import op
import sqlalchemy as sa
import pandas as pd
from botm.joueurs.models import Joueurs


# revision identifiers, used by Alembic.
revision = 'e3055eae9271'
down_revision = '27cd3992716a'
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
    joueurs = pd.read_csv('player.tsv', sep='\t')
    for i in range(len(joueurs)):
        j = Joueurs(i, joueurs['Pseudo'][i], joueurs['Points'][i], joueurs['Picks'][i])
        session.add(j)

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    joueurs = pd.read_csv('player.tsv', sep='\t')
    for i in range(len(joueurs)):
        j = session.query(Joueurs).filter(Joueurs.id_j == i).first()
        session.delete(j)

    session.commit()
