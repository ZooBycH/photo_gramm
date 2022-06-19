import json
from json import JSONDecodeError
from pprint import pprint as pp
from bp_posts.dao.comment import Comment
from exceptions.data_exceptions import DataSourceError


class CommentDAO:
    """Менеджер комментов: загружает, ищет, получает данные"""

    def __init__(self, path):
        """При создании экземпляра CommentsDAO необходимо указать путь к файлу"""
        self.path = path

    def _load_data(self):
        """Загружает данные из файла"""

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                comment_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удаётся получить данные из файла {self.path}")

        return comment_data

    def _load_comments(self):
        """ Возвращает список экземпляров класса Comments"""

        comments_data = self._load_data()
        list_of_comments = [Comment(**comment_data) for comment_data in comments_data]

        return list_of_comments

    def get_comments_by_post_id(self, post_id):
        """Возвращает комментарии определенного поста"""

        if type(post_id) != int:
            raise TypeError("post_id must be an int")

        comments = self._load_comments()
        # posts_id = [comment.post_id for comment in comments]
        # if post_id not in posts_id:
        #     raise ValueError("Такого поста нет")

        post_comment = []
        for p_comment in comments:
            if p_comment.post_id == post_id:
                if len(p_comment.comment) > 0:
                    post_comment.append(p_comment)

        return post_comment


