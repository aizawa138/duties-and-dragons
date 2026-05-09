from django.utils import timezone
from .models import DailyResetState, Habits
from .services.fight_service import rotate_expired_fights


class DailyResetMiddleware:
    """Reset completed habits to active once per day."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        today = timezone.localdate()
        state, _ = DailyResetState.objects.get_or_create(
            key="habits_reset",
            defaults={"last_reset_date": today},
        )

        if state.last_reset_date < today:
            Habits.objects.filter(status="Completed").update(status="Active")
            state.last_reset_date = today
            state.save()

        rotate_expired_fights()

        return self.get_response(request)
