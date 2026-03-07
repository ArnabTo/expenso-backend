from django.db import models
from django.conf import settings


class SavingsPlan(models.Model):
    """DPS (Deposit Pension Scheme) style savings plan."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='savings_plans',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    monthly_deposit = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'savings_plans'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.name}'

    @property
    def total_saved(self):
        return self.transactions.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    @property
    def progress_percentage(self):
        if not self.target_amount:
            return 0
        return round((float(self.total_saved) / float(self.target_amount)) * 100, 1)


class SavingsTransaction(models.Model):
    """Individual deposit into a savings plan."""
    plan = models.ForeignKey(
        SavingsPlan,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'savings_transactions'
        ordering = ['-date']

    def __str__(self):
        return f'{self.plan.name} - ${self.amount} on {self.date}'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'savings_transactions'
        indexes = [
            models.Index(fields=['plan', 'date']),
        ]
        ordering = ['-date']

    def __str__(self):
        return f'{self.plan.name} - {self.amount} on {self.date}'
