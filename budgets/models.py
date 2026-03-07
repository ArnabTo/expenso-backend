from django.db import models
from django.conf import settings
from expenses.models import Category


class Budget(models.Model):
    """Monthly budget goal per category for a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.PositiveSmallIntegerField()  # 1–12
    year = models.PositiveIntegerField()

    class Meta:
        db_table = 'budgets'
        unique_together = ('user', 'category', 'month', 'year')
        indexes = [
            models.Index(fields=['user', 'year', 'month']),
        ]
        ordering = ['-year', '-month']

    def __str__(self):
        return f'{self.user.email} - {self.category.name} ({self.month}/{self.year}): {self.amount}'
