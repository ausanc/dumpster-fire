from django.db import models


class Hook(models.Model):
    #  ACTION = (
    #     ('N', 'Notify'),
    #     ('K', 'Send New Key'),
    #     ...,
    # )

    account_url = models.URLField(max_length=200, null=False, blank=False, default=None)
    game_id = models.CharField(max_length=255, null=False, blank=False, default=None)
    achievement_id = models.CharField(max_length=255, null=False, blank=False, default=None)
    ach_name = models.CharField(max_length=255, null=False, blank=False, default=None)
    icon_url = models.CharField(max_length=255, null=False, blank=False, default=None)
    game_name = models.CharField(max_length=255, null=False, blank=False, default=None)
    profile_name = models.CharField(max_length=255, null=False, blank=False, default=None)
    completed = models.BooleanField(null=False, default=False)
    # action_on_complete = models.CharField(max_length=1, choices=ACTIONS)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(auto_now_add=False, editable=False, null=True, blank=True, default=None)
