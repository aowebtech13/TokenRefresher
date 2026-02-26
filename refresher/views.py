from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import refresh_axiom_tokens, TOKENS_FILE
import os
import datetime

def index(request):
    token_status = "Not found"
    last_modified = "N/A"
    
    if os.path.exists(TOKENS_FILE):
        token_status = "Token file exists"
        mtime = os.path.getmtime(TOKENS_FILE)
        last_modified = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    return render(request, 'refresher/index.html', {
        'token_status': token_status,
        'last_modified': last_modified,
    })

def trigger_refresh(request):
    if request.method == 'POST':
        success, message = refresh_axiom_tokens()
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    return redirect('index')
