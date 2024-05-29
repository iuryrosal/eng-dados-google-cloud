from google.cloud import secretmanager
import google_crc32c
import os
import google.auth.jwt
import google.auth.crypt
import time
import requests
import json
from dotenv import load_dotenv


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


def generate_jwt(sa_keyfile_string, sa_email, expire, project_id):
    current_time_int = int(time.time())

    payload = {
        "iat": current_time_int,
        "exp": current_time_int + expire,
        "iss": f"https://securetoken.google.com/{project_id}",
        "aud": project_id,
        "sub": sa_email,
        "email": sa_email
    }

    signer = google.auth.crypt.RSASigner.from_string(sa_keyfile_string)

    jwt = google.auth.jwt.encode(signer, payload)

    return jwt


def create_jwt_token():
    sa_email = "api-apoenastack@fourth-eon-422319-v6.iam.gserviceaccount.com"
    expire = 300
    project_id = os.getenv("project_id", None)
    sm = SecretManager()
    sa_kf = json.loads(sm.access_secret(secret_id="sa_api",
                                        version_id=1))["private_key"]

    jwt = generate_jwt(sa_keyfile_string=sa_kf,
                       sa_email=sa_email,
                       expire=expire,
                       project_id=project_id)

    return jwt.decode("utf-8")


if __name__ == "__main__":
    load_dotenv()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "test_api_apoena/credentials.json"

    jwt = create_jwt_token()

    url = "https://api-apoena-stack-001gf3zmcopcz.uc.gateway.dev"

    auth_header = {"Authorization": f"Bearer {jwt}"}

    response = requests.get(f"{url}/",
                            verify=True,
                            headers=auth_header)

    print(response.status_code)
    print(response.content.decode("utf-8"))
