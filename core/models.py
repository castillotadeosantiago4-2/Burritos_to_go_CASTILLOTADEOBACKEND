from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('super', 'Súper Usuario'),
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='cliente')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"


class Pedido(models.Model):
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estatus = models.CharField(max_length=20, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        return sum(p.precio for p in self.productos.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda primero para generar pk
        self.total = self.calcular_total()
        super().save(update_fields=['total'])

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"
