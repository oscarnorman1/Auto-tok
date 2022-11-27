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
    subreddit_top = subreddit.top('week', limit=1)

    all_comments = []
    best_submission = ''

    for best_submission in subreddit_top:
        if not best_submission.stickied:
            best_submission = best_submission
            break

    # print('Title: {}, Ups: {}, Downs: {}'.format(submission.title, submission.ups, submission.downs))
    title = best_submission.title
    ups = best_submission.ups
    content = best_submission.selftext
    l = content.split()
    n = 7
    sentence_list = [' '.join(l[x:x + n]) for x in range(0, len(l), n)]

    values = {
        'title': title,
        'ups': ups,
        'sentence_list': sentence_list,
        'sentence_list_full': content
    }

    #    for top in top_comments:
    #        print('Comment: {}, Ups: {}'.format(top.body, top.ups))

    return json.dumps(values)
