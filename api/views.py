from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Endpoint para login do usuário.
    
    Parâmetros:
        username: Nome de usuário
        password: Senha
        
    Retorna:
        token: Token de autenticação
        user_id: ID do usuário
        username: Nome do usuário
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Por favor, forneça username e password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Credenciais inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Endpoint para logout do usuário.
    Remove o token de autenticação do usuário.
    """
    try:
        # Deleta o token do usuário
        request.user.auth_token.delete()
        return Response(
            {'message': 'Logout realizado com sucesso'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
