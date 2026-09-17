import pandas as pd

from src.database.postgres import get_connection


def load_channels_from_staging():
    connection = get_connection()

    try:
        query = """
            SELECT
                channel_id,
                title,
                description,
                custom_url,
                country,
                view_count,
                subscriber_count,
                video_count
            FROM staging.youtube_channels;
        """

        df = pd.read_sql_query(
            query,
            connection
        )

        print(
            f"{len(df)} chaîne(s) récupérée(s) depuis le Staging."
        )

        return df

    finally:
        connection.close()


def load_videos_from_staging():
    connection = get_connection()

    try:
        query = """
            SELECT
                video_id,
                title,
                published_at,
                duration,
                view_count,
                like_count,
                comment_count
            FROM staging.youtube_videos;
        """

        df = pd.read_sql_query(
            query,
            connection
        )

        print(
            f"{len(df)} vidéo(s) récupérée(s) depuis le Staging."
        )

        return df

    finally:
        connection.close()