import streamlit as st
from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable
import os
import json
from datetime import datetime
from dotenv import load_dotenv


def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future,
    data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


load_dotenv()

form_data = {}

st.write("Formulário de Inscrição")

form_data["nome"] = st.text_input("Nome Completo:", key="nome")

form_data["email"] = st.text_input("E-mail:", key="mail")

form_data["telefone"] = st.text_input("Telefone", key="phone")

form_data["option"] =  st.radio(
        "Como você prefere ser contatado?",
        key="contato",
        options=["Email", "WhatsApp", "SMS"],
    )

subscription = st.button("Se inscrever!")

project_id = os.getenv("project_id", None)
topic_id = os.getenv("topic_id", None)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fourth-eon-422319-v6-bc6807d8fc17.json'


if subscription:
    str_datetime = str(datetime.now().timestamp())
    name_email = form_data["email"].split("@")[0]
    form_data["person_id"] = "_".join([name_email, str_datetime])

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(form_data).encode("utf-8")

    publish_future = publisher.publish(topic_path, data)
    publish_future.add_done_callback(get_callback(publish_future, data))

    futures.wait([publish_future], return_when=futures.ALL_COMPLETED)

    print(form_data)
    print(f"Published messages with error handler to {topic_path}.")

