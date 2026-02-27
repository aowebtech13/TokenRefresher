from django.core.management.base import BaseCommand
import time
from token_filter.services import PumpFunFilterService, SolanaWebSocketService

class Command(BaseCommand):
    help = 'Runs the Solana pump.fun token filter service with WebSocket real-time interception'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Solana real-time WebSocket filter...'))
        
        filter_service = PumpFunFilterService()
        ws_service = SolanaWebSocketService(filter_service)
        
        # Start the WebSocket in a background thread
        ws_service.start_async()
        
        try:
            # Main loop for background tasks or backup polling
            while True:
                # You can still run a backup poll cycle or just keep the process alive
                filter_service.run_filter_cycle()
                time.sleep(15) 
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Filter service stopped.'))
