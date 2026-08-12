# ============================================================================
# App:  users
# File: management/commands/seed_users.py
# Run:  python manage.py seed_users
# Role: Creates a demo superuser and a demo regular user (with preferences)
#       for local development / testing the frontend against real data.
# ============================================================================

from django.core.management.base import BaseCommand
from django.db import transaction

from users.models import User, UserPreferences


class Command(BaseCommand):
    help = "Seed demo users for local development."

    @transaction.atomic
    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@Beta AI.local", "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin12345")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin' / password 'admin12345'"))
        else:
            self.stdout.write("Superuser 'admin' already exists — skipping.")

        demo_user, created = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@Beta AI.local", "is_email_verified": True},
        )
        if created:
            demo_user.set_password("demopass123")
            demo_user.save()
            UserPreferences.objects.get_or_create(user=demo_user)
            self.stdout.write(self.style.SUCCESS("Created demo user 'demo_user' / password 'demopass123'"))
        else:
            self.stdout.write("Demo user 'demo_user' already exists — skipping.")

        self.stdout.write(self.style.SUCCESS("users: seed complete."))