from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from src.audio_library import serializers
from src.audio_library.models import Genre, Album, Audio, Playlist, Comment

User = get_user_model()


class GenreSerializerTest(TestCase):
    def setUp(self):
        self.genre_data = {"title": "Test Genre"}
        self.genre = Genre.objects.create(title="Test Genre")

    def test_genre_serializer(self):
        serializer = serializers.GenreSerializer(instance=self.genre)
        self.assertEqual(serializer.data["title"], self.genre_data["title"])


class AlbumSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.genre = Genre.objects.create(title="Test Genre")
        self.album_data = {
            "user": self.user.pk,
            "title": "Test Album",
            "description": "Test Description",
            "genre": [self.genre.title],
        }
        self.album = Album.objects.create(
            user=self.user, title="Test Album", description="Test Description"
        )

    def test_album_serializer(self):
        serializer = serializers.AlbumSerializer(instance=self.album)
        self.assertEqual(serializer.data["title"], self.album_data["title"])
        self.assertEqual(serializer.data["description"], self.album_data["description"])
        self.assertEqual(serializer.data["user"], self.album_data["user"])


class AudioSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.genre = Genre.objects.create(title="Test Genre")
        self.audio_data = {
            "user": self.user.pk,
            "title": "Test Audio",
            "genre": [self.genre.pk],
            "file": SimpleUploadedFile("test.mp3", b"file_content"),
        }
        self.audio = Audio.objects.create(
            user=self.user, title="Test Audio", file="test.mp3"
        )

    def test_audio_serializer(self):
        serializer = serializers.AudioSerializer(instance=self.audio)
        self.assertEqual(serializer.data["title"], self.audio_data["title"])
        self.assertEqual(
            serializer.data["file"], f"/media/{self.audio_data['file'].name}"
        )


class PlaylistSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.playlist_data = {"user": self.user.pk, "title": "Test Playlist"}
        self.playlist = Playlist.objects.create(user=self.user, title="Test Playlist")

    def test_playlist_serializer(self):
        serializer = serializers.PlaylistSerializer(instance=self.playlist)
        self.assertEqual(serializer.data["title"], self.playlist_data["title"])


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.audio = Audio.objects.create(
            title="Test Audio", user=self.user, file="test.mp3"
        )
        self.comment_data = {
            "user": self.user.pk,
            "audio": self.audio.pk,
            "text": "Test Comment",
        }
        self.comment = Comment.objects.create(
            user=self.user, audio=self.audio, text="Test Comment"
        )

    def test_comment_serializer(self):
        serializer = serializers.CommentSerializer(instance=self.comment)
        self.assertEqual(serializer.data["text"], self.comment_data["text"])
