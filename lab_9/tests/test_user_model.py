import unittest
from models.user import User


class TestUserModel(unittest.TestCase):

    def test_create_valid_user(self):
        u = User(user_id=5, name="Михаил")
        self.assertEqual(u.id, 5)
        self.assertEqual(u.name, "Михаил")

    def test_invalid_user_id(self):
        with self.assertRaises(ValueError):
            User(user_id=-1, name="Имя")

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            User(user_id=1, name="A")
