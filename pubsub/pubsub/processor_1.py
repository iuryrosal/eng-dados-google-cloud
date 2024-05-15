from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os


load_dotenv()

project_id = os.getenv("project_id", None)
subscription_id = os.getenv("subscription_id", None)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fourth-eon-422319-v6-bc6807d8fc17.json'


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    while True:
        try:
            streaming_pull_future.result()
        except Exception as e:
            print(
                f"Listening for messages on {subscription_path} threw an exception: {e}."
            )
            streaming_pull_future.cancel()
            streaming_pull_future.result()
