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
