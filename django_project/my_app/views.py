from datetime import datetime

from .services.database_operations import insert_subscriber

data = {
    "last_name": "Doe",
    "first_name": "John",
    "email": "johndoe@example.com",
    "last_updated_timestamp": datetime.now(),
    "subscription_active": True,
    "roles": ["user"],
    "acl": {"read": True, "write": False}
}

new_subscriber = insert_subscriber(data)
print("Inserted subscriber:", new_subscriber)
