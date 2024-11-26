from django.core.management.base import BaseCommand
from django_rdbms.models import Subscriber, LegalMatter


class Command(BaseCommand):
    help = "Retrieves subscribers from the database"

    def handle(self, *args, **options):
        try:
            # Retrieve all subscribers
            legal_matters = LegalMatter.objects.all()
            # Print each subscriber's information
            for legal_matter in legal_matters:
                self.stdout.write(self.style.SUCCESS(f"LegalMatter ID: {legal_matter.id}"))
                self.stdout.write(f"status: {legal_matter.status}")
                self.stdout.write(f"kind_ref: {legal_matter.kind_ref}")
                self.stdout.write(f"created_timestamp: {legal_matter.created_timestamp}")
                self.stdout.write(f"subscriber_ref: {legal_matter.subscriber_ref}")
                self.stdout.write(f"acl: {legal_matter.acl}")
                self.stdout.write('-' * 50)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error retrieving subscribers: {e}"))
