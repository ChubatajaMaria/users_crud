from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('users')
        data = {
            "username": "admin",
            "first_name": "Мой",
            "last_name": "Бог",
            "password": "12345678",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_success(self):
        """
        Ensure we can login as a new user.
        """
        url = reverse('users')
        data = {
            "username": "admin",
            "first_name": "Мой",
            "last_name": "Бог",
            "password": "12345678",
        }
        self.client.post(url, data, format='json')

        url = reverse('login')
        del data['first_name']
        del data['last_name']
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    def test_login_fail(self):
        """
        Ensure we cannot login with wrong password.
        """
        url = reverse('users')
        data = {
            "username": "admin",
            "first_name": "Мой",
            "last_name": "Бог",
            "password": "12345678",
        }
        self.client.post(url, data, format='json')

        url = reverse('login')
        wrong_credentials = {
            "username": "admin",
            "password": "not_correct",
        }
        response = self.client.post(url, wrong_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        """
        Ensure we can get a user object.
        """
        url = reverse('users')
        data = {
            "username": "admin",
            "first_name": "Мой",
            "last_name": "Бог",
            "password": "12345678"
        }
        response = self.client.post(url, data, format='json')
        data['id'] = response.json()['id']
        del data['password']

        url = reverse('user', args=[data['id']])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), data)

    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        url = reverse('users')
        init_data = {
            "username": "admin",
            "first_name": "Мой",
            "last_name": "Бог",
            "password": "12345678",
        }
        response = self.client.post(url, init_data, format='json')
        init_data['id'] = response.json()['id']
        del init_data['password']

        data = {
            "username": "no_admin",
            "password": "87654321",
        }
        url = reverse('user', args=[init_data['id']])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        init_data.update(data)
        del init_data['password']
        response = self.client.get(url, format='json')
        self.assertDictEqual(response.json(), init_data)  # the username was updated successfully

        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # the password was updated successfully

    def test_delete_user(self):
        """
        Ensure we can delete a user object.
        """
        url = reverse('users')
        data = {
            "username": "admin",
            "first_name": "Мой",
            "last_name": "Бог",
            "password": "12345678",
        }
        response = self.client.post(url, data, format='json')
        user_id = response.json()['id']
        del data['password']

        url = reverse('user', args=[user_id])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
