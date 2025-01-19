# Trend Finder Agent Slack Bot using Groq, Composio, Tavily

This guide provides detailed steps to create a Trend Finder agent that leverages Groq and Composio to research and find trends on Twitter and Linkedin. 

## Steps to Run Locally

Prerequisites:

Python 3.8 or higher installed.
A groq account, composio account, twitter account.

As well as the API keys for the things listed below.

```
COMPOSIO_API_KEY=KEY
GROQ_API_KEY=KEY
SLACK_BOT_TOKEN=KEY
SLACK_APP_TOKEN=KEY
```

Additionally, you will need sign in with a twitter account when prompted and input a Tavily API key from the terminal when you run the application.

Tavily=KEY

**Navigate to the Project Directory:**
Change to the directory where the `setup.sh`, `main.py`, `requirements.txt`, and `README.md` files are located. For example (assuming you just git cloned the repo)

If you type `ls` and you see the files above you're in the correct directory.

Otherwise, navigate into the folder with `cd slack-bot-groq`

Fill in the .env file with your secrets.

```
COMPOSIO_API_KEY=KEY
GROQ_API_KEY=KEY
SLACK_BOT_TOKEN=KEY
SLACK_APP_TOKEN=KEY
```

### Run the Setup File

Make the [setup.sh](http://setup.sh/) Script Executable (if necessary):
On Linux or macOS, you might need to make the [setup.sh](http://setup.sh/) script executable:

```
chmod +x setup.sh

```

Execute the [setup.sh](http://setup.sh/) script to set up the environment, install dependencies, login to composio and
add necessary tools:

```
./setup.sh

```

You’ll be asked to login to your twitter account via composio.

![Screenshot 2025-01-17 at 12.05.05 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/7ab21512-3597-42cc-ab4e-9daaccbe9162/3976a2a0-442a-4fa8-b2f0-7b9320c1f55c/Screenshot_2025-01-17_at_12.05.05_PM.png)

![Screenshot 2025-01-17 at 12.20.52 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/7ab21512-3597-42cc-ab4e-9daaccbe9162/7c563311-496d-497a-8d41-1065d7bbd9cf/Screenshot_2025-01-17_at_12.20.52_PM.png)

As well as for your Tavily API key.

On subsequent/later script runs, it’ll ask you whether you want to replace previous twitter or tavily keys, enter y for yes (to input a new one) or n for no if it’s already working.

**install all of the things in the requirements file before the next step**

pip3 install -r requirements.txt

### Run the python script

```
Run the command below. If you're using python version 3 then make sure to add the 3 to the end of the python word.)

python3 main.py
```

Something I ran into was this issue with Python:

https://github.com/slackapi/bolt-python/issues/673

If you run into it, just run the certificate command by double clicking on it in the folder view and you should be fine.

**Install from the slack bot marketplace**


Add the bot to your workspace.

**Invite the bot into a channel**

/invite @trend-finder-slack-groq

**To remove the bot from a channel**

/***kick*** @trend-finder-slack-groq

To use the bot, make sure the python script above is running and type in the channel

“trendfinder”

Notes:

The twitter username id in the code (found on line 69) and twitter account sign in during the prompt has to be from the same account otherwise the results will be a little off. The program will still work, but it will mainly lean on the linkedin results.