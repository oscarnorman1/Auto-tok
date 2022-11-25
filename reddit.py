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
    subreddit_hot = subreddit.hot(limit=10)

    all_comments = []
    best_submission = ''

    for best_submission in subreddit_hot:
        if not best_submission.stickied:
            best_submission = best_submission
            break

    # print('Title: {}, Ups: {}, Downs: {}'.format(submission.title, submission.ups, submission.downs))
    title = best_submission.title
    ups = best_submission.ups
    content = best_submission.selftext

    values = {
        'title': title,
        'ups': ups,
        'content': content
    }

    #    for top in top_comments:
    #        print('Comment: {}, Ups: {}'.format(top.body, top.ups))

    return json.dumps(values)
