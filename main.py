import os
from composio_llamaindex import App, Action, ComposioToolSet
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.llms import ChatMessage
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

def composio():

    # Initialize LLM
    llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    # Get Composio tools
    toolset = ComposioToolSet()
    tools = toolset.get_tools(actions=[Action.TWITTER_USER_LOOKUP_BY_USERNAME, Action.TWITTER_BOOKMARKS_BY_USER, Action.TWITTER_RECENT_SEARCH, Action.TAVILY_TAVILY_SEARCH, Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM])


    prefix_messages = [
        ChatMessage(
            role="system",
                content=(
                """You are an advanced trend analyzer specializing in AI technology trends.
                    
                    Output Format:
                    :relevant emoji: Trend Title [Trend Score: X/10] [Momentum: ↑↓→]
                    - Key Insight: One-line summary
                    - Evidence: Engagement metrics across platforms, do not say based on Tavily Search but suggest what kind of posts are doing well.
                    - Market Impact: Potential business implications
                    - Action Items: Specific next steps
                    
                    Guidelines:
                    1. Cross-validate trends across platforms
                    2. Include engagement metrics (views, likes, shares)
                    3. Provide sentiment analysis
                    4. Compare with historical data
                    5. Add expert citations when available
                    6. Identify market opportunities
                    7. Suggest practical applications
                    
                    Search Strategy:
                    - Use broad keyword clusters for Twitter search
                    - Leverage Tavily for LinkedIn professional insights
                    - Analyze bookmark patterns for emerging topics

                    Rules: 
                    1. First fetch id from the username.
                    2. Then fetch the bookmarks from the id.
                    3. Then based on the keywords, search twitter.
                    4. Search for the keywords on tavily and collect all the linkedin related posts that have done well.
                    5. Then compile all of this info, write it in the above format the correct amount of times and send it.
                    """
                ),
            )
        ]
        
    agent = FunctionCallingAgentWorker(
            tools=tools, # type: ignore
            llm=llm,
            prefix_messages=prefix_messages,
            max_function_calls=10,
            allow_parallel_tool_calls=False,
            verbose=True,
        ).as_agent()
        
    id = '@HoChris44859' #your twitter id
    return str(agent.chat(f"What are the top 3 latest trends within artificial intelligence from twitter from my bookmarks, search and linkedin, my id is {id}."))


# # Old non Bolt Slack stuff
# print(output_text)

# client = WebClient(token=os.getenv("SLACK_TOKEN"))
# try:
#     response = client.chat_postMessage(channel="#slack-bot-test-chris", text=output_text)
#     assert response["message"]["text"] == output_text
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["ok"] is False
#     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#     print(f"Got an error: {e.response['error']}")
#     # Also receive a corresponding status_code
#     assert isinstance(e.response.status_code, int)
#     print(f"Received a response status_code: {e.response.status_code}")



# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("trendfinder")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say("Sure! Give me ne second while I search the web...")
    output_text = composio()
    say(output_text)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()