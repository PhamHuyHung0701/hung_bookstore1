from django.db import models
from django.db.models import Avg


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title

    def is_available(self):
        return self.stock_quantity > 0

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(r.score for r in ratings) / ratings.count()
        return 0

    @classmethod
    def recommend_for_customer(cls, customer_id, limit=5):
        """
        Simple recommendation:
        - Books the customer bought previously -> recommend similar authors
        - Or top-rated books overall
        """
        bought_authors = (
            cls.objects.filter(orderitem__order__customer_id=customer_id)
            .values_list('author', flat=True).distinct()
        )
        qs = cls.objects.none()
        if bought_authors:
            qs = cls.objects.filter(author__in=list(bought_authors)).order_by('-stock_quantity')
        if not qs.exists():
            qs = cls.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
        return qs[:limit]


class Rating(models.Model):
    customer_id = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField()

    class Meta:
        db_table = 'ratings'
        unique_together = ('customer_id', 'book')


class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.name} ({self.role})"
