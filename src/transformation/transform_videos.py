import pandas as pd
from src.database.staging_reader import load_videos_from_staging
import re


def duration_to_seconds(duration):
    if pd.isna(duration):
        return 0

    duration = str(duration)

    match = re.fullmatch(
        r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",
        duration
    )

    if not match:
        return 0

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    return hours * 3600 + minutes * 60 + seconds
 
def transform_videos():
    df = load_videos_from_staging()

    print(
        f"Nombre de lignes initiales : {len(df)}"
    )

    # --------------------------------------------------
    # 1. Vérification des colonnes
    # --------------------------------------------------

    required_columns = [
        "video_id",
        "title",
        "published_at",
        "duration",
        "view_count",
        "like_count",
        "comment_count",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes : {missing_columns}"
        )

    # --------------------------------------------------
    # 2. Supprimer les doublons
    # --------------------------------------------------

    duplicates = df["video_id"].duplicated().sum()

    print(f"Doublons détectés : {duplicates}")

    df = df.drop_duplicates(
        subset="video_id"
    )
    df = load_videos_from_staging()

    print(
        f"Nombre de lignes initiales : {len(df)}"
    )
    # --------------------------------------------------
    # 1. Vérification des colonnes
    # --------------------------------------------------

    required_columns = [
    "video_id",
    "title",
    "published_at",
    "duration",
    "view_count",
    "like_count",
    "comment_count",
     ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes : {missing_columns}"
        )


    # --------------------------------------------------
    # 3. Supprimer les doublons
    # --------------------------------------------------

    duplicates = df["video_id"].duplicated().sum()

    print(f"Doublons détectés : {duplicates}")

    df = df.drop_duplicates(
        subset="video_id"
    )

    # --------------------------------------------------
    # 4. Nettoyer les titres
    # --------------------------------------------------

    df["title"] = (
        df["title"]
        .fillna("Titre inconnu")
        .astype(str)
        .str.strip()
    )

    # Remplacer les titres vides
    df.loc[
        df["title"] == "",
        "title"
    ] = "Titre inconnu"

    # --------------------------------------------------
    # 5. Nettoyer les dates
    # --------------------------------------------------

    df["published_at"] = pd.to_datetime(
        df["published_at"],
        errors="coerce",
        utc=True
    )

    invalid_dates = df["published_at"].isna().sum()

    print(f"Dates invalides : {invalid_dates}")

    # Supprimer les vidéos sans date valide
    df = df.dropna(
        subset=["published_at"]
    )

    # --------------------------------------------------
    # 6. Convertir les statistiques
    # --------------------------------------------------

    numeric_columns = [
        "view_count",
        "like_count",
        "comment_count",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )
     
        df[column] = df[column].fillna(0)

        df[column] = df[column].astype("int64")
        
    df["duration"] = df["duration"].apply(
           duration_to_seconds
    )

    # --------------------------------------------------
    # 7. Vérifier les valeurs négatives
    # --------------------------------------------------

    for column in numeric_columns:
        negative_values = (
            df[column] < 0
        ).sum()

        print(
            f"Valeurs négatives dans {column} : "
            f"{negative_values}"
        )

        df.loc[
            df[column] < 0,
            column
        ] = 0

    # --------------------------------------------------
    # 8. Nettoyer les espaces dans video_id
    # --------------------------------------------------

    df["video_id"] = (
        df["video_id"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # 9. Supprimer les video_id vides
    # --------------------------------------------------

    df = df[
        df["video_id"].notna()
        & (df["video_id"] != "")
    ]

    # --------------------------------------------------
    # 10. Contrôle final
    # --------------------------------------------------

    print(
        f"Nombre de lignes après nettoyage : "
        f"{len(df)}"
    )

    print(
        f"Doublons restants : "
        f"{df['video_id'].duplicated().sum()}"
    )

    print(
        f"Valeurs nulles restantes : "
        f"{df.isna().sum().sum()}"
    )

    print("\nTypes après nettoyage :")
    print(df.dtypes)

    print("\nAperçu des données propres :")
    print(df)
    print("\nDurées converties en secondes :")
    print(df["duration"].head())

    return df
if __name__ == "__main__":
   
    transform_videos()