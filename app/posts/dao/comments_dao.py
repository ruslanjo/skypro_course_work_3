import json


class CommentsDAO:
    def __init__(self, path):
        self.path = path

    def get_all_comments(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            comments = json.load(file)
        return comments

    def get_comments_by_pk(self, post_pk):
        comments = self.get_all_comments()
        selected_comments = [comment for comment in comments if comment.get('post_id') == post_pk]
        return selected_comments
