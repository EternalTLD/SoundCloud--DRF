from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from src.audio_library.models import Genre, Album, Audio

User = get_user_model()


class GenreListAPIViewTest(APITestCase):
    def setUp(self):
        Genre.objects.create(title="Test Genre 1")
        Genre.objects.create(title="Test Genre 2")

    def test_list_genres(self):
        url = reverse("audio:genre-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test Genre 1")


class AlbumViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_login(user=self.user)
        self.album = Album.objects.create(
            title="Test Album", user=self.user, description="Test Description"
        )

    def test_list_albums(self):
        url = reverse("audio:album-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Album")

    def test_retrieve_album(self):
        url = reverse("audio:album-detail", kwargs={"pk": self.album.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Album")
        self.assertEqual(response.data["description"], "Test Description")

    def test_create_album(self):
        url = reverse("audio:album-list")
        data = {
            "title": "New Album",
            "description": "New Description",
            "user": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)

    def test_delete_album(self):
        url = reverse("audio:album-detail", kwargs={"pk": self.album.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Album.objects.count(), 0)

    def test_audios_action(self):
        audio = Audio.objects.create(title="Test Audio", user=self.user)
        self.album.audios.add(audio)
        url = reverse("audio:album-audios", kwargs={"pk": self.album.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Audio")


class AudioViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_authenticate(user=self.user)
        self.album = Album.objects.create(
            title="Test Album", description="Test description", user=self.user
        )

    def test_create_audio(self):
        url = reverse("audio:audio-list")
        file_content = b"This is a test file"
        file = SimpleUploadedFile(
            "test_audio.mp3", file_content, content_type="audio/mp3"
        )
        data = {
            "title": "New Audio",
            "file": file,
            "album": self.album.id,
            "user": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Audio.objects.count(), 1)

    def test_delete_audio(self):
        audio = Audio.objects.create(title="Test Audio", user=self.user)
        url = reverse("audio:audio-detail", kwargs={"pk": audio.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Audio.objects.count(), 0)

    def test_update_audio(self):
        audio = Audio.objects.create(title="Test Audio", user=self.user)
        url = reverse("audio:audio-detail", kwargs={"pk": audio.pk})
        updated_data = {"title": "Updated Audio"}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        audio.refresh_from_db()
        self.assertEqual(audio.title, "Updated Audio")

    def test_delete_audio(self):
        audio = Audio.objects.create(title="Test Audio", user=self.user)
        url = reverse("audio:audio-detail", kwargs={"pk": audio.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Audio.objects.count(), 0)

    def test_list_audio(self):
        Audio.objects.create(title="Test Audio 1", user=self.user)
        Audio.objects.create(title="Test Audio 2", user=self.user)
        url = reverse("audio:audio-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_comments_action(self):
        audio = Audio.objects.create(title="Test Audio", user=self.user)
        url = reverse("audio:audio-comments", kwargs={"pk": audio.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_add_comment_action(self):
        audio = Audio.objects.create(title="Test Audio", user=self.user)
        url = reverse("audio:audio-add-comment", kwargs={"pk": audio.pk})
        data = {"text": "Test comment", "audio": audio.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(audio.audio_comments.count(), 1)

    def test_play_action(self):
        file_content = b"This is a test file"
        file = SimpleUploadedFile(
            "test_audio.mp3", file_content, content_type="audio/mp3"
        )
        audio = Audio.objects.create(title="Test Audio Play", user=self.user, file=file)
        url = reverse("audio:audio-play", kwargs={"pk": audio.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download_action(self):
        file_content = b"This is a test file"
        file = SimpleUploadedFile(
            "test_audio.mp3", file_content, content_type="audio/mp3"
        )
        audio = Audio.objects.create(
            title="Test Audio Download", user=self.user, file=file
        )
        url = reverse("audio:audio-download", kwargs={"pk": audio.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
