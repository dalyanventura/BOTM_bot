"""empty message

Revision ID: b71243e2551d
Revises: 
Create Date: 2022-09-25 21:24:25.958350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b71243e2551d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CartesJoueurs')
    op.drop_table('Joueurs')
    op.drop_table('Cartes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Cartes',
    sa.Column('id_carte', sa.INTEGER(), server_default=sa.text('nextval(\'"Cartes_id_carte_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('nom', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('niveau', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('univers', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('force', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('mana', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vitesse', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('popularite', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('prix', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('image', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_carte', name='Cartes_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('Joueurs',
    sa.Column('id_j', sa.INTEGER(), server_default=sa.text('nextval(\'"Joueurs_id_j_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('pseudo', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('points', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pick_nb', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_j', name='Joueurs_pkey')
    )
    op.create_table('CartesJoueurs',
                    sa.Column('id_carte', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('id_j', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('nb_cartes', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['id_carte'], ['Cartes.id_carte'], name='CartesJoueurs_id_carte_fkey'),
                    sa.ForeignKeyConstraint(['id_j'], ['Joueurs.id_j'], name='CartesJoueurs_id_j_fkey'),
                    sa.PrimaryKeyConstraint('id_carte', 'id_j', name='CartesJoueurs_pkey')
                    )
    # ### end Alembic commands ###
