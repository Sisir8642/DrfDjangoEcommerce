from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from products.permissions import IsAdmin, IsCustomer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomer()]
        elif self.action in ['change_status']:
            return [IsAdmin()]
        elif self.action == 'destroy':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user and request.user.role != 'admin':
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != 'pending':
            return Response({'detail': 'Cannot cancel non-pending orders'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()
        return Response({'detail': 'Order cancelled'}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
            request_body = OrderStatusUpdateSerializer
            
    )
    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def patch(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            new_status = serializer.validated_data.get('status')
            if new_status not in dict(Order.STATUS):
                return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'detail': f'Status updated to {new_status}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
