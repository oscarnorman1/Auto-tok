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
    subreddit_top = subreddit.top(top_category, limit=10)

    best_submission = ''

    tmpdict = {}
    tmp_dict_list = []
    for index, best_submission in enumerate(subreddit_top):
        if not best_submission.stickied:
            tmpdict = {
                'content': best_submission.selftext,
                'ups': best_submission.ups,
                'spot': index + 1
            }
            tmp_dict_list.append(tmpdict)

    winnerPost = sort_posts(tmp_dict_list)
    print(f'WINNER POST CONTENT: {winnerPost["content"]}')
    print(f'WINNER POST UPS: {winnerPost["ups"]}')
    print(f'WINNER POST SPOT: {winnerPost["spot"]}')
    # print('Title: {}, Ups: {}, Downs: {}'.format(submission.title, submission.ups, submission.downs))
    # title = best_submission.title
    # ups = best_submission.ups
    content = best_submission.selftext
    l = content.split()
    n = 7
    sentence_list = [' '.join(l[x:x + n]) for x in range(0, len(l), n)]

    values = {
        # 'title': title,
        # 'ups': ups,
        'sentence_list': sentence_list,
        'sentence_list_full': content
    }
    return json.dumps(values)


def sort_posts(dict_list):
    tmp = dict_list
    sorted_by_len_list = []
    for post in tmp:
        print(f'SPOTS: {post["spot"]}')
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





def main():
    blob = fetch_reddit_stuff('confession')
    #print(f'1st POST: {blob["best_submission_list"][0]}')
    #print(f'2nd POST: {blob["best_submission_list"][1]}')
    #print(f'3rd POST: {blob["best_submission_list"][2]}')
    #print(f'4th POST: {blob["best_submission_list"][3]}')
    #print(f'5th POST: {blob["best_submission_list"][4]}')
    #print(f'6th POST: {blob["best_submission_list"][5]}')
    #print(f'7th POST: {blob["best_submission_list"][6]}')
    #print(f'8th POST: {blob["best_submission_list"][7]}')
    #print(f'9th POST: {blob["best_submission_list"][8]}')
    #print(f'10th POST: {blob["best_submission_list"][9]}')


def fetch_reddit_stuff(subreddit):
    reddit = return_instance()
    blob = json.loads(return_blob(subreddit, reddit))
    return blob


if __name__ == "__main__":
    main()
