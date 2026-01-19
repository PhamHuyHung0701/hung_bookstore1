from django.db import models


class Customer(models.Model):
    """Customer model - maps to 'customers' table"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Plain text password
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name

    def check_password(self, raw_password):
        """Check password - plain text comparison"""
        return self.password == raw_password
