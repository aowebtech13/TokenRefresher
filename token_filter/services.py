import requests
import time
import os
from .models import SolanaToken
from decimal import Decimal

import json
import websocket
import threading

class SolanaWebSocketService:
    WS_URL = "wss://pumpportal.fun/api/data" # Example high-speed pump.fun data stream
    
    def __init__(self, filter_service):
        self.filter_service = filter_service
        self.ws = None
        self.is_running = False

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            # Intercept "new token" or "trade" messages
            if data.get('txType') == 'create' or 'mint' in data:
                token = self.filter_service.filter_and_save_token(data)
                if token and token.is_passing_filter:
                    # Logic ends with having token name and address immediately
                    print(f"🔥 REAL-TIME MATCH: {token.name} | {token.address}")
                    
                    # Notify via Telegram
                    msg = (
                        f"⚡ <b>REAL-TIME: {token.name}</b>\n"
                        f"<code>{token.address}</code>\n"
                        f"MCap: ${token.market_cap:,.0f} | Holders: {token.holders_count}"
                    )
                    TelegramService.send_message(msg)
        except Exception as e:
            print(f"WS Message Error: {e}")

    def on_error(self, ws, error):
        print(f"WS Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WS Connection Closed. Refreshing token and reconnecting...")
        if self.is_running:
            time.sleep(5)
            self.start_async()

    def on_open(self, ws):
        print("WS Connection Opened. Subscribing to token streams...")
        # Example subscription for pump.fun real-time mints
        payload = {"method": "subscribeNewToken"}
        ws.send(json.dumps(payload))

    def start_async(self):
        self.is_running = True
        self.ws = websocket.WebSocketApp(
            self.WS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

class TelegramService:
    @staticmethod
    def send_message(message):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if not token or not chat_id:
            return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")

class PumpFunFilterService:
    BASE_API_URL = "https://frontend-api.pump.fun/coins"
    
    def __init__(self, config=None):
        self.config = config or {
            'min_market_cap': Decimal(os.getenv('MIN_MARKET_CAP', '10000')),
            'min_liquidity': Decimal(os.getenv('MIN_LIQUIDITY', '5000')),
            'has_socials': True,
            'min_volume': Decimal(os.getenv('MIN_VOLUME', '1000')),
            'min_age_seconds': int(os.getenv('MIN_AGE_SECONDS', '60')),
            'min_holders': int(os.getenv('MIN_HOLDERS', '20')),
        }

    def fetch_latest_tokens(self):
        """Fetch latest tokens from pump.fun frontend API"""
        try:
            # Note: This is a placeholder URL, pump.fun API structure might vary
            response = requests.get(f"{self.BASE_API_URL}/latest", params={'limit': 50}, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching tokens: {e}")
            return []

    def filter_and_save_token(self, token_data):
        """Apply filtering logic and save to DB if it passes"""
        try:
            address = token_data.get('mint')
            if not address:
                return None

            # Map fields from API (this depends on the actual pump.fun API response structure)
            name = token_data.get('name', 'Unknown')
            symbol = token_data.get('symbol', 'Unknown')
            market_cap = Decimal(str(token_data.get('market_cap', 0)))
            # Liquidity is often estimated or fetched from a different endpoint
            liquidity = Decimal(str(token_data.get('usd_market_cap', 0))) * Decimal('0.2') # Rough estimate for pump.fun bonding curve
            
            twitter = token_data.get('twitter')
            website = token_data.get('website')
            volume = Decimal(str(token_data.get('v24h', 0)))
            
            created_timestamp = token_data.get('created_timestamp', time.time() * 1000)
            age_seconds = int(time.time() - (created_timestamp / 1000))
            holders = token_data.get('holder_count', 0)

            # Filtering logic
            is_passing = True
            if market_cap < self.config['min_market_cap']: is_passing = False
            if liquidity < self.config['min_liquidity']: is_passing = False
            if self.config['has_socials'] and not (twitter or website): is_passing = False
            if volume < self.config['min_volume']: is_passing = False
            if age_seconds < self.config['min_age_seconds']: is_passing = False
            if holders < self.config['min_holders']: is_passing = False

            token, created = SolanaToken.objects.update_or_create(
                address=address,
                defaults={
                    'name': name,
                    'symbol': symbol,
                    'market_cap': market_cap,
                    'liquidity': liquidity,
                    'twitter': twitter,
                    'website': website,
                    'volume_24h': volume,
                    'age_seconds': age_seconds,
                    'holders_count': holders,
                    'is_passing_filter': is_passing,
                    # Optional fields (placeholders if available)
                    'dev_hold_percent': Decimal(str(token_data.get('dev_hold_percent', 0))),
                    'top_10_percent': Decimal(str(token_data.get('top_10_percent', 0))),
                }
            )
            
            if is_passing:
                print(f"TOKEN PASSED: {name} ({symbol}) - {address}")
            return token

        except Exception as e:
            print(f"Error filtering token {token_data.get('mint')}: {e}")
            return None

    def run_filter_cycle(self):
        """Run a full cycle of fetching and filtering"""
        tokens = self.fetch_latest_tokens()
        passed_tokens = []
        for token_data in tokens:
            passed = self.filter_and_save_token(token_data)
            if passed:
                passed_tokens.append(passed)
                # Send real-time notification
                msg = (
                    f"🚀 <b>New Token Passed Filter!</b>\n\n"
                    f"<b>Name:</b> {passed.name} ({passed.symbol})\n"
                    f"<b>MCap:</b> ${passed.market_cap:,.0f}\n"
                    f"<b>Liq:</b> ${passed.liquidity:,.0f}\n"
                    f"<b>Holders:</b> {passed.holders_count}\n"
                    f"<b>Address:</b> <code>{passed.address}</code>\n\n"
                    f"<b>Socials:</b> "
                )
                if passed.twitter: msg += f"<a href='{passed.twitter}'>Twitter</a> "
                if passed.website: msg += f"<a href='{passed.website}'>Web</a>"
                
                TelegramService.send_message(msg)
                
        return passed_tokens
