from django.db import models

class IP(models.Model):
    ip = models.CharField(max_length=127)
    time = models.DateTimeField(null=True, default=None)
    requests = models.IntegerField(default=0)
    ban_counter = models.IntegerField(default=0)
    banned_for_life = models.BooleanField(default=False)

    def __unicode__(self):
        if self.banned_for_life:
            return self.ip + ' (Permanent ban)'
        return self.ip + ' Bans: ' + str(self.ban_counter)
