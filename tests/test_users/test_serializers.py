from django.test import TestCase

from src.users.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.validated_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.validated_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.validated_data["username"])
        self.assertEqual(user.email, self.validated_data["email"])
        self.assertTrue(user.check_password(self.validated_data["password"]))

    def test_invalid_data(self):
        invalid_data = {
            "username": "testuser",
            "email": "invalid_email",
            "password": "testpassword",
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_write_only_fields(self):
        serializer = UserSerializer(data=self.validated_data)
        self.assertTrue("password" in serializer.fields)
        self.assertTrue(serializer.fields["password"].write_only)
