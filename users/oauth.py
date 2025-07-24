import requests
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from users.serializers import GoogleLoginSerializer
from rest_framework.response import Response
import os
import requests
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleLogineAPIView(CreateAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        token_response = requests.post(
         "https://oauth2.googleapis.com/token",
         data={
            "code": code,
            "client_id": os.environ.get('GOOGLE_CLIENT_ID'),
            "client_secret": os.environ.get('GOOGLE_CLIENT_SECRET'),
            "redirect_uri": os.environ.get('GOOGLE_REDIRECT_URI'),
            "grant_type": "authorization_code"
         }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "Invalid access token"}, status=400)

        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()
        print(f"user_data {user_info}")
        
        email = user_info.get["email"]
        given_name = user_info.get("given_name")
        family_name = user_info.get("family_name")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': given_name,
                'last_name': family_name
            }
        )

        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email

        return Response({"acces": str(refresh.access_token), "refresh_token": str(refresh)})
