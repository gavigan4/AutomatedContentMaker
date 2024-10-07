import os
import praw
from dotenv import load_dotenv
import json

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

# retrieving top weekly post
subreddit = reddit.subreddit('confession')

# make sure sfw
post1 = None
for post in subreddit.top(time_filter='year'):
    if not post.over_18:
        post1 = post
        break

if post1:
    print(f"Title: {post1.title}")
    print(f"Content: {post1.selftext}")

    # save post data
    post_data = {
        'title' : post1.title,
        'content' : post1.selftext
    }

    # write json to be used in tts
    with open('../post_data.json', 'w') as file:
        json.dump(post_data, file, indent=4)


