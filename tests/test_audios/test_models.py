from django.test import TestCase
from django.contrib.auth import get_user_model

from src.audio_library.models import Genre, Album, Audio, Comment, Playlist

User = get_user_model()


class GenreTestCase(TestCase):
    def setUp(self) -> None:
        self.genre = Genre.objects.create(title="Test Genre")

    def test_genre_creation(self):
        genre = Genre.objects.get(title="Test Genre")
        self.assertEqual(genre.title, "Test Genre")
        self.assertEqual(str(genre.title), "Test Genre")


class AlbumTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username="test_user1", password="test_password"
        )
        self.user2 = User.objects.create_user(
            username="test_user2", password="test_password"
        )
        self.genre1 = Genre.objects.create(title="Test Genre1")
        self.genre2 = Genre.objects.create(title="Test Genre2")
        self.genre3 = Genre.objects.create(title="Test Genre3")
        self.audio1 = Audio.objects.create(
            title="Test Audio1", user=self.user1, file="test1.mp3"
        )
        self.audio2 = Audio.objects.create(
            title="Test Audio2", user=self.user2, file="test2.mp3"
        )
        self.album = Album.objects.create(
            title="Test Album", user=self.user1, description="Test Description"
        )

    def test_album_creation(self):
        album = Album.objects.get(title="Test Album")
        self.assertEqual(album.title, "Test Album")
        self.assertEqual(album.user, self.user1)
        self.assertEqual(album.description, "Test Description")

    def test_album_genres(self):
        album = Album.objects.get(title="Test Album")
        album.genre.add(self.genre1)
        album.genre.add(self.genre2)
        album.genre.add(self.genre3)
        self.assertIn(self.genre1, album.genre.all())
        self.assertIn(self.genre2, album.genre.all())
        self.assertIn(self.genre3, album.genre.all())

        album.genre.remove(self.genre2)
        self.assertIn(self.genre1, album.genre.all())
        self.assertNotIn(self.genre2, album.genre.all())
        self.assertIn(self.genre3, album.genre.all())

    def test_album_likes(self):
        album = Album.objects.get(title="Test Album")
        album.likes.add(self.user1)
        album.likes.add(self.user2)
        self.assertIn(self.user1, album.likes.all())
        self.assertIn(self.user2, album.likes.all())
        self.assertEqual(album.count_likes, 2)

        album.likes.remove(self.user2)
        self.assertIn(self.user1, album.likes.all())
        self.assertNotIn(self.user2, album.likes.all())
        self.assertEqual(album.count_likes, 1)

    def test_album_audios(self):
        album = Album.objects.get(title="Test Album")
        album.audios.add(self.audio1)
        album.audios.add(self.audio2)
        self.assertEqual(album.count_audios, 2)
        self.audio1.delete()
        self.assertEqual(album.count_audios, 1)
        album.audios.remove(self.audio2)
        self.assertEqual(album.count_audios, 0)

    def test_album_str(self):
        album = Album.objects.get(title="Test Album", user__username="test_user1")
        self.assertEqual(str(album), "test_user1 - Test Album")


class AudioTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.genre = Genre.objects.create(title="Test Genre")
        self.audio = Audio.objects.create(
            title="Test Audio", user=self.user, file="test.mp3"
        )

    def test_audio_creation(self):
        audio = Audio.objects.get(title="Test Audio")
        self.assertEqual(audio.title, "Test Audio")
        self.assertEqual(audio.user, self.user)
        self.assertEqual(audio.file, "test.mp3")

    def test_audio_genres(self):
        audio = Audio.objects.get(title="Test Audio")
        audio.genre.add(self.genre)
        self.assertIn(self.genre, audio.genre.all())

    def test_audio_likes(self):
        audio = Audio.objects.get(title="Test Audio")
        audio.likes.add(self.user)
        self.assertIn(self.user, audio.likes.all())
        self.assertEqual(audio.count_likes, 1)

        audio.likes.remove(self.user)
        self.assertNotIn(self.user, audio.likes.all())
        self.assertEqual(audio.count_likes, 0)


class CommentTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.audio = Audio.objects.create(
            title="Test Audio", user=self.user, file="test.mp3"
        )
        self.comment = Comment.objects.create(
            text="Test Comment", audio=self.audio, user=self.user
        )

    def test_comment_creation(self):
        comment = Comment.objects.get(text="Test Comment")
        self.assertEqual(comment.text, "Test Comment")
        self.assertEqual(comment.audio, self.audio)
        self.assertEqual(comment.user, self.user)

    def test_comment_likes(self):
        comment = Comment.objects.get(text="Test Comment")
        comment.likes.add(self.user)
        self.assertIn(self.user, comment.likes.all())
        self.assertEqual(comment.count_likes, 1)

        comment.likes.remove(self.user)
        self.assertNotIn(self.user, comment.likes.all())
        self.assertEqual(comment.count_likes, 0)


class PlaylistTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.audio = Audio.objects.create(
            title="Test Audio", user=self.user, file="test.mp3"
        )
        self.playlist = Playlist.objects.create(title="Test Playlist", user=self.user)

    def test_playlist_creation(self):
        playlist = Playlist.objects.get(title="Test Playlist")
        self.assertEqual(playlist.title, "Test Playlist")
        self.assertEqual(playlist.user, self.user)

    def test_playlist_audios(self):
        playlist = Playlist.objects.get(title="Test Playlist")
        playlist.audios.add(self.audio)
        self.assertIn(self.audio, playlist.audios.all())

        playlist.audios.remove(self.audio)
        self.assertNotIn(self.audio, playlist.audios.all())

    def test_playlist_count_audios(self):
        playlist = Playlist.objects.get(title="Test Playlist")
        self.assertEqual(playlist.count_audios, 0)

        playlist.audios.add(self.audio)
        self.assertEqual(playlist.count_audios, 1)

        playlist.audios.create(title="Test Audio 2", user=self.user, file="test2.mp3")
        self.assertEqual(playlist.count_audios, 2)

    def test_playlist_str(self):
        playlist = Playlist.objects.get(title="Test Playlist")
        self.assertEqual(str(playlist), "Playlist - Test Playlist")
