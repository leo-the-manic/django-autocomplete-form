"""Tests for the autocomplete functionality."""
import unittest
from unittest import mock

import django.forms

from . import forms


class TryGetCleanedDataTest(unittest.TestCase):
    """Tests for the autocomplete functions."""

    def test_get_clean_data_by_using_is_valid(self):
        """try_get_clean_data() uses a form's is_valid() method."""
        mock_form = mock.MagicMock(spec=django.forms.ModelForm)

        def is_valid():
            mock_form.cleaned_data = 'stuff'
        mock_form.is_valid.side_effect = is_valid

        self.assertEqual(forms.try_get_cleaned_data(mock_form), 'stuff')
        mock_form.is_valid.assert_called_once_with()

    def test_get_cleaneddata_on_exception(self):
        """Even if form.is_valid() raises an exception, get cleaned data."""
        form_inst = mock.MagicMock(spec=django.forms.ModelForm)

        def is_valid():
            form_inst.cleaned_data = 'stuff'
            raise Exception
        form_inst.is_valid.side_effect = is_valid

        self.assertEqual(forms.try_get_cleaned_data(form_inst), 'stuff')
        form_inst.is_valid.assert_called_once_with()

    def test_get_cleaneddata_fails_returning_none(self):
        """If try_get_cleaned_data fails, it returns None."""
        form_inst = mock.MagicMock(spec=django.forms.ModelForm)
        del form_inst.cleaned_data
        self.assertIsNone(forms.try_get_cleaned_data(form_inst))
        form_inst.is_valid.assert_called_once_with()


class FindInstanceTest(unittest.TestCase):
    """Tests for the find_instance function."""

    def test_sends_params(self):
        """find_instance sends its fields to the DB."""
        filter_func = mock.MagicMock(return_value=[])
        data = {'a': 'b'}
        forms.find_instance(filter_func, data)
        filter_func.assert_called_with(**data)

    def test_explodes_with_multiple_objects(self):
        """Raise an AssertError if many instances are found."""
        filter_func = mock.MagicMock(return_value=['a', 'b'])
        self.assertRaises(AssertionError, forms.find_instance, filter_func, {})

    def test_unpacks_object_on_successful_find(self):
        """If an object is found, return it (and not its container)."""
        filter_func = mock.MagicMock(return_value=['a'])
        self.assertEqual(forms.find_instance(filter_func, {}), 'a')

    def test_returns_none_on_failed_find(self):
        """If no matching objects are found, return None."""
        filter_func = mock.MagicMock(return_value=None)
        self.assertEqual(forms.find_instance(filter_func, {}), None)
