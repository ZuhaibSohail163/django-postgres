from django.core.management.base import BaseCommand
from legal_fix.models import Subscriber, FirmUser


class Command(BaseCommand):
    help = "Retrieves subscribers from the database"

    def handle(self, *args, **options):
        try:
            # Retrieve all firm_users
            firm_users= FirmUser.objects.all()

            for firm_user in firm_users:
                self.stdout.write(self.style.SUCCESS(f"firm_user ID: {firm_user.id}"))
                self.stdout.write(f"Name: {firm_user.first_name} {firm_user.last_name}")
                self.stdout.write(f"Email: {firm_user.email}")
                self.stdout.write(f"last_updated_timestamp: {firm_user.last_updated_timestamp}")
                self.stdout.write(f"number_of_assigning_legal_matters: {firm_user.number_of_assigning_legal_matters}")
                self.stdout.write(f"number_of_assigned_legal_matters: {firm_user.number_of_assigned_legal_matters}")
                self.stdout.write(f"Roles: {firm_user.roles}")
                self.stdout.write(f"phone: {firm_user.phone}")
                self.stdout.write(f"firm_ref: {firm_user.firm_ref}")
                self.stdout.write('-' * 50)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error retrieving firm_users: {e}"))
