# 🤖 Arbitrage Bot on Railway - Complete Guide

## 📋 Project Overview

This is an **Arbitrage Detection Bot** that:
- ✅ Fetches real-time data from **Cloudbet** and **Polymarket**
- ✅ Detects **sports arbitrage opportunities**
- ✅ Calculates **profit margins**
- ✅ Sends **Telegram alerts** for profitable trades
- ✅ Provides **Web Dashboard** for monitoring

---

## 🏗️ Architecture on Railway

### **Web Service (HTTP)**
```
Port: 8000 (assigned by Railway via $PORT)
Purpose: FastAPI Dashboard
Entry Point: asgi.py → DashboardApp
Endpoint: https://your-domain.railway.app
```

**What it does:**
- Shows detected arbitrage opportunities
- Displays system status and logs
- Provides REST API for data

### **Worker Service (Background)**
```
Process: Long-running Python script
Purpose: Continuous arbitrage detection
Entry Point: src/main.py → ArbitrageBot
```

**What it does:**
- Continuously monitors Cloudbet API
- Continuously monitors Polymarket API
- Matches events between platforms
- Calculates arbitrage opportunities
- Sends Telegram alerts

---

## 🔄 How It Works

### **Workflow Diagram**

```
┌─────────────────────────────────────────────────────────┐
│              Railway Deployment                         │
├────────────────────┬────────────────────────────────────┤
│                    │                                    │
│   WEB SERVICE      │        WORKER SERVICE              │
│   (Port 8000)      │     (Continuous Loop)              │
│                    │                                    │
│  FastAPI App       │    1. Fetch Cloudbet API          │
│  • Dashboard       │    2. Fetch Polymarket API        │
│  • REST API        │    3. Normalize market data       │
│  • Status page     │    4. Match sports events         │
│                    │    5. Calculate arbitrage         │
│                    │    6. Calculate profit            │
│                    │    7. Send Telegram alert         │
│                    │    8. Store in database           │
│                    │    9. Repeat every X seconds      │
└────────────────────┴────────────────────────────────────┘
```

### **Data Flow**

```
Cloudbet API ──┐
               ├─→ CloudbetFetcher ──┐
               │                     │
Polymarket API─┤                     ├─→ MarketNormalizer ──┐
               │                     │                      │
               └→ PolymarketFetcher ─┤                      ├─→ SportsArbitrageEngine
                                     │                      │
                                     └──→ SportEventMatcher─┤
                                                            │
                                                            ├─→ Calculate Profit
                                                            │
                                                            ├─→ Telegram Alert
                                                            │
                                                            └─→ Database Storage
```

---

## 📊 Key Components

### **1. Data Fetchers**
```python
CloudbetFetcher()      # Fetches sports events & markets from Cloudbet
PolymarketFetcher()    # Fetches prediction markets from Polymarket
```

### **2. Market Matching**
```python
SportEventMatcher()       # Matches same sports events across platforms
MarketMatcher()          # Matches outcome markets
```

### **3. Arbitrage Detection**
```python
SportsArbitrageEngine()   # Detects profit opportunities
ProbabilityEngine()       # Calculates implied probabilities
```

### **4. Alerts**
```python
TelegramNotifier()        # Sends async Telegram messages
ArbitrageDatabase()       # Stores opportunities for dashboard
```

---

## ⚙️ Environment Variables Required

### **Cloudbet Credentials**
```env
CLOUDBET_API_KEY=<your_jwt_token>
```

### **Polymarket API**
```env
POLYMARKET_API_KEY=<optional>
```

### **Telegram Bot Setup**
```env
TELEGRAM_BOT_TOKEN=<bot_token_from_botfather>
TELEGRAM_CHAT_ID=<your_chat_id>
```

### **Bot Configuration**
```env
PROFIT_THRESHOLD=2.0              # Minimum profit % to alert (e.g., 2.0 = 2%)
FETCH_INTERVAL=30                 # Seconds between API checks
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
TELEGRAM_ENABLED=true             # Enable/disable alerts
```

---

## 🔐 Getting Credentials

### **Cloudbet API Key**
1. Go to https://cloudbet.com
2. Create account / Login
3. Go to API settings
4. Generate trading API key
5. Copy the JWT token

### **Telegram Bot Token**
1. Chat with @BotFather on Telegram
2. Send: `/newbot`
3. Follow instructions
4. Copy the token (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### **Telegram Chat ID**
1. Send any message to your bot
2. Go to: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"id"` in the response
4. That's your Chat ID

---

## 📱 What You'll Receive on Telegram

### **Arbitrage Alert Format**
```
🎯 ARBITRAGE OPPORTUNITY DETECTED

Event: Manchester United vs Liverpool (Soccer - Premier League)
Date: 2026-01-15 20:00 UTC

Cloudbet Odds:
  • Manchester United: 2.10
  • Liverpool: 1.85

Polymarket Price:
  • Manchester United: 0.45 (2.22 implied)
  • Liverpool: 0.55 (1.82 implied)

💰 PROFIT CALCULATION:
  • Stake: $1000
  • Outcome A: +$120
  • Outcome B: +$150
  
✅ Guaranteed Profit: $135 (13.5% ROI)

⚡ Status: LIVE - Act Now!
🔗 Dashboard: https://your-domain.railway.app
```

---

## 🚀 Deployment Checklist

### **Before Deployment**

- [ ] Have Cloudbet API key ready
- [ ] Have Polymarket API key (if using)
- [ ] Have Telegram bot token
- [ ] Have Telegram chat ID
- [ ] Repository pushed to GitHub
- [ ] Railway project created

### **During Deployment**

- [ ] Set environment variables in Railway
- [ ] Trigger build
- [ ] Monitor build logs

### **After Deployment**

- [ ] Check web service is running
- [ ] Check worker service is running
- [ ] Visit dashboard: `https://your-domain.railway.app`
- [ ] Test Telegram notification (manually trigger opportunity)
- [ ] Monitor logs for errors

---

## 📊 Expected Bot Behavior

### **Startup (First 30 seconds)**
```
✓ Loading configuration
✓ Initializing database
✓ Connecting to Cloudbet API
✓ Connecting to Polymarket API
✓ Starting arbitrage detection loop
✓ Ready for monitoring
```

### **During Operation (Continuous)**
```
Every 30 seconds:
  1. Fetch current Cloudbet markets
  2. Fetch current Polymarket contracts
  3. Normalize odds/prices
  4. Match events across platforms
  5. Calculate arbitrage opportunities
  6. If profit > PROFIT_THRESHOLD:
     → Send Telegram alert
     → Store in database
     → Log to dashboard
  7. Sleep 30 seconds
  8. Repeat
```

### **On Arbitrage Detected**
```
✓ Calculate all possible combinations
✓ Verify profitable outcome exists
✓ Format alert message
✓ Send to Telegram (async, non-blocking)
✓ Store in database
✓ Update dashboard
✓ Continue monitoring
```

---

## 📈 Performance Metrics

### **Resources Used**
```
CPU:     Minimal (< 10% average)
Memory:  ~100-150 MB
Network: API calls every 30 seconds
Database: SQLite (lightweight)
```

### **Expected Results**
```
Opportunities Found: 5-20 per day (varies by market activity)
Telegram Alerts: Immediate upon detection
Dashboard Updates: Real-time
False Positives: Minimal with proper threshold
```

---

## 🐛 Troubleshooting

### **Bot Not Starting**
```
❌ Worker service showing "Failed"
✓ Check: src/main.py has correct imports
✓ Check: All required packages in requirements.txt
✓ Check: Environment variables are set
✓ Check: Cloudbet API key is valid
```

### **No Opportunities Found**
```
❌ Dashboard shows no arbitrage opportunities
✓ Check: Bot is running (worker service)
✓ Check: API connections are working
✓ Check: Market data is being fetched
✓ Increase PROFIT_THRESHOLD to lower (e.g., 1.0)
✓ Wait longer (markets need time to populate)
```

### **Telegram Alerts Not Working**
```
❌ No Telegram messages received
✓ Check: TELEGRAM_BOT_TOKEN format (should have colon)
✓ Check: TELEGRAM_CHAT_ID is numeric
✓ Check: Bot is member of chat/group
✓ Check: Telegram enabled: TELEGRAM_ENABLED=true
✓ Test manually in Telegram
```

### **High CPU Usage**
```
❌ Railway showing high CPU utilization
✓ Increase FETCH_INTERVAL (e.g., 60 instead of 30)
✓ Reduce number of markets being monitored
✓ Check for infinite loops in logs
✓ Optimize market matching algorithm
```

---

## 📊 Monitoring & Logs

### **What to Watch**

**In Railway Logs:**
```
✓ "[INFO] Starting arbitrage detection bot"
✓ "[INFO] Fetching Cloudbet markets"
✓ "[INFO] Fetching Polymarket markets"
✓ "[INFO] Opportunity detected: Manchester United vs Liverpool"
✓ "[INFO] Telegram alert sent successfully"
```

**What Indicates Problems:**
```
✗ "[ERROR] Failed to connect to Cloudbet API"
✗ "[ERROR] Telegram bot token invalid"
✗ "[ERROR] Database locked"
✗ Connection timeouts
```

### **Dashboard (Web Interface)**

Access at: `https://your-domain.railway.app`

Shows:
- ✅ Last detected opportunities
- ✅ System status (running/stopped)
- ✅ API connection status
- ✅ Recent alerts sent
- ✅ Statistics & metrics

---

## 🔄 Deployment Steps Summary

### **Step 1: Set Environment Variables**
In Railway dashboard:
```
CLOUDBET_API_KEY=<your_key>
POLYMARKET_API_KEY=<optional>
TELEGRAM_BOT_TOKEN=<bot_token>
TELEGRAM_CHAT_ID=<your_id>
PROFIT_THRESHOLD=2.0
FETCH_INTERVAL=30
LOG_LEVEL=INFO
TELEGRAM_ENABLED=true
```

### **Step 2: Deploy**
Railway auto-detects GitHub changes and rebuilds

### **Step 3: Monitor**
1. Watch build logs
2. Verify both services start
3. Check dashboard loads
4. Receive first Telegram alert

### **Step 4: Optimize**
1. Adjust PROFIT_THRESHOLD based on opportunities
2. Adjust FETCH_INTERVAL based on your needs
3. Monitor performance metrics

---

## ✨ Expected Outcome

After successful deployment:

```
✅ Web service running: https://your-domain.railway.app
✅ Worker service running: Continuous arbitrage detection
✅ Telegram alerts: Received when opportunities detected
✅ Dashboard: Real-time view of opportunities
✅ Database: Recording all arbitrage events
✅ Logs: Available in Railway for debugging
```

---

## 📞 Support Resources

- **Cloudbet API Docs**: https://cloudbet.com/api/docs
- **Polymarket API**: https://docs.polymarket.com
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Railway Docs**: https://docs.railway.app

---

## 🎯 Next Actions

1. **Verify Credentials**
   - [ ] Cloudbet API key ready
   - [ ] Telegram bot token ready
   - [ ] Chat ID ready

2. **Deploy to Railway**
   - [ ] Go to https://railway.app
   - [ ] Set environment variables
   - [ ] Trigger build

3. **Test After Deployment**
   - [ ] Check web service running
   - [ ] Check worker service running
   - [ ] Visit dashboard
   - [ ] Wait for first Telegram alert

4. **Monitor & Optimize**
   - [ ] Watch logs
   - [ ] Adjust thresholds if needed
   - [ ] Monitor resources
   - [ ] Receive alerts 24/7

---

**Status**: ✅ **READY FOR DEPLOYMENT**
**Bot Function**: Continuous arbitrage detection + Telegram alerts
**Expected Uptime**: 24/7 on Railway
**Last Updated**: January 12, 2026
