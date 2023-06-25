from django.db import models

from users.models import User


class CardItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    price = models.PositiveIntegerField()
    images = models.ImageField(upload_to="mobi_market/card_items/", blank=True, null=True)
    short_description = models.CharField(max_length=150)
    detailed_description = models.TextField()

    def __str__(self):
        return f"id: {self.pk} - user_id: {self.user_id} - title{self.title}"

    class Meta:
        verbose_name = "Card item"
        verbose_name_plural = "Card items"
