"""create event model

Revision ID: bebc68bfaf07
Revises: ef1d775276c0
Create Date: 2025-04-18 01:22:39.485807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bebc68bfaf07'
down_revision: Union[str, None] = 'ef1d775276c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('bio', sa.String(length=500), nullable=True),
    sa.Column('profile_picture_url', sa.String(length=255), nullable=True),
    sa.Column('linkedin_profile_url', sa.String(length=255), nullable=True),
    sa.Column('github_profile_url', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('ANONYMOUS', 'AUTHENTICATED', 'MANAGER', 'ADMIN', name='UserRole'), nullable=False),
    sa.Column('is_professional', sa.Boolean(), nullable=True),
    sa.Column('professional_status_updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('failed_login_attempts', sa.Integer(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('verification_token', sa.String(), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_nickname'), 'users', ['nickname'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_nickname'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
