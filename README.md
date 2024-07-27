# Discord Moderation Bot

This is a Discord moderation bot built using `discord.py`, pymongo and flask, with additional web pages for displaying database information.

## Features

- **User Moderation**: Manage roles, warnings, and user history.
- **Content Filtering**: Detect and manage banned words and alternative accounts.
- **Database Integration**: Stores data in MongoDB for easy access and persistence.
- **Web Interface**: Displays data such as banned words, sanctions history, command history, and role information.

## Setup

### Installation
- Update `config.json` With **EVERYTHING**
    - **dev** and **admin**, are the id on discord of the dev and admin
      (if you dont have any admin or dev for your bot, just let them empty)
- Install the dependencies:
- - ```pip install -r requirements.txt```

### Mongo DB setup

- [Inscription MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
- create a cluster
- create a database "**UR_DATABASE_NAME**"
- create 4 collection :
    * "**FIRST_COLLECTION**"
    * "**SECOND_COLLECTION**"
    * "**THIRD_COLLECTION**"
    * "**FOURTH_COLLECTION**"
## (Optional) Run the web interface:

- start app.py
- (url should be : http://127.0.0.1:5500)

## Usage

- Use the commands in the `/command` directory to interact with the bot.
- The web interface provides a way to view data like banned words and user histories.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
