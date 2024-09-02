import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Campaign Unique ID.")
    name = models.CharField(max_length=255, help_text="Campaign Name.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the campaign was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the campaign was updated.")

    class Meta:
        ordering = ['name']
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'

    def __str__(self):
        return self.name


class Member(models.Model):
    ROLE_CHOICES = (
        ("Trainer", "trainer"),
        ("Lead", "lead")
    )
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, help_text="Member Role.")
    email = models.EmailField(primary_key=True, help_text="Member email, also primary key.")
    full_name = models.CharField(max_length=255, help_text="Member full name.")
    campaign = models.ManyToManyField(Campaign, related_name="members", help_text="Member's Campaign Foreign keys.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the member was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the member was updated.")

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return self.full_name


class Task(models.Model):
    STATUS_CHOICES = (
        ("in progress", "In Progress"),
        ("pending", "Pending"),
        ("submitted", "Submitted"),
        ("reviewed", "Reviewed")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, help_text="Task's status.")
    name = models.CharField(max_length=255, help_text="Task's name.")
    score = models.FloatField(
        help_text="Task's continuous Score, can vary from 1.0 to 7.0.",
        validators=[MinValueValidator(1.0), MaxValueValidator(7.0)]
    )
    campaign = models.ManyToManyField(Campaign, ralated_name="tasks", help_text="Member's Campaign Foreign keys.")
    trainer = models.ManyToManyField(
        Member,
        related_name="tasks",
        limit_choices_to={"role": "Trainer"},
        help_text="Member's (trainer) Campaign Foreign keys."
    )
    lead = models.ManyToManyField(
        Member,
        related_name="reviewed_tasks",
        limit_choices_to={"role": "Lead"},
        help_text="Member's (trainer) Campaign Foreign keys."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the task was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the task was updated.")

    class Meta:
        ordering = ['name']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.name
