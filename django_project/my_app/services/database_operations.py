from ..pydantic_models import SubscriberData
from ..models import Subscriber


def insert_subscriber(data: dict):
    # Validate data with Pydantic
    subscriber_data = SubscriberData(**data)

    # Insert data into the database using Django ORM
    subscriber = Subscriber.objects.create(
        last_name=subscriber_data.last_name,
        first_name=subscriber_data.first_name,
        middle_name=subscriber_data.middle_name,
        email=subscriber_data.email,
        phone=subscriber_data.phone,
        gender=subscriber_data.gender,
        last_updated_timestamp=subscriber_data.last_updated_timestamp,
        date_of_birth=subscriber_data.date_of_birth,
        subscription_active=subscriber_data.subscription_active,
        roles=subscriber_data.roles,
        acl=subscriber_data.acl
    )
    return subscriber
