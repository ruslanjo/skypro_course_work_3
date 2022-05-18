import logging
from flask import Blueprint, render_template, request, abort, redirect
from json import JSONDecodeError
from config import POSTS_JSON_PATH, COMMENTS_JSON_PATH, BOOKMARKS_JSON_PATH
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDAO
from app.posts.dao.bookmarks_dao import BookmarksDAO

logger = logging.getLogger('basic')

posts_dao = PostsDAO(POSTS_JSON_PATH)
comments_dao = CommentsDAO(COMMENTS_JSON_PATH)
bookmarks_dao = BookmarksDAO(BOOKMARKS_JSON_PATH)


posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')


@posts_blueprint.route('/')
def index_page():
    logger.info('Запрошены все посты')
    try:
        posts = posts_dao.get_all_posts()
    except FileNotFoundError as e:
        logger.error(f'Не получилось найти файл: {e}')
        return f'Такого файла нет. Код ошибки: {e}', 404
    except JSONDecodeError as e:
        logger.error(f'Не получилось декодировать JSON {e}')
        return f'Не получилось декодировать JSON. ' \
               f'Проверьте правильность формата. Код ошибки: {e}', 404
    else:
        bookmarks_count = len(bookmarks_dao.get_all_bookmarks())
        logger.info('Файл постов успешно прочитан, возвращаем страницу с постами')
        return render_template('index.html', posts=posts, bookmarks_count=bookmarks_count)


@posts_blueprint.route('/search')
def search_page():
    logger.info('Выполняется поиск по постам')
    query = request.values.get('search')
    posts_found = posts_dao.search_for_posts(query)
    posts_found = posts_found[-10:]  # По ТЗ необходимо выводить последние 10 постов
    return render_template('search.html', posts=posts_found, query=query)


@posts_blueprint.route('/posts/<post_pk>')
def post_page(post_pk):
    logger.info('Запрос поста по id')
    try:
        post_pk = int(post_pk)
    except ValueError:
        return 'Неправильный формат id поста. Должен быть целым числом', 404
    else:
        post = posts_dao.get_post_by_pk(post_pk)
        if post is None:
            abort(404)
        post_comments = comments_dao.get_comments_by_pk(post_pk)
        return render_template('post.html', post=post, comments=post_comments)


@posts_blueprint.errorhandler(404)
def post_error(e):
    return 'Такой пост не найден', 404


@posts_blueprint.route('/users/<user_name>')
def user_page(user_name):
    logger.info(f'Показываю посты пользователя {user_name}')
    posts = posts_dao.get_posts_by_user(user_name)
    return render_template('user-feed.html', posts=posts)


@posts_blueprint.route('/bookmarks/add/<post_pk>')
def add_bookmark(post_pk):
    logger.info(f'Добавляю в закладки {post_pk}')
    try:
        post_pk = int(post_pk)
    except ValueError:
        logger.error(f'Для добавления закладки передан неправильный post pk. Передано: {post_pk}')
        return 'Пост PK должен быть целым числом'
    else:
        post_to_add = posts_dao.get_post_by_pk(post_pk)
        bookmarks_dao.add_bookmark(post_to_add)
        return redirect("/", code=302)


@posts_blueprint.route('/bookmarks/delete/<post_pk>')
def delete_bookmark(post_pk):
    logger.info(f'Удаляю закладку {post_pk}')
    try:
        post_pk = int(post_pk)
    except ValueError as e:
        logger.error(e)
        return 'Пост PK должен быть целым числом'
    else:
        bookmarks_dao.delete_bookmark_by_post_pk(post_pk)
        return redirect('/bookmarks', code=302)


@posts_blueprint.route('/bookmarks')
def bookmarks_page():
    bookmarks = bookmarks_dao.get_all_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)
