CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.channels (
    channel_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    custom_url TEXT,
    country VARCHAR(10),
    view_count BIGINT DEFAULT 0,
    subscriber_count BIGINT DEFAULT 0,
    video_count BIGINT DEFAULT 0,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS core.videos (
    video_id VARCHAR(255) PRIMARY KEY,
    channel_id VARCHAR(255),
    title TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE,
    duration TEXT,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    comment_count BIGINT DEFAULT 0,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_videos_channel
        FOREIGN KEY (channel_id)
        REFERENCES core.channels(channel_id)
);