from django.test import TestCase
import datetime
from django.utils import timezone
from .models import UserProfile
# Create your tests here.
class DeleteBanned(TestCase):
    def test_delete_banned(self):
        banned_users = UserProfile.objects.filter(banned=True, banned_date__lte=timezone.now() - datetime.timedelta(days=10))
        banned_users.delete()