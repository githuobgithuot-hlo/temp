# Quick Start - Railway Deployment Checklist

## ✅ Already Complete
- [x] Project pushed to GitHub: https://github.com/githuobgithuot-hlo/temp.git
- [x] Main branch configured
- [x] railway.json configured
- [x] Procfile configured
- [x] nixpacks.toml configured
- [x] Python 3.11 environment ready
- [x] All dependencies in requirements.txt

## 📋 Next Steps (Quick Reference)

### 1. Go to Railway.app
```
https://railway.app
```

### 2. Create Project from GitHub
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose: githuobgithuot-hlo/temp
- Click "Deploy Now"

### 3. Set Environment Variables (Critical!)
In Railway dashboard → Variables tab:

| Variable | Value |
|----------|-------|
| `CLOUDBET_USERNAME` | Your Cloudbet username |
| `CLOUDBET_PASSWORD` | Your Cloudbet password |
| `CLOUDBET_API_KEY` | Your Cloudbet API key |
| `POLYMARKET_API_KEY` | Your Polymarket API key |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `PROFIT_THRESHOLD` | 2.0 (or your preferred threshold) |
| `LOG_LEVEL` | INFO |
| `TELEGRAM_ENABLED` | true |

### 4. Deploy & Monitor
- Railway will auto-deploy when code is pushed
- Watch logs in: Deployments → Logs tab
- Test at: `https://<your-railway-domain>.railway.app/health`

## 🔗 Useful Links
- **Repository**: https://github.com/githuobgithuot-hlo/temp.git
- **Railway Dashboard**: https://railway.app
- **Railway Docs**: https://docs.railway.app
- **Project Docs**: See DEPLOYMENT_GUIDE.md

## 🚀 What Deploys
- **Web Service**: Runs FastAPI dashboard on port 8000
- **Worker**: Runs arbitrage detection bot continuously
- **Health Check**: `/health` endpoint

## 💡 Tips
1. Start with PROFIT_THRESHOLD=5.0 to see if system works
2. Keep Telegram ENABLED=true for notifications
3. Logs show real-time bot activity - watch them!
4. Use Railway CLI for advanced deployments:
   ```bash
   npm install -g @railway/cli
   railway login
   railway deploy
   ```

## 📞 Support
- Check Railway docs: https://docs.railway.app/reference
- Review logs in Railway dashboard
- See DEPLOYMENT_GUIDE.md for detailed instructions
