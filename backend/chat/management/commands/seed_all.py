# ============================================================================
# App:  chat  (lives here since chat has no user-dependency and app order
#              doesn't matter for where this convenience command sits)
# File: management/commands/seed_all.py
# Run:  python manage.py seed_all
# Role: Runs every app's seed_* command in the order that satisfies their
#       dependencies (users -> chat -> mentalhealth -> media_ai).
# ============================================================================

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run all app seed_* commands in dependency order."

    def handle(self, *args, **options):
        for command_name in ["seed_users", "seed_modules", "seed_mentalhealth", "seed_media"]:
            self.stdout.write(self.style.MIGRATE_HEADING(f"Running {command_name}..."))
            call_command(command_name)

        self.stdout.write(self.style.SUCCESS("\nAll apps seeded."))