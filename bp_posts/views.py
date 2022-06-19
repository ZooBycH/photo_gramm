from flask import Blueprint, render_template, abort, request

from config import DATA_PATH_POSTS, DATA_PATH_COMMENT
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post_dao import PostsDAO

post_blueprint = Blueprint("post_blueprint", __name__, template_folder="templates")

# Создаем объекты доступа к данным
post_dao = PostsDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENT)


@post_blueprint.route("/")
def page_posts_index():
    """Страничка для всех постов"""
    all_posts = post_dao.get_all()

    return render_template("index.html", posts=all_posts)


@post_blueprint.route("/posts/<int:pk>/")
def page_posts_single(pk):
    """Страничка для одного поста"""
    post = post_dao.get_by_pk(pk)
    comments = comments_dao.get_comments_by_post_id(pk)

    if post is None:
        abort(404)

    return render_template("post.html", post=post,
                           comments=comments,
                           comments_len=len(comments)
                           )


@post_blueprint.route("/users/<poster_name>")
def page_posts_by_user(poster_name):
    """Страничка для постов пользователя"""

    posts = post_dao.get_by_poster(poster_name)

    if not posts:
        abort(404, "Такого пользователя нет")

    return render_template("user-feed.html", posts=posts, user_name=poster_name)


@post_blueprint.route("/search/")
def page_posts_search():

    query = request.args.get("s", "")

    if query == "":
        posts = []
    else:
        posts = post_dao.search_in_content(query)

    return render_template("search.html", posts=posts, query=query, search_count=len(posts))
