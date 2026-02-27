from django.http import JsonResponse
from .models import SolanaToken

def dashboard(request):
    tokens = SolanaToken.objects.filter(is_passing_filter=True).order_by('-created_at')[:50]
    return render(request, 'token_filter/dashboard.html', {'tokens': tokens})

def get_new_tokens(request):
    """API endpoint to poll for new unnotified tokens"""
    new_tokens = SolanaToken.objects.filter(is_passing_filter=True, is_notified=False)
    data = []
    for token in new_tokens:
        data.append({
            'name': token.name,
            'symbol': token.symbol,
            'address': token.address,
            'market_cap': float(token.market_cap or 0),
        })
        token.is_notified = True
        token.save()
    return JsonResponse({'new_tokens': data})
