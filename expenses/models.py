
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Member(models.Model):
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    group = models.ForeignKey(Group, related_name='expenses', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='expenses', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    participants = models.ManyToManyField(Member, related_name='expenses_participated')

    def __str__(self):
        return f"{self.cate} - {self.amount} on {self.date}"

    def split_amount(self, num_people):
        return round(self.amount / num_people, 2)
    



