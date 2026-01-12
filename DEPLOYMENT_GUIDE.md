# Cloudbet Arbitrage Bot - Deployment Guide

## GitHub Repository Setup ✅
Your project has been successfully pushed to GitHub:
- **Repository**: https://github.com/githuobgithuot-hlo/temp.git
- **Branch**: main

## Railway Deployment Instructions

### Step 1: Create a Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with your GitHub account (recommended for easy integration)
3. Authorize Railway to access your GitHub repositories

### Step 2: Create a New Railway Project
1. Click **"+ New Project"** in the Railway dashboard
2. Select **"Deploy from GitHub repo"**
3. Find and select the **temp** repository (githuobgithuot-hlo/temp)
4. Click **"Deploy Now"**

### Step 3: Configure Environment Variables
The app requires the following environment variables. Set them in Railway:

1. In Railway dashboard, go to your project
2. Click on **"Variables"** tab
3. Add the following variables:

```
CLOUDBET_USERNAME=<your_cloudbet_username>
CLOUDBET_PASSWORD=<your_cloudbet_password>
CLOUDBET_API_KEY=<your_cloudbet_api_key>
POLYMARKET_API_KEY=<your_polymarket_api_key>
TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
TELEGRAM_CHAT_ID=<your_telegram_chat_id>
PROFIT_THRESHOLD=2.0
LOG_LEVEL=INFO
TELEGRAM_ENABLED=true
DATABASE_URL=postgresql://user:password@host:port/dbname  # Optional if using PostgreSQL
```

### Step 4: Configure Build Settings (Already Done!)
The project already has Railway configuration:
- **railway.json**: Build configuration
- **nixpacks.toml**: Python environment setup
- **Procfile**: Process definitions for web and worker dynos

### Step 5: Deploy
1. Railway should auto-deploy when you push to the main branch
2. Monitor the deployment in the **Deployments** tab
3. Check logs in the **Logs** tab

### Step 6: Verify Deployment
- The web service should be available at: `https://<your-railway-domain>.railway.app`
- Check the health endpoint: `https://<your-railway-domain>.railway.app/health`
- Monitor logs for any errors

## Project Structure
```
cloudbet/
├── arbitrage-bot/
│   ├── src/
│   │   ├── main.py              # Main worker process
│   │   ├── dashboard/           # Web dashboard (Uvicorn)
│   │   ├── fetchers/            # API data fetchers
│   │   │   ├── cloudbet_fetcher.py
│   │   │   └── polymarket_fetcher.py
│   │   ├── sports_matcher.py    # Event matching
│   │   ├── sports_arbitrage_engine.py  # Arbitrage detection
│   │   ├── telegram_notifier.py # Telegram notifications
│   │   └── config_loader.py     # Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── Procfile                 # Process types for Railway
│   ├── railway.json             # Railway config
│   └── nixpacks.toml            # Build configuration
```

## Key Features
- **Real-time Arbitrage Detection**: Monitors Cloudbet and Polymarket
- **Sports Event Matching**: Automatically matches events across platforms
- **Telegram Notifications**: Sends alerts for profitable opportunities
- **Web Dashboard**: Monitor system status and opportunities
- **Automated Betting**: (When configured)

## Troubleshooting

### Deployment Issues
1. **Build fails**: Check `nixpacks.toml` and ensure Python 3.11 is specified
2. **Missing dependencies**: Verify all packages are in `requirements.txt`
3. **Port issues**: Railway automatically assigns PORT env variable

### Runtime Issues
1. **API Connection errors**: Check environment variables are set correctly
2. **Telegram not sending**: Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
3. **Database errors**: Check DATABASE_URL format if using PostgreSQL

### Checking Logs
```bash
# View deployment logs in Railway dashboard
# Or use Railway CLI if installed
railway logs
```

## Manual Deployment with Railway CLI

### Install Railway CLI
```bash
npm install -g @railway/cli
```

### Login to Railway
```bash
railway login
```

### Deploy
```bash
cd cloudbet/arbitrage-bot
railway deploy
```

## Continuous Deployment
The project is set up for continuous deployment:
- Push to `main` branch on GitHub
- Railway automatically detects and deploys changes
- Check deployment status in Railway dashboard

## Support
For issues or questions:
1. Check [Railway Documentation](https://docs.railway.app)
2. Review project README files
3. Check application logs in Railway dashboard

---

**Last Updated**: January 12, 2026
