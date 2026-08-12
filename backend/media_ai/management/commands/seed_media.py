# ============================================================================
# App:  media_ai
# File: management/commands/seed_media.py
# Run:  python manage.py seed_media
# Role: Creates one sample GeneratedImage record (status="complete", no
#       actual file — just enough for the UI/admin to have a row to show).
#       Most media_ai data is naturally user-generated, so there's
#       intentionally little to seed here.
# ============================================================================

from django.core.management.base import BaseCommand, CommandError

from media_ai.models import GeneratedImage
from users.models import User


class Command(BaseCommand):
    help = "Seed a sample generated-image record for demo_user."

    def handle(self, *args, **options):
        try:
            demo_user = User.objects.get(username="demo_user")
        except User.DoesNotExist as exc:
            raise CommandError("Run 'python manage.py seed_users' first — demo_user not found.") from exc

        _, created = GeneratedImage.objects.get_or_create(
            user=demo_user,
            prompt="A calm sunrise over a quiet harbor, soft watercolor style",
            defaults={"status": "complete"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created sample GeneratedImage record."))
        else:
            self.stdout.write("Sample GeneratedImage record already exists — skipping.")

        self.stdout.write(self.style.SUCCESS("media_ai: seed complete."))