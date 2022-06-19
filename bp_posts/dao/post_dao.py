import json
from json import JSONDecodeError

from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostsDAO:
    """Менеджер постов: загружает, ищет, получает данные"""

    def __init__(self, path):
        """При создании экземпляра PostsDAO необходимо указать путь к файлу"""
        self.path = path

    def _load_data(self):
        """ Загружает данные из файла и возвращает список словарей"""

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удаётся получить данные из файла {self.path}")

        return posts_data

    def _load_posts(self):
        """ Возвращает список экземпляров класса Post"""

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]

        return list_of_posts

    def get_all(self):
        """Получает все посты"""

        posts = self._load_posts()

        return posts

    # def get_all_short(self):
    #
    #     posts_data = self._load_data()
    #     list_of_posts = [ShortPost(**post_data) for post_data in posts_data]
    #     return list_of_posts

    def get_by_pk(self, pk):
        """Получает пост по его pk"""

        if type(pk) != int:
            raise TypeError("pk must be an int")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):
        """Ищет посты, где в контенте встречается substring"""

        if type(substring) != str:
            raise TypeError("substring must be an str")

        substring = substring.lower()
        posts = self._load_posts()

        matching_post = [post for post in posts if substring in post.content.lower()]

        return matching_post

    def get_by_poster(self, poster_name):
        """Получает посты с определенным автором"""

        if type(poster_name) != str:
            raise TypeError("poster_name must be an str")

        poster_name = poster_name.lower()
        posts = self._load_posts()

        matching_post = [post for post in posts if post.poster_name.lower() == poster_name]

        return matching_post
