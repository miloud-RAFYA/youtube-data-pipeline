from src.database.postgres import get_connection


def save_channels_to_core(df):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            for _, channel in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO core.channels (
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
                        channel["channel_id"],
                        channel["title"],
                        channel["description"],
                        channel["custom_url"],
                        channel["country"],
                        int(channel["view_count"]),
                        int(channel["subscriber_count"]),
                        int(channel["video_count"]),
                    )
                )

        connection.commit()

        print(
            f"{len(df)} chaîne(s) chargée(s) dans core.channels."
        )

    finally:
        connection.close()


def get_channel_id():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT channel_id
                FROM core.channels
                LIMIT 1;
                """
            )

            result = cursor.fetchone()

            if result is None:
                raise ValueError(
                    "Aucune chaîne trouvée dans core.channels."
                )

            return result[0]

    finally:
        connection.close()


def save_videos_to_core(df, channel_id):
    if df.empty:
        print("Aucune vidéo reçue. INSERT/UPDATE/DELETE annulés.")
        return

    incoming_ids = set(df["video_id"].tolist())

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # INSERT / UPDATE
            for _, video in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO core.videos (
                        video_id,
                        channel_id,
                        title,
                        published_at,
                        duration,
                        view_count,
                        like_count,
                        comment_count
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (video_id)
                    DO UPDATE SET
                        channel_id = EXCLUDED.channel_id,
                        title = EXCLUDED.title,
                        published_at = EXCLUDED.published_at,
                        duration = EXCLUDED.duration,
                        view_count = EXCLUDED.view_count,
                        like_count = EXCLUDED.like_count,
                        comment_count = EXCLUDED.comment_count;
                    """,
                    (
                        video["video_id"],
                        channel_id,
                        video["title"],
                        video["published_at"],
                        int(video["duration"]),
                        int(video["view_count"]),
                        int(video["like_count"]),
                        int(video["comment_count"]),
                    )
                )

            # DELETE
            cursor.execute("""
                SELECT video_id
                FROM core.videos;
            """)

            existing_ids = {
                row[0]
                for row in cursor.fetchall()
            }

            ids_to_delete = existing_ids - incoming_ids

            for video_id in ids_to_delete:
                cursor.execute(
                    """
                    DELETE FROM core.videos
                    WHERE video_id = %s;
                    """,
                    (video_id,)
                )

        connection.commit()

        print(
            f"{len(df)} vidéos chargées dans core.videos."
        )

        print(
            f"{len(ids_to_delete)} vidéo(s) supprimée(s) de core.videos."
        )

    finally:
        connection.close()
    