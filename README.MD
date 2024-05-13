<!-- PROJECT LOGO -->
<br/>
<div align="center">
  <a href="https://github.com/phamkhoi06/Midori">
    <img src="https://avatars.githubusercontent.com/u/62430582" alt="Logo" width="100" height="100" style="border-radius: 50%;">
  </a>

<h3 align="center">Midori bot</h3>
  <p align="center">
    A multi-purpose discord bot written in Python
    <br/>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#overview">Overview</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- Overview -->
## Overview
Midori is a fully modular bot – meaning all features and commands can be enabled/disabled to your liking and directly through discord chat channel.
This is a self-hosted bot – meaning you will need to host and maintain your own instance. You can do it very easy with a vps, raspberry pi or even your old computer,...

This bot can do: 
- Moderation features.
  * Ban/Unban
  * Mute/Unmute
- Music features (using Youtube platform).
- Fetch random image.
- Get other profile like: banner, avatar,...

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- Python 3: https://www.python.org/downloads
- Discord bot user

### Create a discord bot user (If you already had, skip this section)
1. First, head to Discord's [developer portal](https://discord.com/developers/applications).
2. Sign in if it asks you to, then you should see a screen with a "New Application" button in the top right corner. Click it.
3. Give your bot a name - I called mine "Midori", you can call yours whatever you want. This isn't super important, because you'll be giving it a username later.
4. After you hit "Create", you should see some general info about your bot. You can edit this if you want - give it a name, profile picture, about me, etc - use the profile picture in this repo if you want, or make your own, or don't bother.
5. Navigate to the "Bot" tab in the sidebar. From here you can give it a username - this is what it will show up as in your server.
6. On this page activate the "Message Content Intent" toggle. This is so the bot can read the content of the commands. Make sure to save your changes!

##### After that, the bot is ready to add to your server
1. Go to the "OAuth2" page from the same sidebar.
2. Under "URL generator" select the "bot" checkbox, then under "Bot Permissions" select "Ban Members", "Send Messages", "Manage Messages", "Embed Links", "Connect" and "Speak". Done! That's all permissions the bot needs to work properly.
3. Hit "Copy" next to the URL that got generated and paste it into your browser, then select your server from the dropdown and complete the captcha.

### Installation

1. Get a your bot token at [Discord Portal](https://discord.com/developers/applications).
2. Clone the repo
   ```sh
   git clone https://github.com/phamkhoi06/Midori.git
   cd Midori
   ```
3. Create virtual enviroment (Recommend, you should use it to run bot in isolated enviroment)
   ```bash
   python3 -m venv .venv
   # Then make sure to activate it
   # For Linux
   source .venv/bin/activate
   # For Windows
   # CMD
   .venv\Scripts\activate.bat
   #PowerShell
   .venv\Scripts\Activate.ps1
   ```
4. Install required libraries
   ```sh
   python3 install -r requirements.txt
   ```
5. Enter your bot token in `.env`. Please not delete the first line.

6. Run your bot
  - Windows:
  ```dos
  start bot.cmd
  ```
  - On Linux/Unix-based system:
  ```sh
  chmod +x bot.sh
  ./bot.sh 
  ```
<br/>
Congrats! Now all you need is invite bot to your server and it's already to use. If not, let me know and I'll try to help as best I can.

<!-- USAGE EXAMPLES -->
## Usage

**Attention: All entry with `[]` should be replaced as needed without square brackets**
**Syntax: `[prefix][command] [command options]`**
Default prefix is 'm'. You can change it to whatever you want with `[current prefix]prefix [new prefix]`

Some built-in commands:
- Administrative commands:
  * avatar:   Show up avatar of user mentioned
  * ban:      Ban a member with mention or their id
  * banner:   Show up banner of user mentioned
  * clear:    Clear messages
  * load:     Load a new extension
  * mute:     Mutes the specified user
  * prefix:   Set prefix for commands with [prefix]* command to use the bot
  * presence: Change presence of bot
  * reload:   Reload a existed extension
  * unban:    Unban a member with [username]#[discriminator]
  * unload:   Unload a existed extension
  * unmute:   Unmutes a specified user
- Music:
  * join:     Joins a voice channel.
  * leave:    Clears the queue and leaves the voice channel.
  * loop:     Loops the currently playing song.
  * now:      Displays the currently playing song.
  * pause:    Pauses the currently playing song.
  * play:     Plays a song.
  * queue:    Shows the player's queue.
  * remove:   Removes a song from the queue at a given index.
  * resume:   Resumes a currently paused song.
  * shuffle:  Shuffles the queue.
  * skip:     Skip a song.
  * stop:     Stops playing song and clears the queue.
  * summon:   Summons the bot to a voice channel.
  * volume:   Sets the volume of the player.
- NSFW Commands (Experimental features):
  * s:        Refresh list of Images/Videos
  * select:   Select tag with an interger corresponding to the tag you choice
  * tag:      List all supported tag for select command
  * w:        This command will show images/videos sequentially

