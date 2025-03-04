import os
from composio_llamaindex import App, Action, ComposioToolSet
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.llms import ChatMessage
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime

load_dotenv()

def composio(text, month, year):

    # Initialize LLM
    llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    # Get Composio tools
    toolset = ComposioToolSet()
    tools = toolset.get_tools(actions=[Action.TWITTER_RECENT_SEARCH, Action.TAVILY_TAVILY_SEARCH, Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM])


    prefix_messages = [
        ChatMessage(
            role="system",
                content=(
                f"""You are an advanced trend analyzer specializing in {text}.
                    
                    Output Format:
                    :emoji: Trend Title [Trend Score: X/10] [Momentum: ↑↓→]
                    - Key Insight: One-line summary
                    - Evidence: Engagement metrics across platforms, do not say based on Tavily Search but suggest what kind of posts are doing well.
                    - Market Impact: Potential business implications
                    - Action Items: Specific next steps
                    Sources: Provide links to sources used
                    
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

                    Rules: 
                    1. Search Twitter using keywords on most recent posts
                    2. Search Twitter using keywords on most popular posts
                    3. Search for the keywords on tavily and collect all the linkedin related posts that have done well.
                    4. Then compile all of this info, write it in the above format the correct amount of times and send it.
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
        
    return str(agent.chat(f"What are 3 of the latest trends in {month}, {year} regarding {text} based on twitter and linkedin?"))


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

    print(message)
    print(message["text"])
    text = message["text"].replace('trendfinder', '').strip()
    say(f"Sure! Give me a couple seconds while I search the web for {text}...")

    current_month = datetime.now().month
    current_year = datetime.now().year

    output_text = composio(text, current_month, current_year)
    say(output_text)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()