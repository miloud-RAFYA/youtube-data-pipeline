import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")

BASE_URL = "https://www.googleapis.com/youtube/v3"


def get_channel_data():
    url = f"{BASE_URL}/channels"

    params = {
        "part": "snippet,statistics,contentDetails",
        "forHandle": CHANNEL_HANDLE,
        "key": API_KEY,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        print("HTTP Status :", response.status_code)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print("Erreur : le délai d'attente de la requête a été dépassé.")

    except requests.exceptions.RequestException as e:
        print("Erreur lors de l'appel à l'API YouTube :", e)

    return None


def get_videos_from_playlist(playlist_id):
    url = f"{BASE_URL}/playlistItems"

    all_videos = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": API_KEY,
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            print("HTTP Status playlist :", response.status_code)

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.Timeout:
            print(
                "Erreur : délai d'attente dépassé "
                "lors de la récupération des vidéos."
            )
            return None

        except requests.exceptions.RequestException as e:
            print(
                "Erreur lors de la récupération des vidéos :",
                e
            )
            return None

        all_videos.extend(data.get("items", []))

        print(
            "Vidéos récupérées jusqu'à maintenant :",
            len(all_videos)
        )

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

    return all_videos


def get_video_details(video_ids):
    url = f"{BASE_URL}/videos"

    all_videos = []

    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i + 50]

        params = {
            "part": "snippet,contentDetails,statistics",
            "id": ",".join(batch_ids),
            "key": API_KEY,
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            print("HTTP Status videos :", response.status_code)

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.Timeout:
            print(
                "Erreur : délai d'attente dépassé "
                "lors de la récupération des détails des vidéos."
            )
            return None

        except requests.exceptions.RequestException as e:
            print(
                "Erreur lors de la récupération des détails des vidéos :",
                e
            )
            return None

        all_videos.extend(data.get("items", []))

        print(
            "Vidéos détaillées récupérées :",
            len(all_videos)
        )

    return all_videos


def format_video(video):
    return {
        "videoId": video["id"],
        "title": video["snippet"]["title"],
        "publishedAt": video["snippet"]["publishedAt"],
        "duration": video["contentDetails"]["duration"],
        "viewCount": video["statistics"].get("viewCount", "0"),
        "likeCount": video["statistics"].get("likeCount", "0"),
        "commentCount": video["statistics"].get("commentCount", "0"),
    }


if __name__ == "__main__":
    data = get_channel_data()

    if not data:
        print("Impossible de récupérer les informations de la chaîne.")

    else:
        print("Connexion à YouTube API réussie !")

        if data.get("items"):
            channel = data["items"][0]

            print("Channel ID :", channel["id"])
            print("Nom :", channel["snippet"]["title"])
            print("Handle :", channel["snippet"]["customUrl"])
            print("Pays :", channel["snippet"].get("country"))

            print("Vues :", channel["statistics"]["viewCount"])
            print("Abonnés :", channel["statistics"]["subscriberCount"])
            print("Vidéos :", channel["statistics"]["videoCount"])

            uploads_playlist_id = (
                channel["contentDetails"]["relatedPlaylists"]["uploads"]
            )

            print("Uploads Playlist ID :", uploads_playlist_id)

            # Récupération des vidéos
            playlist_videos = get_videos_from_playlist(
                uploads_playlist_id
            )

            if playlist_videos is None:
                print(
                    "Impossible de récupérer les vidéos "
                    "de la chaîne."
                )

            else:
                print(
                    "Nombre total de vidéos récupérées :",
                    len(playlist_videos)
                )

                # Récupération des Video IDs
                video_ids = [
                    video["contentDetails"]["videoId"]
                    for video in playlist_videos
                ]

                print("Video IDs :", video_ids)

                # Récupération des détails des vidéos
                if video_ids:
                    videos_details = get_video_details(video_ids)

                    if videos_details is None:
                        print(
                            "Impossible de récupérer les détails "
                            "des vidéos."
                        )

                    else:
                        # Transformation dans notre format
                        formatted_videos = []

                        for video in videos_details:
                            formatted_videos.append(
                                format_video(video)
                            )

                        print("\nVidéos formatées :")

                        for video in formatted_videos:
                            print(video)

        else:
            print("Aucune chaîne trouvée.")