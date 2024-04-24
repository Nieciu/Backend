from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    country_name = models.CharField(max_length=100, blank=False)
    # number_of_wins = models.IntegerField(default=0)

    def __str__ (self):
        return self.country_name
    
    class Meta:
        verbose_name_plural = "Countries"

class Contestant(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100, primary_key=True)
    about = models.TextField()

    def __str__ (self):
        return self.artist

    class Meta:
        verbose_name_plural = "Contestants"

class Song(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, primary_key=True, blank=False)
    yt_video_url = models.URLField(max_length=200, blank=False)

    def __str__ (self):
        return self.title

    class Meta:
        verbose_name_plural = "Songs"

class Participant(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

    #generate username from first letter of first name and last name
    def save(self, *args, **kwargs):
        self.username = self.first_name[0].lower() + self.last_name.lower()
        super(Participant, self).save(*args, **kwargs)

    def __str__ (self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Participants"

class Vote(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    #1. Song quality - lyrics, melody, and harmony
    song_quality = models.IntegerField(default=0)
    #2. Stage presence - costume, lighting, and choreography
    stage_presence = models.IntegerField(default=0)
    #3. Vocal performance - pitch, tone, and range
    vocal_performance = models.IntegerField(default=0)
    
    def __str__ (self):
        return self.participant.username + " voted for " + self.song.title
    
    class Meta:
        verbose_name_plural = "Votes"