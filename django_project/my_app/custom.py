from django.db.models import DateTimeField

class DateTimeWithoutTZField(DateTimeField):
  def db_type(self, *args, **kwargs):
    return 'timestamp'
