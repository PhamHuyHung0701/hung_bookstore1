"""
Customer Service API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Customer
from .serializers import (
    CustomerSerializer, 
    CustomerRegistrationSerializer, 
    CustomerLoginSerializer
)


@api_view(['POST'])
def register(request):
    """
    API endpoint for customer registration
    POST /api/customers/register/
    """
    serializer = CustomerRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        customer = Customer(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']  # Lưu plain text
        )
        customer.save()
        
        return Response({
            'success': True,
            'message': 'Đăng ký thành công!',
            'customer': CustomerSerializer(customer).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    API endpoint for customer login
    POST /api/customers/login/
    """
    serializer = CustomerLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                return Response({
                    'success': True,
                    'message': f'Chào mừng {customer.name}!',
                    'customer': CustomerSerializer(customer).data
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Mật khẩu không đúng!'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Email không tồn tại!'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_customer(request, customer_id):
    """
    API endpoint to get customer by ID
    GET /api/customers/<customer_id>/
    """
    try:
        customer = Customer.objects.get(id=customer_id)
        return Response({
            'success': True,
            'customer': CustomerSerializer(customer).data
        })
    except Customer.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy khách hàng!'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def list_customers(request):
    """
    API endpoint to list all customers
    GET /api/customers/
    """
    customers = Customer.objects.all()
    return Response({
        'success': True,
        'customers': CustomerSerializer(customers, many=True).data
    })


@api_view(['GET'])
def check_customer_exists(request, customer_id):
    """
    API endpoint to check if customer exists (used by other services)
    GET /api/customers/<customer_id>/exists/
    """
    exists = Customer.objects.filter(id=customer_id).exists()
    return Response({
        'exists': exists
    })
