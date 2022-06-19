import pytest as pytest

from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostsDAO


def check_fields(post):
    fields = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    for field in fields:
        assert hasattr(post, field), f"Нет поля {field}"


class TestPostDAO:

    @pytest.fixture()
    def post_dao(self):
        post_dao_instance = PostsDAO("./bp_posts/tests/post_mock.json")
        return post_dao_instance

    ### Для функции получения всех экземпляров

    def test_get_all_type(self, post_dao):
        posts = post_dao.get_all()
        assert type(posts) == list, "incorrect type fot result object"

    def test_get_single_type(self, post_dao):
        post = post_dao.get_all()[0]
        assert type(post) == Post, "incorrect type fot result  single item"

    def test_get_all_fields(self, post_dao):
        post = post_dao.get_all()[0]

        check_fields(post)

    def test_get_all_correct_pks(self, post_dao):
        posts = post_dao.get_all()
        correct_pks = {1, 2, 3}

        pks = set([post.pk for post in posts])
        assert pks == correct_pks, "Некорректные id"

    ### Для функции получения одного экземпляра по pk

    def test_get_by_pk_type(self, post_dao):
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, "incorrect type fot result  single item"

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_by_pk(999)
        assert post is None, "Should be None for non existent pk"

    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"Некорректное значение pk для запрошенного поста с pk = {pk}"

    ### Для функции получения постов по вхождению строки

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_in_content("еда")
        assert type(posts) == list, "incorrect type fot result object"

        post = post_dao.search_in_content("еда")[0]
        assert type(post) == Post, "incorrect type fot result  single item"

    def test_search_in_content_fields(self, post_dao):
        post = post_dao.search_in_content("еда")[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_in_content("1234567899874651221")
        assert posts == [], "Должен быть [] если substring нет в постах"

    @pytest.mark.parametrize("s, expected_pks", [
        ("еда", {1}),
        ("днем", {2}),
        ("на", {1, 2, 3})
    ])
    def test_search_in_content_result(self, post_dao, s, expected_pks):
        posts = post_dao.search_in_content(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f"Incorrect result searching for {s}"

    ### Для функции получения постов по имени автора

    def test_get_by_poster_type(self, post_dao):
        post = post_dao.get_by_poster("hank")[0]
        assert type(post) == Post, "incorrect type fot result  single item"

    def test_get_by_poster_fields(self, post_dao):
        post = post_dao.get_by_poster("hank")[0]
        check_fields(post)

    def test_get_by_poster_not_found(self, post_dao):
        post = post_dao.get_by_poster("777777777")
        assert post == [], "Should be None for non existent poster_name"

    @pytest.mark.parametrize("poster_name", ["leo", "johnny", "hank"])
    def test_get_by_poster_correct_name(self, post_dao, poster_name):
        post = post_dao.get_by_poster(poster_name)[0]
        assert post.poster_name == poster_name, f"Некорректное значение poster_name для запрошенного поста"


