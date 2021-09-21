from django.test import TestCase, Client
from django.core.files import File
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import ResourceType, Resource

# Just a write a view demo test


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="Mat4s",
                                        email="matas.sullivan@yopmail.com")
        self.user.set_password('B3nB3n256*')
        self.user.save()

        self.home_url = '/'
        self.reservations_url = reverse('core:reserv_list')

        _type_name = "Studio"
        _type_slug = "studio"
        self.resource_type = ResourceType.objects.create(name=_type_name,
                                                         slug=_type_slug)

        _name = "Mon super studio de test"
        _slug = "mon-super-studio-de-test"
        _price = 14
        _address_line = "Cocody sococe Abidjan CI"
        _country = "Cote d'Ivoire"
        _state = "Cote d'Ivoire"
        _city = "Abidjan"
        _picture = File(open('media/images/resource_type/appart4.jpg', 'rb'))
        self.resource = Resource.objects.create(name=_name,
                                                slug=_slug,
                                                price=_price,
                                                address_line=_address_line,
                                                country=_country,
                                                state=_state,
                                                city=_city,
                                                picture=_picture,
                                                type=self.resource_type)
        self.resource.save()

    def test_home_view(self):
        """ Verify that everyone can se the home page"""
        response = self.client.get(self.home_url)
        # status http 200 query ok
        self.assertEqual(response.status_code, 200)

    def test_redirect_anonymous_user(self):
        """ Redirect a anonymous user who attempt to
        access to the reservations page """
        response = self.client.get(self.reservations_url)
        # status 302 http redirect
        self.assertEqual(response.status_code, 302)
        # Check that the view don't use reservations template
        self.assertTemplateNotUsed(response, 'core/reservation_list.html')
        # Check that the next redirection page is correct
        self.assertRedirects(
            response, '/account/login/?next=/core/resource/reservation/')

    def test_signin_view(self):
        """ Verify if a user can logged in """

        # attempt to log the client
        user_login = self.client.login(username="Mat4s", password="B3nB3n256*")
        response = self.client.get(self.home_url)

        self.assertTrue(user_login)
        # Verify the password
        self.assertTrue(self.user.check_password("B3nB3n256*"))
        # Check if the correct template is used to render the response
        self.assertTemplateUsed(response, 'core/resource_list.html')
