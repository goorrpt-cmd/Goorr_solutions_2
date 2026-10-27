(function($) {
    $(document).ready(function() {
        function toggleExpiry(row) {
            const docType = row.find('select[name$="doc_type"]').val();
            const expiryField = row.find('input[name$="expiry_date"]').closest('.form-row');

            if (docType === "NIF" || docType === "NISS") {
                expiryField.hide();
            } else {
                expiryField.show();
            }
        }

        $('.dynamic-candidatedocument_set').each(function() {
            toggleExpiry($(this));
        });

        $(document).on('change', 'select[name$="doc_type"]', function() {
            const row = $(this).closest('.dynamic-candidatedocument_set');
            toggleExpiry(row);
        });
    });
})(django.jQuery);
