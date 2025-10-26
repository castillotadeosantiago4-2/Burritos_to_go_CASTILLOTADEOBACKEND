from rest_framework import serializers
from .models import Usuario, Producto,Categoria, Pedido
class UsuarioSerializer(serializers.ModelSerializer):
 class Meta:
  model = Usuario
  fields = ['id', 'username', 'email', 'rol','saldo']
class ProductoSerializer(serializers.ModelSerializer):
 class Meta:
  model = Producto
  fields = '__all__'
class CategoriaSerializer(serializers.ModelSerializer):
 class Meta:
  model = Categoria
  fields = '__all__'
class PedidoSerializer(serializers.ModelSerializer):
 class Meta:
  model = Pedido
  fields = '__all__'
  extra_kwargs = {'cliente': {'read_only': True},'total': {'read_only': True}
 }
class CrearPedidoSerializer(serializers.Serializer
):
 productos = serializers.ListField(
 child=serializers.IntegerField(),
 allow_empty=False
 )
 def validate_productos(self, value):
  productos = Producto.objects.filter(id__in=value,activo=True)
  if not productos.exists():
   raise serializers.ValidationError("No se encontraron productos válidos.")
   return value         