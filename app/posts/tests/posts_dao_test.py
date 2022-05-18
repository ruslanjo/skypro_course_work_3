import pytest
from app.posts.dao.posts_dao import PostsDAO


class TestPostDao():

    @pytest.fixture
    def posts_dao(self):
        return PostsDAO('data/posts.json')

    @pytest.fixture
    def keys_expected(self):
        return {'poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count', 'pk'}

    def test_get_all_posts_check_types(self, posts_dao):
        posts = posts_dao.get_all_posts()
        assert type(posts) == list, 'Тип данных постов д.б. список'

    def test_get_all_posts_check_type_first(self, posts_dao):
        posts = posts_dao.get_all_posts()
        assert type(posts[0]) == dict, 'Тип данных одного поста д.б. словарь'

    def test_get_all_posts_check_keys(self, posts_dao, keys_expected):
        assert set(posts_dao.get_all_posts()[0].keys()) == keys_expected


    user_names = ['leo', 'johnny']

    @pytest.mark.parametrize('user_name', user_names)
    def test_get_posts_by_users(self, posts_dao, user_name):
        assert posts_dao.get_posts_by_user(user_name)[0]['poster_name'] == user_name

    pks = [1, 2, 3, 4, 5, 6]

    @pytest.mark.parametrize("pk", pks)
    def test_get_post_by_pk(self, posts_dao, pk):
        post = posts_dao.get_post_by_pk(pk)
        assert post.get('pk') == pk

    search_query_pks = [('утр', {4, 8}), ('лампочк', {6})]
    @pytest.mark.parametrize("query, expected_pks",  search_query_pks)
    def test_search_for_posts(self, posts_dao, query, expected_pks):
        pks = set()
        posts = posts_dao.search_for_posts(query)
        for post in posts:
            pks.add(post.get('pk'))
        assert expected_pks == pks, 'Неверные ID постов при поиске'
