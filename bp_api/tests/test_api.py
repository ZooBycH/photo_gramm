import pytest
from flask import Flask

# from main import create_and_config_app
import main


class TestApi:
    post_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    @pytest.fixture
    def app_instance(self):
        app = main.app
        test_client = app.test_client()
        return test_client

    def test_all_posts_status_code(self, app_instance):
        response = app_instance.get("/api/posts", follow_redirects=True)
        assert response.status_code == 200

    def test_single_posts_status_code(self, app_instance):
        response = app_instance.get("/api/posts/1", follow_redirects=True)
        assert response.status_code == 200

    def test_posts_has_all_type(self, app_instance):
        response = app_instance.get('/api/posts/')
        result = response.get_json()
        assert type(result) == list

    def test_posts_has_all_keys_correct(self, app_instance):
        response = app_instance.get('/api/posts/')
        result = response.get_json()
        result_keys = set(result[0].keys())
        assert result_keys == self.post_keys

    def test_posts_has_single_type(self, app_instance):
        response = app_instance.get('/api/posts/1/')
        result = response.get_json()
        assert type(result) == dict

    def test_posts_has_single_keys_correct(self, app_instance):
        response = app_instance.get('/api/posts/1/')
        result = response.get_json()
        result_keys = set(result.keys())
        assert result_keys == self.post_keys
