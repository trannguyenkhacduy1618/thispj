"""Initial migration: create users, boards, tasks, time_entries

Revision ID: 0001_initial
Revises:
Create Date: 2025-12-14 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Users table ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String(20), unique=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(10), nullable=False, default='user'),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    )

    # ### Boards table ###
    op.create_table(
        'boards',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_public', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    )

    # ### Tasks table ###
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('board_id', sa.Integer, sa.ForeignKey('boards.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, default='todo'),
        sa.Column('priority', sa.String(20), nullable=False, default='medium'),
        sa.Column('assigned_to', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('position', sa.Integer, nullable=False, default=0),
        sa.Column('due_date', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    )

    # ### Time Entries table ###
    op.create_table(
        'time_entries',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=True),
        sa.Column('duration', sa.Integer, nullable=True),  # duration in seconds
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    )


def downgrade() -> None:
    op.drop_table('time_entries')
    op.drop_table('tasks')
    op.drop_table('boards')
    op.drop_table('users')
