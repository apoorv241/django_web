from django.db import models



class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TimePeriod(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Game(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    photo_url = models.URLField(max_length=500)

    website_url = models.URLField(max_length=500)

    review = models.TextField()
    about_the_game = models.TextField()

    timeperiod = models.ForeignKey(
        TimePeriod,
        on_delete=models.PROTECT,
        related_name="games"
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="games"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "region", "timeperiod"],
                name="unique_military_game_assignment"
            )
        ]

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    photo_url = models.URLField(max_length=500)
    buy_url = models.URLField(max_length=500,default=None, blank=True, null=True)
    review = models.TextField()
    about_the_author = models.TextField()

    timeperiod = models.ForeignKey(
        TimePeriod,
        on_delete=models.PROTECT,
        related_name="books"
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="books"
    )

    def __str__(self):
        return self.name


class VideoPlaylist(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        max_length=255,
        unique=True
    )

    about = models.TextField(
        blank=True,
        default=""
    )

    youtube_playlist_url = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="video_playlists",
        blank=True,
        null=True
    )

    timeperiod = models.ForeignKey(
        TimePeriod,
        on_delete=models.PROTECT,
        related_name="video_playlists",
        blank=True,
        null=True
    )

    
    def __str__(self):
        return self.name

class Video(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=255)

    url = models.URLField(max_length=500)

    transcript = models.TextField(
        blank=True,
        default=""
    )

    about_the_video = models.TextField()

    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    episode_number = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    playlist = models.ForeignKey(
        VideoPlaylist,
        on_delete=models.SET_NULL,
        related_name="videos",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title