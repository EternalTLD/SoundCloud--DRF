from django.shortcuts import render


def google_login_view(request):
    """Google login view"""
    return render(request, 'oauth/google_login.html')