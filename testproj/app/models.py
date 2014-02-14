"""Made-up models to use for testing."""
from django.db import models


class PublisherType(models.Model):
    """Classifications for publishers.

    Examples are "family," "multinational." Doesn't map cleanly to a
    real-world concept that I know of, but it *does* let the demo show that
    <select> fields get populated appropriately.

    """
    description = models.CharField(max_length=50)

    def __str__(self):
        """Present the description by itself."""
        return self.description


class Publisher(models.Model):
    """A publisher of titles."""

    name = models.CharField(max_length=50)

    location = models.CharField(max_length=50)

    classification = models.ForeignKey(PublisherType)


class Title(models.Model):
    """A thing that gets published."""

    name = models.CharField(max_length=50)

    synposis = models.TextField()

    release_date = models.DateField()

    publisher = models.ForeignKey(Publisher)
