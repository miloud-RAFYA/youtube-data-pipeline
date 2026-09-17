CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.youtube_channels (
    channel_id VARCHAR(255) PRIMARY KEY,
    title TEXT,
    description TEXT,
    custom_url TEXT,
    country VARCHAR(10),
    view_count BIGINT,
    subscriber_count BIGINT,
    video_count BIGINT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.youtube_videos (
    video_id VARCHAR(255) PRIMARY KEY,
    title TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    duration TEXT,
    view_count BIGINT,
    like_count BIGINT,
    comment_count BIGINT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);