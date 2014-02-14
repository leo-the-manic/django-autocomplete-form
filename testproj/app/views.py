"""Views for the test app."""
from django.shortcuts import render

from . import forms


def hello(request):
    """Preset the demo forms."""

    message = ''
    if request.POST:
        publisher_form = forms.PublisherForm(request.POST, prefix='publisher')
        title_form = forms.TitleForm(request.POST, prefix='title')

        publisher_form.save()
        title_form.save()
        message = 'Saved!'

    context = {
        'publisher_form': forms.PublisherForm(prefix='publisher'),
        'title_form': forms.TitleForm(prefix='title'),
        'message': message,
    }

    return render(request, 'index.django.html', context)
