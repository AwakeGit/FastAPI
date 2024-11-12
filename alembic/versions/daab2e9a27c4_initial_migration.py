"""Initial migration

Revision ID: daab2e9a27c4
Revises: 
Create Date: 2024-11-08 00:48:57.492804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daab2e9a27c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_documents_date'), 'documents', ['date'], unique=False)
    op.create_table('documents_text',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_doc', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['id_doc'], ['documents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents_text')
    op.drop_index(op.f('ix_documents_date'), table_name='documents')
    op.drop_table('documents')
    # ### end Alembic commands ###
