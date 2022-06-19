import logging

from flask import Blueprint, jsonify, abort

from config import DATA_PATH_POSTS, DATA_PATH_COMMENT
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post_dao import PostsDAO

api_blueprint = Blueprint("api_blueprint", __name__)

# Создаем объекты доступа к данным
post_dao = PostsDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENT)

api_logger = logging.getLogger("api_logger")


@api_blueprint.route('/posts/')
def api_posts_all():
    """Эндпоинт для всех постов"""
    all_posts = post_dao.get_all()
    all_posts_as_dict = [post.as_dict() for post in all_posts]

    api_logger.debug("Запрошены все посты")

    return jsonify(all_posts_as_dict), 200


@api_blueprint.route('/posts/<int:pk>/')
def api_posts_single(pk):
    """Эндпоинт для одного поста"""

    post = post_dao.get_by_pk(pk)

    api_logger.debug(f"Запрошен  пост {pk}")

    if post is None:
        api_logger.error(f"Обращение к несуществующему посту {pk}")
        abort(404)

    return jsonify(post.as_dict()), 200


@api_blueprint.errorhandler(404)
def api_error_404(error):
    api_logger.error(f"Ошибка {error}")
    return jsonify({"error": str(error)}), 404


@api_blueprint.route('/')
def api_posts_hello():
    return "Это API. Доступные эндпотнты /api/posts  и /api/posts/<pk>"
