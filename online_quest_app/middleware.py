import datetime
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache

class DeleteBannedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .models import UserProfile
        last_run = cache.get('delete_banned_profiles_last_run')
        now = timezone.now()

        if not last_run or (now - last_run).days >= 1:
            expired_profiles = UserProfile.objects.filter(
                banned=True,
                banned_date__lte=now - datetime.timedelta(days=10)
            )
            for expired_profile in expired_profiles:
                expired_profile.user.delete()
            cache.set('delete_banned_profiles_last_run', now)

        response = self.get_response(request)
        return response