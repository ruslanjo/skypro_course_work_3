import pytest
from run import app


class TestApi:

    @pytest.fixture
    def response_all_posts(self):
        return app.test_client().get('/api/posts', follow_redirects=True)

    @pytest.fixture
    def keys_expected(self):
        return {'poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count', 'pk'}

    def test_api_all_posts_status_code(self, response_all_posts):
        assert response_all_posts.status_code == 200

    def test_api_all_posts_type(self, response_all_posts):
        assert type(response_all_posts.json) == list

    def test_api_keys(self, response_all_posts, keys_expected):
        posts = response_all_posts.json
        for post in posts:
            assert set(post.keys()) == keys_expected, f'Ключи у поста {post.get("pk")} не совпадают'

    pks = [1, 2, 3, 4, 5, 6]

    @pytest.mark.parametrize("pk", pks)
    def test_api_distinct_post(self, pk, keys_expected):
        post = app.test_client().get('api/posts/' + str(pk), follow_redirects=True)
        print(post.json)
        assert type(post.json) == dict, 'Возвращается не словарь'
        assert set(post.json.keys()) == keys_expected, 'Ключи отличаются'
