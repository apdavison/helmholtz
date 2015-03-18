from django.db import models


class Publication(models.Model):
    authors = models.TextField()
    title = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200, help_text="Name of journal or book title and publisher")
    identifier = models.CharField(max_length=20, help_text="Volume and page numbers")
    doi = models.CharField(max_length=30)
    url = models.CharField(max_length=200)

    def __str__(self):
        return "{} ({}) {}. {} {} doi:{}".format(self.authors,
                                               self.date.year,
                                               self.title,
                                               self.venue,
                                               self.identifier,
                                               self.doi)
