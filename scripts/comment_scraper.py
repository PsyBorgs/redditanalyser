#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw

# Connect to Reddit
# ----------------------------

user_agent = "Quick comment thread scraper by /u/mediaarts"
r = praw.Reddit(user_agent = user_agent)


# Get comment thread and populate dict
# ----------------------------

submission_id = "1p1j6c"
submission = r.get_submission(submission_id = submission_id, comment_sort = 'top')
comments = submission.comments

flat_comments = praw.helpers.flatten_tree(comments)
print("flat_comments length: {}".format(len(flat_comments)))
print("flat_comments class: {}".format(type(flat_comments)))
print("first comment class: {}".format(type(flat_comments[0])))
print("last comment class: {}".format(type(flat_comments[len(flat_comments) - 1])))
print("first comment attrs: {}".format(dir(flat_comments[0])))
print("first comment score: {}".format(flat_comments[0].score))
print("first comment author: {}".format(flat_comments[0].author))

fname = submission_id + '.txt'
with open(fname, 'w') as f:
    for comment in flat_comments:
        if isinstance(comment, praw.objects.Comment):
            f.write("\n\n")
            if comment.is_root:
                f.write("---\n\n")
            else:
                f.write("Child comment \n")
            f.write("Author: " + str(comment.author) + "\n")
            f.write("Score: " + str(comment.score) + "\n")
            f.write("Comment: \n\n" + comment.body.encode('utf-8'))
