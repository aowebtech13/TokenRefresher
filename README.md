# Solana Pump.fun Token Filter & Refresher

A Django-based utility to automatically filter Solana tokens from pump.fun and manage Axiom tokens. Features a real-time dashboard with audio alerts and Telegram notifications.

## Features
- **Real-time Filtering**: Monitors pump.fun for tokens matching specific parameters (Market Cap, Liquidity, Socials, Volume, Age, Holders).
- **Dashboard**: Live-updating UI at `/tokens/dashboard/` with **Audio Ringtone** alerts for new matches.
- **Telegram Notifications**: Instant alerts sent to your Telegram bot when a token passes filters.
- **Axiom Refresher**: Management command to refresh Axiom API tokens.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Pip

### 2. Installation
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run migrations
python3 manage.py migrate
```

### 3. Configuration
Create a `.env` file in the root directory and fill in your details:
- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot API token.
- `TELEGRAM_CHAT_ID`: Your personal or group Telegram Chat ID.
- `AXIOM_REFRESH_URL`: The Axiom API endpoint for refreshing tokens.
- `AXIOM_REFRESH_TOKEN`: Your persistent Axiom refresh token.

### 4. Running the Filter
To start the automatic Solana token filtering system:
```bash
python3 manage.py start_filter
```
This command will continuously scan for new tokens and output matches to your console and Telegram.

### 5. Using the Dashboard
1. Start the Django server:
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```
2. Visit `http://127.0.0.1:8000/tokens/dashboard/` in your browser.
3. **Important**: Click anywhere on the dashboard once to enable **Audio Alerts**. The page will play a ringtone and auto-refresh whenever a new token is detected.

## Parameters Tracked
- **Market Cap**: Current valuation.
- **Liquidity**: Estimated bonding curve liquidity.
- **Socials**: Twitter and Website presence.
- **Volume**: 24h trading volume.
- **Age**: Time since token creation.
- **Holders**: Total holder count.

## Management Commands
- `python3 manage.py start_filter`: Runs the Solana filtering loop.
- `python3 manage.py refresh_tokens`: Refreshes Axiom API tokens.
- `python3 manage.py runserver`: Starts the web dashboard.
