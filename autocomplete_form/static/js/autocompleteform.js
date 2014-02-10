var AutocompleteField = (function($) {

    /**
     * Set one field as a trigger for subform autocompletion
     *
     * Parameters:
     *
     * elementQuery
     *     a jQuery expression that will return the autocompleted field.
     *
     * baseAjaxURL
     *     the URL base to use for AJAX. Requests are made to
     *     `base + 'get-all/'` and `base + 'get-detail/{an_id_here}/'`
     *
     * fieldPrefix
     *     A common string in front of all fields. Note that this is also used
     *     to find the autocomplete ID input.
     *
     * fieldList
     *     A list of fields to fill with the AJAX data.
     *
     * autoAdvanceElem
     *     A jQuery expression that will be given focus once the data filling
     *     is finished. This should be the first field following all the
     *     autocompleted fields.
     */
    return {
        activate: function(elementQuery, baseAjaxURL, fieldPrefix,
                                       fieldList, autoAdvanceElem) {

            // set autocompletion
            getAllURL = baseAjaxURL + "get-all/";
            $(elementQuery).autocomplete({autoFocus: true, source: getAllURL});

            // set the handler for when they choose an autocomplete option
            $(elementQuery).bind("autocompleteselect", function(evt, ui) {

                // make another AJAX call to get the rest of the data
                getDetailURL = baseAjaxURL + 'get-detail/' + ui.item.id + '/';
                getDetailURL = baseAjaxURL + "get-detail/" + ui.item.id + "/";
                $.ajax(getDetailURL, {
                    success: function(detail_info) {
                        fieldList.forEach(function(fieldName) {
                            $field = $(fieldPrefix + fieldName);
                            $field.val(detail_info[fieldName]);
                            $field.trigger('change');
                        });
                    }
                });

                // place the user's cursor on a field after all autocompleted fields
                $(autoAdvanceElem).focus()
                evt.preventDefault()  # prevent Tab key from advancing normally
            });
        }
    }
})(jQuery);
