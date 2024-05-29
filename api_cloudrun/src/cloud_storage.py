from google.cloud import storage


class CloudStorage:
    def __init__(self) -> None:
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket_name)

    def pick_object(self, blob_name):
        return self.bucket.get_blob(blob_name).download_as_string()