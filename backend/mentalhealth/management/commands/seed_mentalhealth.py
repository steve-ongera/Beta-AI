# ============================================================================
# App:  mentalhealth
# File: management/commands/seed_mentalhealth.py
# Run:  python manage.py seed_mentalhealth
# Role: Creates a demo chat session with a few messages for demo_user (see
#       users/seed_users.py) — including one high-risk-flagged message and
#       its CrisisEscalation record, so the UI's risk/crisis styling and
#       the admin's escalation review queue both have something to show.
# ============================================================================

from django.core.management.base import BaseCommand, CommandError

from mentalhealth.models import ChatSession, CrisisEscalation, Message
from users.models import User


class Command(BaseCommand):
    help = "Seed a demo mental-health conversation for demo_user."

    def handle(self, *args, **options):
        try:
            demo_user = User.objects.get(username="demo_user")
        except User.DoesNotExist as exc:
            raise CommandError("Run 'python manage.py seed_users' first — demo_user not found.") from exc

        session, created = ChatSession.objects.get_or_create(
            user=demo_user,
            title="Feeling anxious about work",
            defaults={"is_guest_session": False},
        )
        if not created:
            self.stdout.write("Demo session already exists — skipping message seed.")
            return

        turns = [
            (Message.Role.USER, "I've been feeling really anxious about a presentation tomorrow.", "none"),
            (
                Message.Role.ASSISTANT,
                "That sounds stressful. Presentations can bring up a lot of anticipatory anxiety — "
                "would it help to talk through what specifically feels most worrying about it?",
                "none",
            ),
            (Message.Role.USER, "I just feel like I want to hurt myself if it goes badly.", "high_risk"),
        ]

        last_user_message = None
        for role, content, risk in turns:
            last_user_message = Message.objects.create(
                session=session, role=role, content=content, risk_flag=risk,
                model_version="seed_data" if role == Message.Role.ASSISTANT else "",
            )

        CrisisEscalation.objects.create(
            message=last_user_message,
            session=session,
            reason="seed_data_demo",
            resources_shown=[{"name": "988 Suicide & Crisis Lifeline (US)", "contact": "call or text 988"}],
        )

        self.stdout.write(self.style.SUCCESS(f"Created demo session '{session.title}' with {len(turns)} messages "
                                              "and 1 crisis escalation."))
        self.stdout.write(self.style.SUCCESS("mentalhealth: seed complete."))