from google.cloud import pubsub_v1
from google.api_core import retry
from dotenv import load_dotenv
import os


load_dotenv()

project_id = os.getenv("project_id", None)
subscription_id = os.getenv("subscription_id", None)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fourth-eon-422319-v6-bc6807d8fc17.json'

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

NUM_MESSAGES = 3

with subscriber:
    while True:
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
            retry=retry.Retry(deadline=300),
        )

        if not len(response.received_messages) == 0:
            ack_ids = []
            for received_message in response.received_messages:
                print(f"Received: {received_message.message.data}.")
                ack_ids.append(received_message.ack_id)

            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )

            print(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )
