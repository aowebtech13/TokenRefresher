from django.core.management.base import BaseCommand
import time
from token_filter.services import PumpFunFilterService

class Command(BaseCommand):
    help = 'Runs the Solana pump.fun token filter service'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Solana pump.fun token filter...'))
        
        service = PumpFunFilterService()
        
        try:
            while True:
                passed_tokens = service.run_filter_cycle()
                
                if passed_tokens:
                    self.stdout.write(self.style.SUCCESS(f"Found {len(passed_tokens)} tokens passing filters:"))
                    for token in passed_tokens:
                        self.stdout.write(f"NAME: {token.name} | ADDRESS: {token.address}")
                else:
                    self.stdout.write(self.style.WARNING("No tokens passed filters in this cycle."))
                
                # Wait before the next cycle to avoid rate limiting
                time.sleep(10)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Filter service stopped by user.'))
