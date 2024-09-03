from django.core.management.base import BaseCommand
from ....tms_manager.models import Campaign, Member, Task
import random
import uuid


class Command(BaseCommand):
    help = 'Create Dummy data for Campaigns, Members and Tasks'

    def handle(self, *args, **kwargs):
        # Creating dummy Campaigns
        campaigns = [Campaign.objects.create(name=f"Campaign {i}") for i in range(5)]
        self.stdout.write(self.style.SUCCESS("Dummy campaigns Created."))

        roles = ["trainer", "lead"]
        members = []
        for i in range(10):
            member = Member.objects.create(
                role=random.choice(roles),
                email=f"user{i}@dummy.com",
                full_name=f"User {i}"
            )
            members.append(member)
            member.campaign.set(random.sample(campaigns, random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("Dummy members created."))

        # Creating dummy tasks
        for i in range(20):
            Task.objects.create(
                id=uuid.uuid4(),
                status=random.choice(["in progress", "pending", "submitted", "reviewed"]),
                name=f"Task {i}",
                score=random.randint(0,100),
                campaign=random.choice(campaigns),
                trainer=random.choice([member for member in members if member.role == "trainer"]),
                lead=random.choice([member for member in members if member.role == "trainer"]),
            )

        self.stdout.write(self.style.SUCCESS("Dummy tasks created."))
