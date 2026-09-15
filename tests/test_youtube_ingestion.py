from src.ingestion.youtube_api import (
    get_channel_data,
    get_videos_from_playlist,
    get_video_details,
    format_video,
)


def test_ingestion_end_to_end():

    print("\n==============================")
    print("TEST D'INGESTION END-TO-END")
    print("==============================\n")

    # 1. Récupération des informations de la chaîne
    channel_data = get_channel_data()

    assert channel_data is not None, (
        "Échec : impossible de récupérer la chaîne."
    )

    assert channel_data.get("items"), (
        "Échec : aucune chaîne trouvée."
    )

    channel = channel_data["items"][0]

    print("✓ Chaîne récupérée :", channel["snippet"]["title"])

    # 2. Récupération de la playlist Uploads
    playlist_id = (
        channel["contentDetails"]
        ["relatedPlaylists"]
        ["uploads"]
    )

    assert playlist_id, (
        "Échec : playlist Uploads introuvable."
    )

    print("✓ Playlist Uploads récupérée :", playlist_id)

    # 3. Récupération des vidéos
    playlist_videos = get_videos_from_playlist(
        playlist_id
    )

    assert playlist_videos is not None, (
        "Échec : impossible de récupérer les vidéos."
    )

    assert len(playlist_videos) > 0, (
        "Échec : aucune vidéo récupérée."
    )

    print(
        "✓ Vidéos récupérées :",
        len(playlist_videos)
    )

    # 4. Récupération des IDs des vidéos
    video_ids = [
        video["contentDetails"]["videoId"]
        for video in playlist_videos
    ]

    assert len(video_ids) == len(playlist_videos), (
        "Échec : certains Video IDs sont manquants."
    )

    print(
        "✓ Video IDs récupérés :",
        len(video_ids)
    )

    # 5. Récupération des détails
    videos_details = get_video_details(
        video_ids
    )

    assert videos_details is not None, (
        "Échec : impossible de récupérer les détails."
    )

    assert len(videos_details) > 0, (
        "Échec : aucun détail vidéo récupéré."
    )

    print(
        "✓ Détails des vidéos récupérés :",
        len(videos_details)
    )

    # 6. Transformation des données
    formatted_videos = [
        format_video(video)
        for video in videos_details
    ]

    assert len(formatted_videos) > 0, (
        "Échec : aucune vidéo formatée."
    )

    # 7. Vérification de la structure
    required_fields = [
        "videoId",
        "title",
        "publishedAt",
        "duration",
        "viewCount",
        "likeCount",
        "commentCount",
    ]

    for video in formatted_videos:
        for field in required_fields:
            assert field in video, (
                f"Champ manquant : {field}"
            )

    print(
        "✓ Données transformées :",
        len(formatted_videos)
    )

    print("\n==============================")
    print("TEST END-TO-END RÉUSSI ✓")
    print("==============================")