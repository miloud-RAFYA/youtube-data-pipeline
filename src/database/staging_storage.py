from src.database.postgres import get_connection
from src.database.raw_storage import load_json


def load_raw_data_to_staging():
    channel_data = load_json("channel.json")
    videos_data = load_json("videos.json")

    if not channel_data.get("items"):
        raise ValueError("Aucune donnée de chaîne trouvée dans channel.json")

    channel = channel_data["items"][0]

    save_channel(channel)
    save_videos(videos_data)

    print("Données JSON chargées dans PostgreSQL Staging.")

def save_channel(channel):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO staging.youtube_channels (
                    channel_id,
                    title,
                    description,
                    custom_url,
                    country,
                    view_count,
                    subscriber_count,
                    video_count
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (channel_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    custom_url = EXCLUDED.custom_url,
                    country = EXCLUDED.country,
                    view_count = EXCLUDED.view_count,
                    subscriber_count = EXCLUDED.subscriber_count,
                    video_count = EXCLUDED.video_count;
                """,
                (
                    channel["id"],
                    channel["snippet"]["title"],
                    channel["snippet"].get("description"),
                    channel["snippet"].get("customUrl"),
                    channel["snippet"].get("country"),
                    int(channel["statistics"].get("viewCount", 0)),
                    int(channel["statistics"].get("subscriberCount", 0)),
                    int(channel["statistics"].get("videoCount", 0)),
                )
            )

        connection.commit()

    finally:
        connection.close()


def save_videos(videos):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # IDs présents dans la nouvelle extraction
            incoming_ids = {
                video["videoId"]
                for video in videos
            }

            # 1. INSERT + UPDATE
            for video in videos:
                cursor.execute(
                    """
                    INSERT INTO staging.youtube_videos (
                        video_id,
                        title,
                        published_at,
                        duration,
                        view_count,
                        like_count,
                        comment_count
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)

                    ON CONFLICT (video_id)
                    DO UPDATE SET
                        title = EXCLUDED.title,
                        published_at = EXCLUDED.published_at,
                        duration = EXCLUDED.duration,
                        view_count = EXCLUDED.view_count,
                        like_count = EXCLUDED.like_count,
                        comment_count = EXCLUDED.comment_count;
                    """,
                    (
                        video["videoId"],
                        video["title"],
                        video["publishedAt"],
                        video["duration"],
                        int(video.get("viewCount", 0)),
                        int(video.get("likeCount", 0)),
                        int(video.get("commentCount", 0)),
                    )
                )

            # 2. DELETE
            if incoming_ids:
                cursor.execute(
                    """
                    SELECT video_id
                    FROM staging.youtube_videos;
                    """
                )

                existing_ids = {
                    row[0]
                    for row in cursor.fetchall()
                }

                ids_to_delete = existing_ids - incoming_ids

                for video_id in ids_to_delete:
                    cursor.execute(
                        """
                        DELETE FROM staging.youtube_videos
                        WHERE video_id = %s;
                        """,
                        (video_id,)
                    )

                print(
                    f"{len(ids_to_delete)} vidéo(s) supprimée(s) du Staging."
                )

        connection.commit()

    finally:
        connection.close()
    