import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
from collections import defaultdict

# Load environment variables
load_dotenv()

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Music queue and playlist storage
music_queue = defaultdict(list)
playlists = {}
current_playing = {}
is_paused = {}

# Spotify setup (optional - leave blank if not using)
SPOTIFY_ID = os.getenv("SPOTIFY_ID", "")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET", "")

spotify_client = None
if SPOTIFY_ID and SPOTIFY_SECRET:
    try:
        spotify_client = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_ID,
                client_secret=SPOTIFY_SECRET
            )
        )
    except:
        print("Spotify setup failed - will use YouTube only")

# YT-DLP setup for YouTube
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'socket_timeout': 30,
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def get_voice_client(guild_id):
    """Get or create voice client for guild"""
    guild = bot.get_guild(guild_id)
    if guild:
        for vc in bot.voice_clients:
            if vc.guild.id == guild_id:
                return vc
    return None


def search_youtube(query):
    """Search YouTube and return URL"""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                return info['entries'][0]['url']
            return info['url']
        except:
            return None


def search_spotify(query):
    """Search Spotify and return YouTube fallback"""
    if not spotify_client:
        return None
    try:
        results = spotify_client.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            artist = track['artists'][0]['name']
            youtube_query = f"{track_name} {artist} official audio"
            return search_youtube(youtube_query)
    except:
        pass
    return None


def extract_youtube_url(url_or_query):
    """Extract YouTube URL or search for it"""
    if 'youtube.com' in url_or_query or 'youtu.be' in url_or_query:
        return url_or_query
    return search_youtube(url_or_query)


# ============================================================================
# BOT EVENTS
# ============================================================================

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    print(f"🎮 Ready to serve Saint Studio!")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="!help for commands"
    ))


@bot.event
async def on_message(message):
    """Handle messages - auto-react to certain content"""
    if message.author == bot.user:
        return
    
    # Auto-react to messages containing certain keywords
    if any(word in message.content.lower() for word in ["vibes", "fire", "clean", "sick"]):
        try:
            await message.add_reaction("🔥")
        except:
            pass
    
    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    """Handle reaction events"""
    if user == bot.user:
        return
    
    # Log reactions (customize as needed)
    channel = reaction.message.channel
    await channel.send(f"{user.mention} reacted with {reaction.emoji} to a message!")


# ============================================================================
# MUSIC COMMANDS
# ============================================================================

@bot.command(name="join", help="Join your voice channel")
async def join(ctx):
    """Join user's voice channel"""
    if not ctx.author.voice:
        await ctx.send("❌ You're not in a voice channel!")
        return
    
    channel = ctx.author.voice.channel
    voice = await channel.connect()
    await ctx.send(f"✅ Joined {channel.name}")


@bot.command(name="leave", help="Leave voice channel")
async def leave(ctx):
    """Leave voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel")
    else:
        await ctx.send("❌ Not in a voice channel")


@bot.command(name="play", help="Play a song: !play <song name or URL>")
async def play(ctx, *, query):
    """Play a song from YouTube or Spotify"""
    if not ctx.author.voice:
        await ctx.send("❌ Join a voice channel first!")
        return
    
    # Join if not already connected
    if not ctx.voice_client:
        await ctx.invoke(join)
    
    async with ctx.typing():
        await ctx.send(f"🔍 Searching for: **{query}**...")
        
        # Try Spotify first if configured
        url = None
        if spotify_client and not ("youtube.com" in query or "youtu.be" in query):
            url = search_spotify(query)
        
        # Fallback to YouTube
        if not url:
            url = extract_youtube_url(query)
        
        if not url:
            await ctx.send("❌ Could not find that song")
            return
        
        # Add to queue
        guild_id = ctx.guild.id
        music_queue[guild_id].append({
            'url': url,
            'title': query,
            'requester': ctx.author.mention
        })
        
        # Play if nothing is playing
        if not ctx.voice_client.is_playing():
            await play_next(ctx)
        else:
            await ctx.send(f"✅ Added to queue: **{query}**")


async def play_next(ctx):
    """Play next song in queue"""
    guild_id = ctx.guild.id
    voice_client = ctx.voice_client
    
    if not music_queue[guild_id]:
        await ctx.send("✅ Queue finished!")
        return
    
    song = music_queue[guild_id].pop(0)
    current_playing[guild_id] = song
    
    try:
        audio = discord.FFmpegPCMAudio(
            song['url'],
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )
        
        def after_playing(error):
            if error:
                print(f"Player error: {error}")
            # Play next song
            asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        
        voice_client.play(audio, after=after_playing)
        await ctx.send(f"▶️ Now playing: **{song['title']}** (requested by {song['requester']})")
    except Exception as e:
        await ctx.send(f"❌ Could not play song: {str(e)}")
        await play_next(ctx)


@bot.command(name="queue", help="Show music queue")
async def queue(ctx):
    """Display current queue"""
    guild_id = ctx.guild.id
    
    if not music_queue[guild_id]:
        await ctx.send("📭 Queue is empty")
        return
    
    embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.purple())
    
    for i, song in enumerate(music_queue[guild_id][:10], 1):
        embed.add_field(
            name=f"{i}. {song['title']}",
            value=f"Requested by {song['requester']}",
            inline=False
        )
    
    if len(music_queue[guild_id]) > 10:
        embed.add_field(name="...", value=f"+{len(music_queue[guild_id]) - 10} more songs")
    
    await ctx.send(embed=embed)


@bot.command(name="skip", help="Skip current song")
async def skip(ctx):
    """Skip current song"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped!")
    else:
        await ctx.send("❌ Nothing is playing")


@bot.command(name="pause", help="Pause playback")
async def pause(ctx):
    """Pause playback"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        is_paused[ctx.guild.id] = True
        await ctx.send("⏸️ Paused")
    else:
        await ctx.send("❌ Nothing is playing")


@bot.command(name="resume", help="Resume playback")
async def resume(ctx):
    """Resume playback"""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        is_paused[ctx.guild.id] = False
        await ctx.send("▶️ Resumed")
    else:
        await ctx.send("❌ Nothing to resume")


@bot.command(name="clear", help="Clear the queue")
async def clear(ctx):
    """Clear music queue"""
    guild_id = ctx.guild.id
    music_queue[guild_id].clear()
    await ctx.send("🗑️ Queue cleared")


# ============================================================================
# PLAYLIST COMMANDS
# ============================================================================

@bot.command(name="save_playlist", help="Save current queue: !save_playlist <name>")
async def save_playlist(ctx, *, name):
    """Save current queue as playlist"""
    guild_id = ctx.guild.id
    
    if not music_queue[guild_id]:
        await ctx.send("❌ Queue is empty!")
        return
    
    playlists[f"{ctx.guild.id}_{name}"] = music_queue[guild_id].copy()
    await ctx.send(f"✅ Playlist **{name}** saved ({len(music_queue[guild_id])} songs)")


@bot.command(name="load_playlist", help="Load a playlist: !load_playlist <name>")
async def load_playlist(ctx, *, name):
    """Load a saved playlist"""
    guild_id = ctx.guild.id
    key = f"{guild_id}_{name}"
    
    if key not in playlists:
        await ctx.send("❌ Playlist not found")
        return
    
    music_queue[guild_id] = playlists[key].copy()
    await ctx.send(f"✅ Loaded playlist **{name}** ({len(playlists[key])} songs)")


@bot.command(name="playlists", help="List all playlists")
async def list_playlists(ctx):
    """List all saved playlists"""
    guild_id = ctx.guild.id
    user_playlists = [key.split("_", 1)[1] for key in playlists.keys() if key.startswith(f"{guild_id}_")]
    
    if not user_playlists:
        await ctx.send("📭 No playlists saved")
        return
    
    embed = discord.Embed(title="📋 Saved Playlists", color=discord.Color.purple())
    for name in user_playlists:
        count = len(playlists[f"{guild_id}_{name}"])
        embed.add_field(name=name, value=f"{count} songs", inline=False)
    
    await ctx.send(embed=embed)


# ============================================================================
# UTILITY COMMANDS
# ============================================================================

@bot.command(name="react", help="React to a message: !react <emoji>")
async def react_command(ctx, emoji):
    """Add reaction to last message"""
    try:
        message = await ctx.channel.history(limit=2).flatten()
        await message[-1].add_reaction(emoji)
        await ctx.send(f"✅ Reacted with {emoji}")
    except:
        await ctx.send("❌ Could not react")


@bot.command(name="say", help="Make bot say something: !say <message>")
async def say(ctx, *, message):
    """Bot sends a message"""
    await ctx.send(message)


@bot.command(name="info", help="Show bot info")
async def info(ctx):
    """Show bot information"""
    embed = discord.Embed(
        title="🤖 Saint Studio Bot",
        description="Your all-in-one music & moderation bot",
        color=discord.Color.purple()
    )
    embed.add_field(name="🎵 Music", value="Play from YouTube & Spotify", inline=False)
    embed.add_field(name="📋 Playlists", value="Save & load playlists", inline=False)
    embed.add_field(name="⚙️ Commands", value="!help to see all commands", inline=False)
    embed.set_footer(text="Made for Saint Studio Graphics Mods")
    
    await ctx.send(embed=embed)


# ============================================================================
# ERROR HANDLER
# ============================================================================

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument! Use `!help {ctx.command.name}`")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help`")
    else:
        await ctx.send(f"❌ Error: {str(error)}")


# ============================================================================
# RUN BOT
# ============================================================================

def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN not found in .env file!")
        return
    
    bot.run(token)


if __name__ == "__main__":
    run_bot()
