from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Country(models.Model):
    country_name = models.CharField(max_length=100, primary_key=True)
    euro_flag_url = models.URLField(max_length=300, null=True, default=None, blank=True) #TBD later
    final_order = models.IntegerField(default=None, null=True, blank=True)

    def __str__ (self):
        return self.country_name
    
    class Meta:
        verbose_name_plural = "Countries"

class Contestant(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100, primary_key=True)
    about = models.TextField(default=None, null=True, blank=True)

    def __str__ (self):
        return self.artist

    class Meta:
        verbose_name_plural = "Contestants"

class Song(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, primary_key=True)
    yt_video_url = models.URLField(max_length=200, default=None, null=True, blank=True)
    lyrics_original = models.TextField(default=None, null=True, blank=True)
    lyrics_translated = models.TextField(default=None, null=True, blank=True)

    def __str__ (self):
        return self.title

    class Meta:
        verbose_name_plural = "Songs"

class Voter(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    #generate username from first letter of first name and last name
    def save(self, *args, **kwargs):
        self.username = self.first_name[0].lower() + self.last_name.lower()
        super(Voter, self).save(*args, **kwargs)

    def __str__ (self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Voters"

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    #1. Song quality - lyrics, melody, and harmony
    song_quality = models.IntegerField(default=None, null=True)
    #2. Stage presence - costume, lighting, and choreography
    stage_presence = models.IntegerField(default=None, null=True)
    #3. Vocal performance - pitch, tone, and range
    vocal_performance = models.IntegerField(default=None, null=True)
    
    def __str__ (self):
        return self.participant.username + " voted for " + self.song.title
    
    class Meta:
        verbose_name_plural = "Votes"

@receiver(post_save, sender=Voter)
def create_votes(sender, instance, created, **kwargs):
    if created:
        for song in Song.objects.all():
            Vote.objects.create(voter=instance, song=song)