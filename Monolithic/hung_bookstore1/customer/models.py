from django.db import models


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        """Lưu mật khẩu plain text"""
        self.password = raw_password

    def check_password(self, raw_password):
        """So sánh mật khẩu plain text"""
        return self.password == raw_password
