import os
import praw
from dotenv import load_dotenv
import json

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


def check_and_add_post(post_id, file_path='../red_post_history.json'):
    try:
        # Load the IDs from the file
        with open(file_path, "r") as file:
            ids = set(json.load(file))
    except FileNotFoundError:
        ids = set()  # Start with an empty set if the file doesn't exist

    if post_id in ids:
        return True  # Post ID exists

    # Add the new post ID to the set and save it back to the file
    ids.add(post_id)
    with open(file_path, "w") as file:
        json.dump(list(ids), file, indent=4)

    return False  # Post ID did not exist, now added


# setting subreddit to look at
subreddit = reddit.subreddit('confession')

# make sure sfw and has not been retrieved in past
post1 = None
for post in subreddit.top(time_filter='year'):
    if not post.over_18 and not check_and_add_post(post.id):
        post1 = post
        break

if post1:
    print(f"Title: {post1.title}")
    print(f"Content: {post1.selftext}")

    # save post data
    post_data = {
        'title': post1.title,
        'content': post1.selftext
    }

    # write json to be used in tts later
    with open('../temp_post_data.json', 'w') as file:
        json.dump(post_data, file, indent=4)
