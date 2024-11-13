from django.core.management.base import BaseCommand
from legal_fix.models import Subscriber


class Command(BaseCommand):
    help = "Retrieves subscribers from the database"

    def handle(self, *args, **options):
        try:
            # Retrieve all subscribers
            subscribers = Subscriber.objects.all()

            # Print each subscriber's information
            for subscriber in subscribers:
                self.stdout.write(self.style.SUCCESS(f"Subscriber ID: {subscriber.id}"))
                self.stdout.write(f"Name: {subscriber.first_name} {subscriber.middle_name} {subscriber.last_name}")
                self.stdout.write(f"Email: {subscriber.email}")
                self.stdout.write(f"Phone: {subscriber.phone}")
                self.stdout.write(f"Gender: {subscriber.gender}")
                self.stdout.write(f"Subscription Active: {subscriber.subscription_active}")
                self.stdout.write(f"Roles: {subscriber.roles}")
                self.stdout.write(f"Date of Birth: {subscriber.date_of_birth}")
                self.stdout.write(f"ACL: {subscriber.acl}")
                self.stdout.write(f"Last Updated: {subscriber.last_updated_timestamp}")
                self.stdout.write('-' * 50)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error retrieving subscribers: {e}"))
