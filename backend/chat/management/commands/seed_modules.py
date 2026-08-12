# ============================================================================
# App:  chat
# File: management/commands/seed_modules.py
# Run:  python manage.py seed_modules
# Role: Registers the mentalhealth module (and a couple of inactive
#       placeholder modules) in the AIModule registry so the frontend's
#       ModuleSwitcher / GET /api/modules/ has real data to render.
# ============================================================================

from django.core.management.base import BaseCommand

from chat.models import AIModule


class Command(BaseCommand):
    help = "Seed the AI-app module registry."

    def handle(self, *args, **options):
        modules = [
            {
                "slug": "mental-health",
                "name": "Mental Health",
                "description": "Talk through what's on your mind with doctor-reviewed guidance.",
                "icon": "bi-chat-heart",
                "is_active": True,
                "requires_auth_for_full_access": True,
                "api_base_path": "/api/modules/mental-health/",
            },
            {
                "slug": "nutrition",
                "name": "Nutrition",
                "description": "Coming soon — nutrition and wellness guidance.",
                "icon": "bi-apple",
                "is_active": False,
                "requires_auth_for_full_access": True,
                "api_base_path": "/api/modules/nutrition/",
            },
        ]

        for data in modules:
            slug = data.pop("slug")
            obj, created = AIModule.objects.update_or_create(slug=slug, defaults=data)
            verb = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{verb} module '{slug}'"))

        self.stdout.write(self.style.SUCCESS("chat: seed complete."))