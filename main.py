import os
import praw
from dotenv import load_dotenv

# loading env variables
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

# setting up reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# test
# subreddit = reddit.subreddit('python')
# for post in subreddit.hot(limit=5):
#     print(post.title)

