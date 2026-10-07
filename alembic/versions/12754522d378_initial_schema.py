"""initial_schema

Revision ID: 12754522d378
Revises: 
Create Date: 2026-10-07 20:15:09.958526

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12754522d378'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # 2. projects
    op.create_table(
        'projects',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_projects_user_id', 'projects', ['user_id'])
    op.create_index('ix_projects_status', 'projects', ['status'])

    # 3. books
    op.create_table(
        'books',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('project_id', sa.String(length=36), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('subtitle', sa.String(length=255), nullable=True),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('academic_level', sa.String(length=50), nullable=True),
        sa.Column('target_audience', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('language', sa.String(length=20), nullable=True),
        sa.Column('book_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_books_project_id', 'books', ['project_id'])
    op.create_index('ix_books_status', 'books', ['status'])

    # 4. book_units
    op.create_table(
        'book_units',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, default=1),
        sa.Column('title', sa.String(length=255), nullable=False),
    )
    op.create_index('ix_book_units_book_id', 'book_units', ['book_id'])

    # 5. book_topics
    op.create_table(
        'book_topics',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('unit_id', sa.String(length=36), sa.ForeignKey('book_units.id'), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, default=1),
        sa.Column('title', sa.String(length=255), nullable=False),
    )
    op.create_index('ix_book_topics_unit_id', 'book_topics', ['unit_id'])

    # 6. book_subtopics
    op.create_table(
        'book_subtopics',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('topic_id', sa.String(length=36), sa.ForeignKey('book_topics.id'), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, default=1),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
    )
    op.create_index('ix_book_subtopics_topic_id', 'book_subtopics', ['topic_id'])
    op.create_index('ix_book_subtopics_status', 'book_subtopics', ['status'])

    # 7. generation_jobs
    op.create_table(
        'generation_jobs',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('progress', sa.Float(), nullable=True),
        sa.Column('current_stage', sa.String(length=100), nullable=True),
        sa.Column('current_item', sa.String(length=255), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_generation_jobs_book_id', 'generation_jobs', ['book_id'])
    op.create_index('ix_generation_jobs_status', 'generation_jobs', ['status'])

    # 8. generation_events
    op.create_table(
        'generation_events',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('job_id', sa.String(length=36), sa.ForeignKey('generation_jobs.id'), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('progress', sa.Float(), nullable=True),
        sa.Column('event_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_generation_events_job_id', 'generation_events', ['job_id'])
    op.create_index('ix_generation_events_event_type', 'generation_events', ['event_type'])
    op.create_index('ix_generation_events_created_at', 'generation_events', ['created_at'])

    # 9. generated_assets
    op.create_table(
        'generated_assets',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('job_id', sa.String(length=36), sa.ForeignKey('generation_jobs.id'), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('storage_key', sa.String(length=512), nullable=False),
        sa.Column('url', sa.String(length=1024), nullable=True),
        sa.Column('asset_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_generated_assets_book_id', 'generated_assets', ['book_id'])
    op.create_index('ix_generated_assets_job_id', 'generated_assets', ['job_id'])

    # 10. generated_sections
    op.create_table(
        'generated_sections',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('unit_id', sa.String(length=36), sa.ForeignKey('book_units.id'), nullable=True),
        sa.Column('topic_id', sa.String(length=36), sa.ForeignKey('book_topics.id'), nullable=True),
        sa.Column('subtopic_id', sa.String(length=36), sa.ForeignKey('book_subtopics.id'), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('review_status', sa.String(length=50), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_generated_sections_book_id', 'generated_sections', ['book_id'])
    op.create_index('ix_generated_sections_status', 'generated_sections', ['status'])
    op.create_index('idx_sections_book_subtopic', 'generated_sections', ['book_id', 'subtopic_id'])

    # 11. research_sources
    op.create_table(
        'research_sources',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('topic_id', sa.String(length=36), sa.ForeignKey('book_topics.id'), nullable=True),
        sa.Column('title', sa.String(length=512), nullable=False),
        sa.Column('url', sa.String(length=1024), nullable=True),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('publisher', sa.String(length=255), nullable=True),
        sa.Column('publication_date', sa.String(length=100), nullable=True),
        sa.Column('accessed_date', sa.String(length=100), nullable=True),
        sa.Column('source_type', sa.String(length=100), nullable=True),
        sa.Column('key_points', sa.JSON(), nullable=True),
        sa.Column('relevance', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_research_sources_book_id', 'research_sources', ['book_id'])
    op.create_index('ix_research_sources_topic_id', 'research_sources', ['topic_id'])

    # 12. review_results
    op.create_table(
        'review_results',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('section_id', sa.String(length=36), sa.ForeignKey('generated_sections.id'), nullable=True),
        sa.Column('agent', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('fact_check_status', sa.String(length=50), nullable=True),
        sa.Column('originality_score', sa.Float(), nullable=True),
        sa.Column('issues', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_review_results_book_id', 'review_results', ['book_id'])
    op.create_index('ix_review_results_section_id', 'review_results', ['section_id'])
    op.create_index('ix_review_results_status', 'review_results', ['status'])

    # 13. document_exports
    op.create_table(
        'document_exports',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('book_id', sa.String(length=36), sa.ForeignKey('books.id'), nullable=False),
        sa.Column('job_id', sa.String(length=36), sa.ForeignKey('generation_jobs.id'), nullable=True),
        sa.Column('format', sa.String(length=50), nullable=True),
        sa.Column('file_path', sa.String(length=1024), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('validation_report', sa.JSON(), nullable=True),
        sa.Column('syllabus_coverage', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_document_exports_book_id', 'document_exports', ['book_id'])
    op.create_index('ix_document_exports_job_id', 'document_exports', ['job_id'])


def downgrade() -> None:
    op.drop_table('document_exports')
    op.drop_table('review_results')
    op.drop_table('research_sources')
    op.drop_table('generated_sections')
    op.drop_table('generated_assets')
    op.drop_table('generation_events')
    op.drop_table('generation_jobs')
    op.drop_table('book_subtopics')
    op.drop_table('book_topics')
    op.drop_table('book_units')
    op.drop_table('books')
    op.drop_table('projects')
    op.drop_table('users')
