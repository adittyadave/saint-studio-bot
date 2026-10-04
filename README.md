# Saint Studio Discord Bot

A powerful Discord music bot for Saint Studio gaming community with YouTube + Spotify support, queue management, and playlist features.

## Features

✅ **Music Playback**
- Play from YouTube and Spotify
- Queue management (skip, pause, resume)
- Playlist save/load functionality

✅ **Reactions**
- Auto-react to messages
- Manual emoji reactions
- Custom keywords

✅ **Utility**
- Custom message sending
- Bot information command
- Full help system

## Quick Start

1. **Get your Discord bot token:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new app → Add Bot
   - Copy your token

2. **Clone this repo to Replit:**
   - Go to [Replit.com](https://replit.com)
   - Click "Import" → paste this repo URL
   - Replit creates the project automatically

3. **Add environment variables:**
   - In Replit, go to "Secrets" (🔒)
   - Add `DISCORD_TOKEN` = your token
   - Optional: Add `SPOTIFY_ID` and `SPOTIFY_SECRET`

4. **Run the bot:**
   - Click "Run"
   - Bot goes live on your Discord server

## Commands

### Music
- `!play <song>` - Play from YouTube/Spotify
- `!skip` - Next song
- `!pause` / `!resume` - Control playback
- `!queue` - Show queued songs
- `!clear` - Clear queue

### Playlists
- `!save_playlist <name>` - Save current queue
- `!load_playlist <name>` - Load saved playlist
- `!playlists` - List all playlists

### Utility
- `!say <message>` - Bot says something
- `!react <emoji>` - React to message
- `!info` - Bot info
- `!help` - All commands

## Keep 24/7

**Option A: Replit Autouptime (Free)**
- In Replit → Tools → Autouptime → Toggle ON

**Option B: UptimeRobot (Free)**
- Sign up at [UptimeRobot.com](https://uptimerobot.com)
- Create HTTP monitor with your Replit URL
- Pings every 5 min to keep bot alive

## Support

Need help? Check DEPLOYMENT_GUIDE.md for troubleshooting.

---

Made for Saint Studio Graphics Mods 🎮
