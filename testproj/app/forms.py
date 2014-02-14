"""Forms for the test models.

:class:`TitleForm`` is the *main* form, and :class:`PublisherForm` is the
autocompletable subform.

"""
import django.forms

from . import models


class PublisherForm(django.forms.ModelForm):
    """An autocompletable form to fill out a publisher.

    When rendered, the desired effect is that certain fields will launch
    queries and autosuggest completions. If the user picks a completion, the
    rest of the fields also get auto-filled, allowing the user to easily:

    - choose an existing publisher

    - create a new publisher

    """

    class Meta:

        model = models.Publisher


class TitleForm(django.forms.ModelForm):
    """A normal, non-autocompleting form for :class:`.Title` objects."""

    class Meta:

        model = models.Title
