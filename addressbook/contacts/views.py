from django.views.generic import ListView

from contacts.models import Contact

# Create your views here.


class ListContactView(ListView):
    """
    View to list contacts
    """

    model = Contact
    template_name = 'contact_list.html'
