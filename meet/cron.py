from django_cron import CronJobBase, Schedule
from django.db.models import F
from meet.models import FreeSlot

class ResetFreeSlotsCronJob(CronJobBase):
    RUN_EVERY_MINS = 0  # Run once a month

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'meet.reset_free_slots_cron_job'  # Unique identifier for this cron job

    def do(self):
        FreeSlot.objects.all().update(free_slots=F('total'))
