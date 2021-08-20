#MIT License

#Copyright (c) 2021 SUBIN

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, emoji
from utils import mp, playlist
from config import Config


HELP = """

<b>Add the bot and User account in your Group with admin rights.

Start a VoiceChat

Use /play <song name> or use /play as a reply to an audio file or youtube link.

You can also use /splay <song name> to play a song from JioSaavn or /cplay <channel username or channel id> to play music from a telegram channel.</b>

**Common Commands**:

**/play**  Reply to an audio file or YouTube link to play it or use /play <song name>.
**/splay** Play music from Jio Saavn, Use /splay <song name>
**/player**  Show current playing song.
**/help** Show help for commands
**/playlist** Shows the playlist.

**Admin Commands**:
**/skip** [n] ...  Skip current or n where n >= 2
**/join**  Join voice chat.
**/leave**  Leave current voice chat
**/shuffle** Shuffle Playlist.
**/cplay** Play music from a channel's music files.
**/vc**  Check which VC is joined.
**/stop**  Stop playing.
**/radio** Start Radio.
**/stopradio** Stops Radio Stream.
**/clearplaylist** Clear the playlist.
**/replay**  Play from the beginning.
**/clean** Remove unused RAW PCM files.
**/pause** Pause playing.
**/resume** Resume playing.
**/volume** Change volume(0-200).
**/mute**  Mute in VC.
**/unmute**  Unmute in VC.
**/restart** Update and restarts the Bot.
"""



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await mp.get_admins(Config.CHAT)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "😒 Played Joji.mp3",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty Playlist"
        else:
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "upload": 
        async def upload(client, message):
    if not playlist:
        k=await message.reply_text(f"{emoji.NO_ENTRY} No songs are playing")
        await mp.delete(k)
        await mp.delete(message)
        return
    url=playlist[0][2]
    if playlist[0][3] == "telegram":
        await client.send_audio(chat_id=message.chat.id, audio=url, caption="Uploaded Using [MusicPlayer](https://t.me/MusicForSSHstore_bot)")
    elif playlist[0][3] == "youtube":
        file=GET_FILE[url]
        thumb=GET_THUMB[url]
        response = requests.get(thumb, allow_redirects=True)
        open(f"{playlist[0][5]}.jpeg", 'wb').write(response.content)
        await message.reply_chat_action("upload_document")
        m=await message.reply_text(f"Starting Uploading {playlist[0][1]}...")
        await client.send_audio(chat_id=message.chat.id, audio=file, file_name=playlist[0][1], thumb=f"{playlist[0][5]}.jpeg", title=playlist[0][1], caption=f"<b>Song: [{playlist[0][1]}]({playlist[0][2]})\nUploaded Using [MusicPlayer](https://github.com/subinps/MusicPlayer)</b>")
        await m.delete()
    else:
        file=GET_FILE[url]
        thumb=GET_THUMB[url]
        response = requests.get(thumb, allow_redirects=True)
        open(f"{playlist[0][5]}.jpeg", 'wb').write(response.content)
        await message.reply_chat_action("upload_document")
        cmd=f"cp {file} {playlist[0][5]}.mp3"
        os.system(cmd)
        await asyncio.sleep(2)
        m=await message.reply_text(f"Starting Uploading {playlist[0][1]}...")
        await client.send_audio(chat_id=message.chat.id, audio=f"{playlist[0][5]}.mp3", file_name=f"{playlist[0][1]}", thumb=f"{playlist[0][5]}.jpeg", title=playlist[0][1], caption=f"<b>Song: [{playlist[0][1]}]({playlist[0][2]})\nUploaded Using [MusicPlayer](https://github.com/subinps/MusicPlayer)</b>")
        await m.delete()
        try:
            os.remove(f"{playlist[0][5]}.mp3")
        except:
            pass
        
           
    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused\n\n{pl},",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="resume"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    
    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed\n\n{pl}",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Skipped\n\n{pl}",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏯", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('👥 Friends Channel', url='https://t.me/UNLIMITEDworldTEAM'),
                InlineKeyboardButton('👤 VpnStock', url='https://t.me/VPN_Stock'),
            ],
            [
                InlineKeyboardButton('👨🏼‍💻 Developer', url='https://t.me/Lakshan_S'),
                InlineKeyboardButton('👀 Our Group', url='https://t.me/SSH_Store'),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP,
            reply_markup=reply_markup

        )

