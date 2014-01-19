from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.test import LiveServerTestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from selenium.webdriver.firefox.webdriver import WebDriver

from contacts.models import Contact
from contacts.views import ListContactView
from contacts.forms import ContactForm


class ContactListIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ContactListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):

        cls.selenium.quit()
        super(ContactListIntegrationTests, cls).tearDownClass()

    def test_contact_listed(self):

        Contact.objects.create(first_name='foo', last_name='bar')

        self.selenium.get('%s%s' % (self.live_server_url, '/'))

        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[0].text,
            'foo bar ( edit )')

    def test_add_contact_linked(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
            self.selenium.find_element_by_link_text('add contact'))

    def test_add_contact(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys(
            'test@example.com')
        self.selenium.find_element_by_id('id_confirm_email').send_keys(
            'test@example.com')
        self.selenium.find_element_by_id('save_contact').click()

        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[-1].text,
            'test contact ( edit )')

    def test_edit_contact(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))

        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys(
            'edit@example.com')
        self.selenium.find_element_by_id('id_confirm_email').send_keys(
            'edit@example.com')
        self.selenium.find_element_by_id('save_contact').click()

        self.selenium.find_element_by_id('edit_1').click()

        self.selenium.find_element_by_id('id_first_name').send_keys(
            "\b" * 4)

        self.selenium.find_element_by_id('id_first_name').send_keys(
            'New')

        self.selenium.find_element_by_id('save_contact').click()

        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[-1].text,
            'New contact ( edit )')

    def test_delete_contact(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))

        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys(
            'delete@example.com')
        self.selenium.find_element_by_id('id_confirm_email').send_keys(
            'delete@example.com')
        self.selenium.find_element_by_id('save_contact').click()

        self.selenium.find_element_by_link_text('edit').click()
        self.selenium.find_element_by_link_text('Delete').click()
        self.selenium.find_element_by_id('yes_delete').click()

        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact'),
            [])

    def test_detail_contact(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))

        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys(
            'detail@example.com')
        self.selenium.find_element_by_id('id_confirm_email').send_keys(
            'detail@example.com')
        self.selenium.find_element_by_id('save_contact').click()

        self.selenium.find_element_by_link_text('test contact').click()

        self.assertEquals(
            self.selenium.find_element_by_id('contact_email').text,
            'detail@example.com')


class ContactTests(TestCase):
    """ Contact model tests. """

    def test_str(self):

        contact = Contact(first_name='John', last_name='Smith')

        self.assertEquals(
            str(contact),
            'John Smith')


class ContactFormsTests(TestCase):

    def test_email_confirm(self):

        vals = {
            'first_name': 'foo',
            'last_name': 'bar',
            'email': 'test@example.com',
            'confirm_email': 'test@example.com'}

        form = ContactForm(vals)
        form.is_valid()
        form.clean()

    def test_confirm_email_fail(self):

        vals = {
            'first_name': 'foo',
            'last_name': 'bar',
            'email': 'test@example.com',
            'confirm_email': 'doesNotMatch@example.com'}

        form = ContactForm(vals)
        form.is_valid()

        self.assertRaises(
            ValidationError,
            form.clean)

    def test_post_contact_good_email(self):

        c = Client()

        vals = {
            'first_name': 'foo',
            'last_name': 'bar',
            'email': 'test@example.com',
            'confirm_email': 'test@example.com'}

        response = c.post('/new', vals)

        contact = Contact.objects.get(pk=1)

        self.assertTrue(
            contact,
            "foo bar")

    def test_post_contact_bad_email(self):

        c = Client()

        vals = {
            'first_name': 'foo',
            'last_name': 'bar',
            'email': 'test@example.com',
            'confirm_email': 'doesNotMatch@example.com'}

        response = c.post('/new', vals)

        self.assertRaises(
            ObjectDoesNotExist,
            Contact.objects.get,
            pk=1)


class ContactListViewTests(TestCase):
    """
    Contact list view tests.
    """

    def test_contacts_in_the_context(self):

        client = Client()
        response = client.get('/')

        self.assertEquals(
            list(response.context['object_list']),
            [])

        Contact.objects.create(
            first_name='foo',
            last_name='bar')
        response = client.get('/')
        self.assertEquals(
            response.context['object_list'].count(),
            1)

    def test_contacts_in_the_context_request_factory(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = ListContactView.as_view()(request)

        self.assertEquals(
            list(response.context_data['object_list']),
            [])

        Contact.objects.create(
            first_name='foo',
            last_name='bar')
        response = ListContactView.as_view()(request)
        self.assertEquals(
            response.context_data['object_list'].count(),
            1)
