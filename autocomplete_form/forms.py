import django.forms


def find_instance(filter_method, data_dict):
    """Search the database for an instance with the data given.

    If one exists, return that model instance. Otherwise return ``None``.

    :type  filter_method: callable
    :param filter_method: A Django ORM ``filter`` method. This can be found on
                          querysets and on model managers, e.g.
                          ``models.Blog.objects.filter``


    :type  data_dict: dict
    :param data_dict: Values for fields that the instance should have.

    :raises: ``AssertionError`` if multiple matching instances were found.

    """
    other_instances = filter_method(**data_dict)
    if other_instances:
        assert len(other_instances) == 1
        return other_instances[0]


def try_get_cleaned_data(form_inst):
    """Try to get ``cleaned_data``; return None on failure.

    ..warning:: Dictionaries returned by this function may not be complete, if
                the form is invalid. It is not heavily tested.

    """
    # is_valid() creates the dict; it may fail for database integrity
    # reasons but if so then it will still create the cleaned_data dict.
    try:
        form_inst.is_valid()
    except Exception:
        pass

    return getattr(form_inst, 'cleaned_data', None)


class AutocompletedForm(django.forms.ModelForm):
    """A ModelForm that checks for a similar instance before saving.

    If an instance already exists that would be equivalent to what this form
    would save, then this form doesn't save and uses the already existing
    instance instead.

    """

    def validate_unique(self):
        """Override and disable uniqueness validation."""
        pass

    def save(self, *args, **kwargs):
        """Save a new object if a similar object doesn't already exist."""
        cleaned_data = try_get_cleaned_data(self)
        instance = None
        if cleaned_data:
            instance = find_instance(self.Meta.model.objects.filter,
                                     cleaned_data)
        if instance is None:
            super_method = super(AutocompletedForm, self).save
            instance = super_method(*args, **kwargs)

        return instance
