from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .utils import refresh_axiom_tokens
from .models import TokenRefreshLog
import os
import datetime

def index(request):
    recent_logs = TokenRefreshLog.objects.all()[:10]
    latest_log = TokenRefreshLog.objects.filter(success=True).first()
    
    token_status = "Not found"
    last_modified = "N/A"
    
    if latest_log:
        token_status = "Token active"
        last_modified = latest_log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # Fallback to file check if no logs exist
        file_path = settings.TOKENS_FILE_PATH
        if os.path.exists(file_path):
            token_status = "Token file exists"
            mtime = os.path.getmtime(file_path)
            last_modified = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    return render(request, 'refresher/index.html', {
        'token_status': token_status,
        'last_modified': last_modified,
        'recent_logs': recent_logs,
    })

def trigger_refresh(request):
    if request.method == 'POST':
        success, message = refresh_axiom_tokens()
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    return redirect('index')
