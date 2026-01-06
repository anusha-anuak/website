import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuyNexa.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_dummy_social_app():
    # Ensure site exists
    site, created = Site.objects.get_or_create(id=1, defaults={'domain': '127.0.0.1:8000', 'name': 'ShoeStore'})
    if created:
        print(f"Created Site: {site}")
    
    # Create or update SocialApp
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google',
        defaults={
            'client_id': 'dummy-client-id',
            'secret': 'dummy-secret',
        }
    )
    if created:
        print("Created dummy Google SocialApp.")
    else:
        print("Google SocialApp already exists.")
    
    app.sites.add(site)
    print("Added site to Google SocialApp.")

if __name__ == '__main__':
    setup_dummy_social_app()
