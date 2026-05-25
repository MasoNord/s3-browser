import sqlalchemy as sa

from browser.domain.entity.s3_connection_settings import S3ConnectionSetting
from browser.infrastructure.persistence.registry import mapper_registry

metadata = mapper_registry.metadata

s3_connection_settings_table = sa.Table(
    "s3_connection_settings",
    metadata,
    sa.Column("id", sa.String(36), primary_key=True),
    sa.Column("region_name", sa.String(255), nullable=False),
    sa.Column("endpoint_url", sa.String(255), nullable=False),
    sa.Column("aws_access_key_id", sa.String(255), nullable=False),
    sa.Column("aws_secret_access_key", sa.String(255), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
)

mapper_registry.map_imperatively(
    S3ConnectionSetting,
    s3_connection_settings_table
)