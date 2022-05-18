import json


class PostsDAO:

    def __init__(self, path):
        self.path = path

    def get_all_posts(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_posts_by_user(self, user_name):
        selected_posts = []
        posts = self.get_all_posts()
        for post in posts:
            if post.get('poster_name') == user_name:
                selected_posts.append(post)
        return selected_posts

    def get_post_by_pk(self, post_pk):
        try:
            post_pk = int(post_pk)
        except ValueError:
            raise ValueError('ID поста должно быть числом')
        else:
            posts = self.get_all_posts()
            for post in posts:
                if post.get('pk') == post_pk:
                    return post

    def search_for_posts(self, search_query):
        selected_posts = []
        posts = self.get_all_posts()
        for post in posts:
            if search_query.lower() in post.get('content').lower():
                selected_posts.append(post)
        return selected_posts

