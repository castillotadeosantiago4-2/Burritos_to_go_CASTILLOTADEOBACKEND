from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Usuario, Producto, Categoria, Pedido
from .serializers import (
    UsuarioSerializer,
    ProductoSerializer,
    CategoriaSerializer,
    PedidoSerializer,
    CrearPedidoSerializer
)

# ViewSets CRUD automáticos
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        productos = serializer.validated_data.get('productos', [])
        total = sum([p.precio for p in productos])
        serializer.save(cliente=self.request.user, total=total)


# Endpoint personalizado para crear pedidos
class CrearPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        productos_ids = request.data.get('productos', [])
        productos = Producto.objects.filter(id__in=productos_ids, activo=True)

        if not productos.exists():
            return Response({'error': 'No se encontraron productos válidos.'}, status=400)

        total = sum([p.precio for p in productos])
        cliente = request.user

        if cliente.saldo < total:
            return Response({
                'error': 'Saldo insuficiente.',
                'saldo_actual': cliente.saldo,
                'total_pedido': total,
                'faltante': round(total - cliente.saldo, 2)
            }, status=400)

        pedido = Pedido.objects.create(
            cliente=cliente,
            total=total,
            estatus='pendiente',
            fecha=timezone.now()
        )
        pedido.productos.set(productos)
        cliente.saldo -= total
        cliente.save()

        return Response({
            'mensaje': 'Pedido creado exitosamente.',
            'pedido_id': pedido.id,
            'total': total,
            'productos': [p.nombre for p in productos],
            'fecha': pedido.fecha,
            'saldo_restante': cliente.saldo
        })
