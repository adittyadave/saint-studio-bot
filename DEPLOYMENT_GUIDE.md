# Saint Studio Discord Bot — Deployment Guide

## Complete Setup in 5 Minutes (Free Hosting)

Your bot is ready to go! Follow these steps to get it running on **Replit** (free, no credit card, 24/7 uptime).

---

## STEP 1: Create Discord Bot & Get Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → name it `Saint Studio Bot`
3. Go to **"Bot"** tab → click **"Add Bot"**
4. Under **TOKEN**, click **"Copy"** — save this somewhere safe (you'll need it in a minute)
5. Under **Privileged Gateway Intents**, turn ON:
   - ✅ Message Content Intent
   - ✅ Voice States
   - ✅ Server Members Intent

6. Go to **OAuth2 → URL Generator**
7. Select scopes: `bot`
8. Select permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Connect (voice)
   - ✅ Speak (voice)
   - ✅ Move Members

9. Copy the generated URL → paste in browser → select your Saint Studio server → Authorize

**You now have a bot in your Discord server!**

---

## STEP 2: Deploy on Replit (Free)

1. Go to [Replit.com](https://replit.com) and sign up (free)
2. Click **"Create Repl"** → select **"Python"**
3. Copy all files from this kit into Replit:
   - `saint-studio-bot.py` (main bot file)
   - `requirements.txt` (dependencies)

4. Create a new file called `.env` in Replit:
   ```
   DISCORD_TOKEN=your_token_here
   SPOTIFY_ID=
   SPOTIFY_SECRET=
   ```
   - Paste your Discord bot token after `DISCORD_TOKEN=`
   - Leave Spotify blank for now (optional)

5. Click **"Run"** — the bot will start!
   - Check the console: should see ✅ Bot logged in as Saint Studio Bot
   - Check Discord: bot is now ONLINE in your server

---

## STEP 3 (OPTIONAL): Add Spotify Support

If you want Spotify playback:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app → you'll get:
   - **Client ID**
   - **Client Secret**

3. Update your `.env` file:
   ```
   DISCORD_TOKEN=your_discord_token
   SPOTIFY_ID=your_spotify_client_id
   SPOTIFY_SECRET=your_spotify_client_secret
   ```

4. Click **"Run"** again — Spotify is now enabled!

---

## STEP 4: Keep Bot Running 24/7

Replit free tier runs while you're using it. To keep it running forever:

**Option A: Replit Autouptime (Free)**
- In Replit, go to **Tools** → **Autouptime** → toggle ON
- Bot stays online indefinitely (free)

**Option B: UptimeRobot (Free)**
1. Go to [UptimeRobot.com](https://uptimerobot.com)
2. Create monitor → select "HTTP(S)"
3. Paste your Replit URL (shown when you run the bot)
4. Save — UptimeRobot will ping your bot every 5 minutes to keep it alive

---

## COMMAND REFERENCE

### Music Commands
| Command | What it does |
|---|---|
| `!play <song>` | Play a song from YouTube or Spotify |
| `!join` | Join your voice channel |
| `!leave` | Leave voice channel |
| `!skip` | Skip current song |
| `!pause` | Pause playback |
| `!resume` | Resume playback |
| `!queue` | Show queued songs |
| `!clear` | Clear entire queue |

### Playlist Commands
| Command | What it does |
|---|---|
| `!save_playlist <name>` | Save current queue as playlist |
| `!load_playlist <name>` | Load a saved playlist |
| `!playlists` | List all saved playlists |

### Utility Commands
| Command | What it does |
|---|---|
| `!say <message>` | Make bot say something |
| `!react <emoji>` | React with emoji (auto-detects) |
| `!info` | Show bot info |
| `!help` | Show all commands |

---

## EXAMPLE USAGE

**Play a song:**
```
!play never gonna give you up
```
Bot searches YouTube → plays it → queues are shown

**Create a playlist:**
```
!play song 1
!play song 2
!play song 3
!save_playlist gaming-vibes
```

**Load later:**
```
!load_playlist gaming-vibes
!queue
```

---

## TROUBLESHOOTING

**Bot is offline?**
- Check your Replit console for errors
- Make sure `.env` has correct Discord token
- Restart Replit (click "Run" again)

**Music not playing?**
- Make sure bot is in a voice channel (`!join`)
- Check Discord permissions (bot needs Connect + Speak)
- Try a different song (might be blocked region)

**Spotify not working?**
- Bot falls back to YouTube automatically
- Only needed if you want to search by Spotify track name

**Need more commands?**
- Message me, I can add them (ban users, mod tools, etc.)

---

## FILE STRUCTURE

```
Replit/
├── saint-studio-bot.py      (main bot code)
├── requirements.txt          (Python dependencies)
└── .env                      (your secrets — keep safe!)
```

That's it! Your bot is live. 🎉

---

## NEXT STEPS

1. ✅ Bot is running
2. Test commands in your Discord server
3. Customize keywords for auto-reactions (edit line ~101)
4. Add more features as needed

Need help? Let me know!
