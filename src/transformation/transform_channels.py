import pandas as pd

from src.database.staging_reader import load_channels_from_staging


def transform_channels():
    df = load_channels_from_staging()

    print(
        f"Nombre de chaînes initiales : {len(df)}"
    )

    # --------------------------------------------------
    # 1. Vérifier les colonnes
    # --------------------------------------------------

    required_columns = [
        "channel_id",
        "title",
        "description",
        "custom_url",
        "country",
        "view_count",
        "subscriber_count",
        "video_count",
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
    # 2. Nettoyer channel_id
    # --------------------------------------------------

    df["channel_id"] = (
        df["channel_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # 3. Nettoyer title
    # --------------------------------------------------

    df["title"] = (
        df["title"]
        .fillna("Titre inconnu")
        .astype(str)
        .str.strip()
    )

    df.loc[
        df["title"] == "",
        "title"
    ] = "Titre inconnu"

    # --------------------------------------------------
    # 4. Nettoyer description
    # --------------------------------------------------

    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # 5. Nettoyer custom_url
    # --------------------------------------------------

    df["custom_url"] = (
        df["custom_url"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # 6. Nettoyer country
    # --------------------------------------------------

    df["country"] = (
        df["country"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # --------------------------------------------------
    # 7. Convertir les statistiques
    # --------------------------------------------------

    numeric_columns = [
        "view_count",
        "subscriber_count",
        "video_count",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        df[column] = df[column].fillna(0)

        df[column] = df[column].clip(
            lower=0
        )

        df[column] = df[column].astype("int64")

    # --------------------------------------------------
    # 8. Supprimer channel_id vide
    # --------------------------------------------------

    df = df[
        (df["channel_id"] != "")
    ]

    # --------------------------------------------------
    # 9. Supprimer doublons
    # --------------------------------------------------

    duplicates = df["channel_id"].duplicated().sum()

    print(
        f"Doublons détectés : {duplicates}"
    )

    df = df.drop_duplicates(
        subset="channel_id"
    )

    # --------------------------------------------------
    # 10. Contrôle final
    # --------------------------------------------------

    print(
        f"Nombre de lignes après nettoyage : "
        f"{len(df)}"
    )

    print(
        f"Valeurs nulles restantes : "
        f"{df.isna().sum().sum()}"
    )

    print("\nTypes après nettoyage :")
    print(df.dtypes)

    print("\nDonnées propres :")
    print(df)

    return df


if __name__ == "__main__":
    transform_channels()