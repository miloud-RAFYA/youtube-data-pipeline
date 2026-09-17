import pandas as pd

from src.database.postgres import get_connection
from src.database.core_storage import save_videos_to_core


def test_pipeline_core_data():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Vérifier les chaînes
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM core.channels;
                """
            )

            channels_count = cursor.fetchone()[0]

            assert channels_count > 0

            # Vérifier les vidéos
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM core.videos;
                """
            )

            videos_count = cursor.fetchone()[0]

            assert videos_count > 0

            # Vérifier les vidéos orphelines
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM core.videos v
                LEFT JOIN core.channels c
                    ON v.channel_id = c.channel_id
                WHERE c.channel_id IS NULL;
                """
            )

            orphan_videos = cursor.fetchone()[0]

            assert orphan_videos == 0

    finally:
        connection.close()


def test_core_delete_removed_video():
    video_id = "TEST_DELETE_CORE"

    # Récupérer un channel_id existant
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

            assert result is not None

            channel_id = result[0]

    finally:
        connection.close()

    # 1. Insérer une vidéo de test
    df_with_video = pd.DataFrame([
        {
            "video_id": video_id,
            "title": "Vidéo de test DELETE",
            "published_at": "2026-09-17T10:00:00Z",
            "duration": 60,
            "view_count": 100,
            "like_count": 10,
            "comment_count": 5,
        }
    ])

    save_videos_to_core(df_with_video, channel_id)

    # Vérifier que la vidéo existe
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT video_id
                FROM core.videos
                WHERE video_id = %s;
                """,
                (video_id,)
            )

            assert cursor.fetchone() is not None

    finally:
        connection.close()

    # 2. DataFrame sans TEST_DELETE_CORE
    df_without_video = pd.DataFrame([
        {
            "video_id": "OTHER_TEST_VIDEO",
            "title": "Autre vidéo",
            "published_at": "2026-09-17T10:00:00Z",
            "duration": 120,
            "view_count": 200,
            "like_count": 20,
            "comment_count": 10,
        }
    ])

    # 3. INSERT/UPDATE + DELETE
    save_videos_to_core(df_without_video, channel_id)

    # 4. Vérifier que TEST_DELETE_CORE a été supprimée
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT video_id
                FROM core.videos
                WHERE video_id = %s;
                """,
                (video_id,)
            )

            assert cursor.fetchone() is None

    finally:
        connection.close()
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM core.videos
                WHERE video_id IN (%s, %s);
                """,
                (video_id, "OTHER_TEST_VIDEO")
            )

        connection.commit()

    finally:
        connection.close()