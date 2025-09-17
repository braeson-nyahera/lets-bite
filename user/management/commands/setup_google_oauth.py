from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

class Command(BaseCommand):
    help = 'Set up Google OAuth Social Application'

    def add_arguments(self, parser):
        parser.add_argument('--client-id', type=str, help='Google OAuth Client ID', required=True)
        parser.add_argument('--client-secret', type=str, help='Google OAuth Client Secret', required=True)

    def handle(self, *args, **options):
        client_id = options['client_id']
        client_secret = options['client_secret']

        # Get or create the default site
        site = Site.objects.get(pk=1)
        
        # Create or update the Google social app
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            # Update existing app
            social_app.client_id = client_id
            social_app.secret = client_secret
            social_app.save()
            
        # Add the site to the social app
        social_app.sites.add(site)
        
        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} Google Social Application successfully!\n'
                f'Name: {social_app.name}\n'
                f'Provider: {social_app.provider}\n'
                f'Client ID: {social_app.client_id[:10]}...\n'
                f'Sites: {[site.domain for site in social_app.sites.all()]}'
            )
        )