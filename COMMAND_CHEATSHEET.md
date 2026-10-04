# Saint Studio Bot — Command Cheatsheet

## ⚡ Quick Commands

**Prefix: `!`**

### 🎵 Music (Core)
- `!play <name/URL>` — Search & play from YouTube/Spotify
- `!skip` — Next song
- `!pause` → `!resume` — Pause/Resume
- `!queue` — Show 10 next songs
- `!clear` — Delete all queued songs

### 📋 Playlists
- `!save_playlist <name>` — Save current queue
- `!load_playlist <name>` — Load saved playlist
- `!playlists` — List all your playlists

### 🎙️ Voice
- `!join` — Bot joins your voice channel
- `!leave` — Bot leaves

### 🎭 Utility
- `!say <text>` — Bot repeats your message
- `!react <emoji>` — React to last message
- `!info` — Bot information
- `!help` — Full command list

---

## 🎯 Usage Examples

### Play Music
```
!play lofi hip hop radio
!play https://www.youtube.com/watch?v=...
!play dua lipa  (if Spotify enabled)
```

### Manage Queue
```
!queue                    (see next songs)
!skip                     (next song)
!pause                    (pause)
!resume                   (resume)
!clear                    (clear all)
```

### Playlists
```
!play song 1
!play song 2
!play song 3
!save_playlist studying   (save as "studying")

(later...)
!load_playlist studying   (load it back)
!queue                    (verify)
```

### Auto-Reactions
Bot automatically reacts 🔥 to messages with:
- "vibes"
- "fire"
- "clean"
- "sick"

---

## ❌ Common Issues

| Issue | Fix |
|---|---|
| "Not in voice channel" | `!join` first |
| Music won't play | Check bot permissions (Speak, Connect) |
| Song not found | Try different name/YouTube link |
| Bot offline | Restart Replit |
| Spotify not working | Bot uses YouTube fallback automatically |

---

## 🔧 Customize (Advanced)

Edit `saint-studio-bot.py`:

**Auto-react keywords** (line ~101):
```python
if any(word in message.content.lower() for word in ["vibes", "fire", "clean", "sick"]):
```

**Bot prefix** (line ~17):
```python
bot = commands.Bot(command_prefix="!")  # Change ! to $, >, etc.
```

**Default playing status** (line ~95):
```python
name="!help for commands"  # Change to whatever
```

---

## 📞 Support

All commands work with `!help <command>` for detailed info:
```
!help play
!help playlists
!help
```

That's everything! 🎉
