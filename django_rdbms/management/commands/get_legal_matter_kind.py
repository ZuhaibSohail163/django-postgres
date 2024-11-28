from django.core.management.base import BaseCommand
from django_rdbms.models import Subscriber, LegalMatterKind


class Command(BaseCommand):
    help = "Retrieves Legal Matter Kind from the database"

    def handle(self, *args, **options):
        try:
            # Retrieve all subscribers
            lm_kinds = LegalMatterKind.objects.all()

            # Print each lm kind's information
            for lm_kind in lm_kinds:
                self.stdout.write(self.style.SUCCESS(f"Legal Matter Kind ID: {lm_kind.id}"))
                self.stdout.write(f"category: {lm_kind.category}")
                self.stdout.write(f"description: {lm_kind.description}")
                self.stdout.write(f"intake_form: {lm_kind.intake_form}")
                self.stdout.write(f"name: {lm_kind.name}")
                self.stdout.write(f"products: {lm_kind.products}")
                self.stdout.write('-' * 50)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error retrieving Lm_kinds: {e}"))
