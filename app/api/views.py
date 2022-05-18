from flask import Blueprint, jsonify
from config import POSTS_JSON_PATH
from app.posts.dao.posts_dao import PostsDAO

posts_dao = PostsDAO(POSTS_JSON_PATH)

api_blueprint = Blueprint('api_blueprint', __name__, template_folder='templates')


@api_blueprint.route('/api/posts')
def api_return_posts():
    posts = posts_dao.get_all_posts()
    return jsonify(posts)


@api_blueprint.route('/api/posts/<int:post_pk>')
def api_return_post_by_pk(post_pk):
    post = posts_dao.get_post_by_pk(post_pk)
    return jsonify(post)
