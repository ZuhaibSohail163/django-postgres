from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = "Drops the current database. Use with caution!"

    def handle(self, *args, **options):
        db_name = connection.settings_dict['NAME']

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public';
                """)
                tables = cursor.fetchall()
                if not tables:
                  self.stdout.write(self.style.WARNING('No tables found to drop.'))
                  return
                
                for table in tables:
                  table_name = table[0]
                  try:
                      cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
                      self.stdout.write(self.style.SUCCESS(f'Table "{table_name}" dropped successfully.'))
                  except Exception as e:
                      self.stderr.write(self.style.ERROR(f'Error dropping table "{table_name}": {e}'))
            self.stdout.write(self.style.SUCCESS(f'Database "{db_name}" dropped successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error dropping database: {e}"))
