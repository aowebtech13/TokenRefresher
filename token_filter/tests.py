from django.test import TestCase
from .models import SolanaToken
from .services import PumpFunFilterService
from decimal import Decimal

class TokenFilterTestCase(TestCase):
    def setUp(self):
        self.service = PumpFunFilterService({
            'min_market_cap': Decimal('10000'),
            'min_liquidity': Decimal('5000'),
            'has_socials': True,
            'min_volume': Decimal('1000'),
            'min_age_seconds': 60,
            'min_holders': 20,
        })

    def test_token_passing_filter(self):
        """Test a token that meets all criteria"""
        token_data = {
            'mint': 'Address123',
            'name': 'Good Token',
            'symbol': 'GOOD',
            'market_cap': 15000,
            'usd_market_cap': 75000, # MC * 0.2 = 15000 liquidity in my mock logic
            'twitter': 'https://twitter.com/good',
            'website': 'https://good.com',
            'v24h': 2000,
            'created_timestamp': 0, # Very old
            'holder_count': 50,
        }
        token = self.service.filter_and_save_token(token_data)
        self.assertIsNotNone(token)
        self.assertTrue(token.is_passing_filter)
        self.assertEqual(token.name, 'Good Token')

    def test_token_failing_market_cap(self):
        """Test a token that fails market cap criteria"""
        token_data = {
            'mint': 'AddressFailMC',
            'name': 'Low MC',
            'symbol': 'LOW',
            'market_cap': 5000, # Too low
            'twitter': 'https://twitter.com/low',
            'holder_count': 50,
        }
        token = self.service.filter_and_save_token(token_data)
        # It still saves, but is_passing_filter should be False
        db_token = SolanaToken.objects.get(address='AddressFailMC')
        self.assertFalse(db_token.is_passing_filter)

    def test_token_failing_socials(self):
        """Test a token that fails socials criteria"""
        token_data = {
            'mint': 'AddressNoSocials',
            'name': 'No Socials',
            'symbol': 'NOSOC',
            'market_cap': 20000,
            'twitter': None,
            'website': '',
            'holder_count': 50,
        }
        self.service.filter_and_save_token(token_data)
        db_token = SolanaToken.objects.get(address='AddressNoSocials')
        self.assertFalse(db_token.is_passing_filter)

    def test_token_notified_status(self):
        """Test that is_notified defaults to False"""
        token_data = {
            'mint': 'AddressNotified',
            'market_cap': 20000,
            'twitter': 'exists',
            'holder_count': 50,
        }
        token = self.service.filter_and_save_token(token_data)
        self.assertFalse(token.is_notified)
