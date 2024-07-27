# Discord Moderation Bot

This is a Discord moderation bot built using `discord.py` and MongoDB, with additional web pages for displaying database information.

## Features

- **User Moderation**: Manage roles, warnings, and user history.
- **Content Filtering**: Detect and manage banned words and alternative accounts.
- **Database Integration**: Stores data in MongoDB for easy access and persistence.
- **Web Interface**: Displays data such as banned words, user history, and role information.

## Setup

### Installation
- Update `config.json` with your Discord bot token and MongoDB URI.
- Install the dependencies:

## (Optional) Run the web interface:

- start app.py
- (url should be : http://127.0.0.1:5500)
- - ''' pip install -r requirements.txt'''

## Usage

- Use the commands in the `/command` directory to interact with the bot.
- The web interface provides a way to view data like banned words and user histories.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
