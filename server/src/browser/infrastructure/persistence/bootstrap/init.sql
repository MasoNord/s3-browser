
CREATE TABLE s3_connection_settings (
    id TEXT(36) PRIMARY KEY,

    region_name TEXT(255) NOT NULL,
    endpoint_url TEXT(255) NOT NULL,

    aws_access_key_id TEXT(255) NOT NULL,
    aws_secret_access_key TEXT(255) NOT NULL,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);