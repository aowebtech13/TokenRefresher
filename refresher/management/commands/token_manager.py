import time
import os
from django.core.management.base import BaseCommand
from refresher.utils import refresh_axiom_tokens

TRIGGER_FILE = 'SCREEN0_REFRESH_TRIGGER'
REFRESH_INTERVAL = 300  # 5 minutes in seconds

class Command(BaseCommand):
    help = 'Manages periodic and trigger-based token refreshing'

    def handle(self, *args, **options):
        self.stdout.write("Starting token manager...")
        
        # Initial refresh
        self.perform_refresh("Initial startup")
        
        last_refresh_time = time.time()
        
        while True:
            current_time = time.time()
            
            # Check for file trigger
            if os.path.exists(TRIGGER_FILE):
                self.stdout.write(f"Trigger file {TRIGGER_FILE} detected.")
                self.perform_refresh("File trigger")
                try:
                    os.remove(TRIGGER_FILE)
                except Exception as e:
                    self.stderr.write(f"Could not remove trigger file: {e}")
                last_refresh_time = current_time
            
            # Check for periodic refresh (5 minutes)
            elif current_time - last_refresh_time >= REFRESH_INTERVAL:
                self.perform_refresh("Periodic 5-minute interval")
                last_refresh_time = current_time
            
            # Sleep for a short duration to avoid high CPU usage
            time.sleep(5)

    def perform_refresh(self, reason):
        self.stdout.write(f"Performing refresh: {reason}")
        success, message = refresh_axiom_tokens()
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stderr.write(self.style.ERROR(message))
