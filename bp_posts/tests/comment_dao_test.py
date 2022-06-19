import pytest as pytest

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO


class TestCommentDAO:

    @pytest.fixture()
    def comment_dao(self):
        comment_dao_instance = CommentDAO("./bp_posts/tests/comments_mock.json")
        return comment_dao_instance

    def test_get_comments_by_post_id_all_type(self, comment_dao):
        comment = comment_dao.get_comments_by_post_id(1)
        assert type(comment) == list, "incorrect type fot result  single item"

    def test_get_comments_by_post_id_single_type(self, comment_dao):
        comment = comment_dao.get_comments_by_post_id(1)[0]
        assert type(comment) == Comment, "incorrect type fot result  single item"

    def test_get_comments_by_post_id_not_content(self, comment_dao):
        comment = comment_dao.get_comments_by_post_id(2)
        assert comment == [], "Должен быть [] если у поста нет комментариев"

