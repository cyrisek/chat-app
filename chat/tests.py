from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .models import Contact, Post, Chat


User = get_user_model()


class ContactModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.contact = Contact.objects.create(user=self.user)

    def test_contact_str_representation(self):
        self.assertEqual(str(self.contact), 'testuser')

    def test_default_last_login(self):
        self.assertIsNone(self.contact.last_login)

    def test_default_status(self):
        self.assertEqual(self.contact.status, 'inactive')

    def test_default_profile_img(self):
        self.assertEqual(self.contact.profile_img,
                         'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.contact = Contact.objects.create(user=self.user)
        self.post = Post.objects.create(author=self.contact, body='Test body')

    def test_post_str_representation(self):
        self.assertEqual(str(self.post), 'testuser')

    def test_post_timestamp(self):
        self.assertIsNotNone(self.post.timestamp)


class ChatModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1', password='testpassword')
        self.contact1 = Contact.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(
            username='testuser2', password='testpassword')
        self.contact2 = Contact.objects.create(user=self.user2)
        self.chat = Chat.objects.create()
        self.chat.chatters.add(self.contact1, self.contact2)

    def test_chat_str_representation(self):
        self.assertEqual(str(self.chat), str(self.chat.pk))

    def test_chat_chatters(self):
        self.assertEqual(self.chat.chatters.count(), 2)
        self.assertIn(self.contact1, self.chat.chatters.all())
        self.assertIn(self.contact2, self.chat.chatters.all())

    def test_chat_posts(self):
        self.assertEqual(self.chat.posts.count(), 0)


class IndexURLTest(TestCase):
    def test_index_url(self):
        client = Client()
        response = client.get('/')
        if client.login(username='testuser', password='secret'):
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 302)


class ChatViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(
            username='testuser1', password='password')
        self.contact1 = Contact.objects.create(user=self.user1)
        self.user2 = User.objects.create(
            username='testuser2', password='password')
        self.contact2 = Contact.objects.create(user=self.user2)
        self.chat = Chat.objects.create()
        self.chat.chatters.set([self.contact1.id, self.contact2.id])
        self.post = Post.objects.create(author=self.contact1)

    def test_chat_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            f'/chat/{self.contact2.id}-{self.user1}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat.html')
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'testuser2')
