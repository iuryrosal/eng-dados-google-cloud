from google.cloud import secretmanager
import google_crc32c
import os


class SecretManager:
    def __init__(self) -> None:
        self.project_id = os.getenv("project_id", None)
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret(self, secret_id, version_id):
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response

        payload = response.payload.data.decode("UTF-8")
        return payload
