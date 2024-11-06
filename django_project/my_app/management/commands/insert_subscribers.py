from django.core.management.base import BaseCommand
from datetime import datetime
from django_project.my_app.services.database_operations import insert_subscriber


class Command(BaseCommand):
    help = 'Insert a subscriber into the database'

    def handle(self, *args, **options):
        data = {
            "last_name": "Doe",
            "first_name": "John",
            "email": "johndoe@example.com",
            "phone": "5555555555",
            "gender": "Male",
            "last_updated_timestamp": datetime.now(),
            "date_of_birth": datetime.now(),
            "subscription_active": True,
            "roles": ["user"],
            "acl": {"read": True, "write": False}
        }

        new_subscriber = insert_subscriber(data)
        self.stdout.write(self.style.SUCCESS(f"Inserted subscriber: {new_subscriber}"))
