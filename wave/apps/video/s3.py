import requests
from django.conf import settings


class BunnyVideoAPI:
    def __init__(self):
        access_key = settings.BUNNY_ACCESS_KEY
        storage_name = settings.STORAGE_ZONE_NAME
        self.base_url = f"https://sg.storage.bunnycdn.com/{storage_name}"
        self.headers = {
            "AccessKey": access_key,
            "Accept": "application/json",
            "Content-Type": "application/octet-stream",
        }

    def _request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        # This will raise an HTTPError if the HTTP request returned
        # an unsuccessful status code.
        response.raise_for_status()
        return response.json()

    def list_videos(self, collection):
        endpoint = f"/{collection}/"
        return self._request("GET", endpoint)

    def dowload_video(self, video_id):
        endpoint = f"/videos/{video_id}"
        return self._request("GET", endpoint)

    def upload_video(self, video_path, collection, file_name) -> dict:
        with open(video_path, "rb") as video_file:
            endpoint = f"/{collection}/{file_name}"
            response = requests.put(f"{self.base_url}{endpoint}", headers=self.headers, data=video_file)
            response.raise_for_status()
            return response.json()

    def delete_video(self, collection, file_name):
        endpoint = f"/{collection}/{file_name}"
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_video(self, video_id, data):
        endpoint = f"/videos/{video_id}"
        return self._request("PUT", endpoint, data)


# # Usage
# api_key = "YOUR_BUNNY_API_KEY"
# bunny_api = BunnyVideoAPI(api_key)
# all_videos = bunny_api.get_all_videos()
# print(all_videos)
