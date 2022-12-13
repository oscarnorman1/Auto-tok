import json
import praw
import config


def return_instance():
    return praw.Reddit(
        client_id=config.getProperty("client_id"),
        client_secret=config.getProperty("client_secret"),
        password=config.getProperty("password"),
        user_agent=config.getProperty("user_agent"),
        username=config.getProperty("username"),
        check_for_async=config.getProperty("check_for_async")
    )


def return_blob(subreddit, reddit_instance):
    print(reddit_instance.user.me())

    subreddit = reddit_instance.subreddit(subreddit)
    print("SUBREDDIT: {}".format(subreddit))
    top_category = config.getProperty('top_category')
    subreddit_top = subreddit.top(top_category, limit=100)

    tmp_dict_list = []
    for index, best_submission in enumerate(subreddit_top):
        if not best_submission.stickied:
            tmpdict = {
                'title': best_submission.title,
                'content': best_submission.selftext,
                'ups': best_submission.ups,
                'url': best_submission.url
            }
            tmp_dict_list.append(tmpdict)

    winnerPost = sort_posts(tmp_dict_list)

    # Debugging
    print(f'WINNER POST CONTENT: {winnerPost["content"]}')
    print(f'WINNER POST UPS: {winnerPost["ups"]}')
    print(f'WINNER POST URL: {winnerPost["url"]}')

    # Saving for now
    # sentence_list = [' '.join(l[x:x + n]) for x in range(0, len(l), n)]

    return json.dumps(winnerPost)


def sort_posts(dict_list):
    tmp = dict_list
    sorted_by_len_list = []
    for post in tmp:
        if not len(post['content']) > 1000 or len(post['content']) < 300:
            sorted_by_len_list.append(post)

    currMax = 0
    winner = None
    print(f'SORTED_BY_LEN_LIST SIZE: {len(sorted_by_len_list)}')
    for post in sorted_by_len_list:
        if post['ups'] > currMax:
            currMax = post['ups']
            winner = post

    return winner


def fetch_reddit_stuff(subreddit):
    reddit = return_instance()
    blob = json.loads(return_blob(subreddit, reddit))
    return blob
