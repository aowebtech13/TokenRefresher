from django.core.management.base import BaseCommand
from refresher.utils import refresh_axiom_tokens

class Command(BaseCommand):
    help = 'Refreshes Axiom tokens and logs the result'

    def handle(self, *args, **options):
        self.stdout.write('Starting token refresh...')
        success, message = refresh_axiom_tokens()
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))
