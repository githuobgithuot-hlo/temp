# Railway Deployment Guide

## 🚀 Railway pe Deploy Kaise Karein

### Step 1: Railway Account Setup
1. Railway.app pe account banayein
2. GitHub repository ko connect karein

### Step 2: New Project Create Karein
1. Railway dashboard mein "New Project" click karein
2. "Deploy from GitHub repo" select karein
3. Apni repository select karein

### Step 3: Environment Variables Set Karein
Railway dashboard mein "Variables" tab mein yeh variables add karein:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
CLOUDBET_API_KEY=your_cloudbet_api_key
DATABASE_PATH=data/arbitrage_events.db
PORT=8000
```

### Step 4: Services Configuration
Railway automatically **Procfile** ko detect karega aur **2 services** create karega:

1. **Web Service** (Dashboard)
   - Port: Railway automatically assign karega
   - Command: `web: python -m uvicorn src.dashboard:app --host 0.0.0.0 --port $PORT`

2. **Worker Service** (Bot)
   - Command: `worker: python src/main.py`

### Step 5: Deploy
1. Railway automatically deploy start karega
2. Build logs check karein
3. Deploy hone ke baad web service ka URL milega

### Step 6: Access Dashboard
- Railway dashboard mein web service ka URL milega
- Example: `https://your-app-name.up.railway.app`
- Dashboard available hoga: `/dashboard`, `/opportunities`, `/logs`

## 📋 Important Notes

### Database Persistence
- Railway mein database file **ephemeral** hoti hai (temporary)
- Agar permanent storage chahiye, Railway PostgreSQL addon use karein
- Ya phir external database service use karein

### Logs
- Railway dashboard mein logs dekh sakte hain
- Ya phir `/logs` endpoint pe dashboard se

### Monitoring
- Dashboard se real-time monitoring
- Statistics aur opportunities dekh sakte hain
- Bot status check kar sakte hain

## 🔧 Troubleshooting

### Bot Start Nahi Ho Raha
1. Environment variables check karein
2. Logs dekhin Railway dashboard mein
3. `TELEGRAM_BOT_TOKEN` aur `TELEGRAM_CHAT_ID` verify karein

### Dashboard Nahi Khul Raha
1. Web service ka URL check karein
2. Port variable set hai ya nahi check karein
3. Build logs mein errors dekhin

### Database Errors
1. `DATABASE_PATH` variable set karein
2. `data/` directory writable hai ya nahi check karein

## 🎯 Features
- ✅ Bot aur Dashboard dono ek saath chalenge
- ✅ Automatic restart on failure
- ✅ Real-time monitoring
- ✅ Easy deployment from GitHub


