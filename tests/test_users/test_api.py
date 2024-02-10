from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from src.audio_library.models import Audio, Album, Comment, Playlist


User = get_user_model()


class UserViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.album1 = Album.objects.create(
            title="Test Album 1", description="Test description", user=self.user
        )
        self.album2 = Album.objects.create(
            title="Test Album 2", description="Test description", user=self.user
        )
        self.audio = Audio.objects.create(title="Test Audio", user=self.user)
        self.comment = Comment.objects.create(
            text="Test", audio=self.audio, user=self.user
        )
        self.playlist = Playlist.objects.create(title="Test Playlist", user=self.user)

    def test_create_user(self):
        url = reverse("users:user-list")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_user(self):
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        data = {
            "username": "updated_user",
            "email": "updateduser@example.com",
        }
        self.client.force_login(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_user")
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_delete_user(self):
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_albums(self):
        url = reverse("users:user-albums", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test Album 1")
        self.assertEqual(response.data[0]["description"], "Test description")
        self.assertEqual(response.data[0]["user"], self.user.pk)
        self.assertEqual(response.data[1]["title"], "Test Album 2")
        self.assertEqual(response.data[1]["description"], "Test description")
        self.assertEqual(response.data[1]["user"], self.user.pk)

    def test_user_comments(self):
        url = reverse("users:user-comments", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["text"], "Test")
        self.assertEqual(response.data[0]["audio"], self.audio.pk)
        self.assertEqual(response.data[0]["user"], self.user.pk)

    def test_user_audios(self):
        url = reverse("users:user-audios", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Audio")
        self.assertEqual(response.data[0]["user"], self.user.pk)

    def test_user_playlists(self):
        url = reverse("users:user-playlists", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Playlist")
        self.assertEqual(response.data[0]["user"], self.user.pk)

    def test_user_permission(self):
        another_user = User.objects.create_user(
            username="another_user", password="test_password"
        )
        self.client.force_login(another_user)
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, {"data": "test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(url, {"data": "test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
