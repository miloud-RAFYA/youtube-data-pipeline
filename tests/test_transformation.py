import pandas as pd

from src.transformation.transform_channels import transform_channels
from src.transformation.transform_videos import (
    transform_videos,
    duration_to_seconds,
)


def test_duration_to_seconds():
    assert duration_to_seconds("PT1M17S") == 77
    assert duration_to_seconds("PT4M50S") == 290
    assert duration_to_seconds("PT58S") == 58
    assert duration_to_seconds("PT1H2M3S") == 3723
    assert duration_to_seconds(None) == 0


def test_transform_channels():
    df = transform_channels()

    # Vérifier que le DataFrame existe
    assert isinstance(df, pd.DataFrame)

    # Une chaîne doit être présente
    assert len(df) > 0

    # Vérifier les colonnes
    expected_columns = [
        "channel_id",
        "title",
        "description",
        "custom_url",
        "country",
        "view_count",
        "subscriber_count",
        "video_count",
    ]

    assert list(df.columns) == expected_columns

    # channel_id obligatoire
    assert df["channel_id"].notna().all()
    assert (df["channel_id"] != "").all()

    # Pas de doublons
    assert df["channel_id"].duplicated().sum() == 0

    # Vérifier les types numériques
    assert pd.api.types.is_integer_dtype(
        df["view_count"]
    )

    assert pd.api.types.is_integer_dtype(
        df["subscriber_count"]
    )

    assert pd.api.types.is_integer_dtype(
        df["video_count"]
    )

    # Les statistiques ne doivent pas être négatives
    assert (df["view_count"] >= 0).all()
    assert (df["subscriber_count"] >= 0).all()
    assert (df["video_count"] >= 0).all()

    # Aucune valeur NULL après nettoyage
    assert df.isna().sum().sum() == 0


def test_transform_videos():
    df = transform_videos()

    # Vérifier que le DataFrame existe
    assert isinstance(df, pd.DataFrame)

    # Des vidéos doivent être présentes
    assert len(df) > 0

    # Vérifier les colonnes
    expected_columns = [
        "video_id",
        "title",
        "published_at",
        "duration",
        "view_count",
        "like_count",
        "comment_count",
    ]

    assert list(df.columns) == expected_columns

    # video_id obligatoire
    assert df["video_id"].notna().all()
    assert (df["video_id"] != "").all()

    # Pas de doublons
    assert df["video_id"].duplicated().sum() == 0

    # Vérifier le type de la date
    assert isinstance(
      df["published_at"].dtype,
      pd.DatetimeTZDtype
     )

    # Vérifier que duration est un entier
    assert pd.api.types.is_integer_dtype(
        df["duration"]
    )

    # Vérifier les statistiques
    numeric_columns = [
        "view_count",
        "like_count",
        "comment_count",
        "duration",
    ]

    for column in numeric_columns:
        assert pd.api.types.is_integer_dtype(
            df[column]
        )

        assert (df[column] >= 0).all()

    # Aucune valeur NULL après nettoyage
    assert df.isna().sum().sum() == 0