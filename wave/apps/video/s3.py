import requests
from django.conf import settings


class BunnyVideoAPI:
    def __init__(self):
        api_key = settings.CDN_API_KEY
        library = settings.CDN_LIBRARY
        self.base_url = f"https://video.bunnycdn.com/library/{library}"
        self.headers = {
            "AccessKey": api_key,
            "Accept": "application/json",
            "Content-Type": "application/*+json",
        }

    def _request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        # This will raise an HTTPError if the HTTP request returned
        # an unsuccessful status code.
        response.raise_for_status()
        return response.json()

    def create_collection(self, name):
        endpoint = "/collections"
        return self._request("POST", endpoint, data={"name": name})

    def get_all_videos(self):
        endpoint = "/videos"
        return self._request("GET", endpoint)

    def get_video(self, video_id):
        endpoint = f"/videos/{video_id}"
        return self._request("GET", endpoint)

    def upload_video(self, title, video_path, collection) -> dict:
        with open(video_path, "rb") as video_file:
            endpoint = "/videos"
            files = {"file": video_file}
            data = {"collectionId": collection, "title": title}
            response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, data=data, files=files)
            response.raise_for_status()
            return response.json()

    def delete_video(self, video_id):
        endpoint = f"/videos/{video_id}"
        return self._request("DELETE", endpoint)

    def update_video(self, video_id, data):
        endpoint = f"/videos/{video_id}"
        return self._request("PUT", endpoint, data)


# # Usage
# api_key = "YOUR_BUNNY_API_KEY"
# bunny_api = BunnyVideoAPI(api_key)
# all_videos = bunny_api.get_all_videos()
# print(all_videos)
