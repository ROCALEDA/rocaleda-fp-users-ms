import os
from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials


def get_publisher():
    if os.environ.get("ENV", "PROD") == "DEV":
        creds = Credentials.from_service_account_info(
            {
                "type": os.environ["GOOGLE_CLOUD_TYPE"],
                "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
                "private_key_id": os.environ["GOOGLE_CLOUD_PRIVATE_KEY_ID"],
                "private_key": os.environ["GOOGLE_CLOUD_PRIVATE_KEY"],
                "client_email": os.environ["GOOGLE_CLOUD_CLIENT_EMAIL"],
                "client_id": os.environ["GOOGLE_CLOUD_CLIENT_ID"],
                "auth_uri": os.environ["GOOGLE_CLOUD_AUTH_URI"],
                "token_uri": os.environ["GOOGLE_CLOUD_TOKEN_URI"],
                "auth_provider_x509_cert_url": os.environ[
                    "GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL"
                ],
                "client_x509_cert_url": os.environ["GOOGLE_CLOUD_CLIENT_X509_CERT_URL"],
            }
        )

        return pubsub_v1.PublisherClient(credentials=creds)

    return pubsub_v1.PublisherClient()


def get_candidate_creation_topic_path(publisher: pubsub_v1.PublisherClient):
    CANDIDATE_CREATION_TOPIC = os.environ["CANDIDATE_CREATION_TOPIC"]
    return publisher.topic_path(
        os.environ["GOOGLE_CLOUD_PROJECT"], CANDIDATE_CREATION_TOPIC
    )

def get_customer_creation_topic_path(publisher: pubsub_v1.PublisherClient):
    CUSTOMER_CREATION_TOPIC = os.environ["CUSTOMER_CREATION_TOPIC"]
    return publisher.topic_path(
        os.environ["GOOGLE_CLOUD_PROJECT"], CUSTOMER_CREATION_TOPIC
    )