from src.database.postgres import get_connection
from src.database.core_storage import get_channel_id


def test_core_channels_count():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM core.channels;
                """
            )

            count = cursor.fetchone()[0]

            assert count == 1

    finally:
        connection.close()


def test_core_videos_count():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM core.videos;
                """
            )

            count = cursor.fetchone()[0]

            assert count > 0

    finally:
        connection.close()


def test_channel_exists():
    channel_id = get_channel_id()

    assert channel_id is not None
    assert channel_id != ""


def test_videos_have_valid_channel():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
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