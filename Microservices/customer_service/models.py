"""
Customer Service Models
"""
from django.db import models


class Customer(models.Model):
    """Customer model for customer_service"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        managed = False  # Table managed by SQL script

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        """Lưu mật khẩu plain text (không mã hóa)"""
        self.password = raw_password

    def check_password(self, raw_password):
        """So sánh mật khẩu plain text"""
        return self.password == raw_password

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
