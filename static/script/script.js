// script.js
$(document).ready(function() {
    $('#options-list').select2({
        placeholder: 'Search/Select Options...'
    });

    $('#options-list').on('change', function() {
        updateSelectedOptions();
    });
});

function updateSelectedOptions() {
    var selectedOptions = $('#options-list').val();
    var $selectedOptionsList = $('#selected-options-list');
    $selectedOptionsList.empty();
    if (selectedOptions) {
        selectedOptions.forEach(function(option) {
            var text = $('#options-list option[value="' + option + '"]').text();
            var $item = $('<div class="selected-option">').text(text);
            var $removeButton = $('<button>')
                .text('x')
                .attr('data-value', option)
                .on('click', function() {
                    removeOption($(this).attr('data-value'));
                });
            $item.append($removeButton);
            $selectedOptionsList.append($item);
        });
    }
}

function removeOption(value) {
    var selectedOptions = $('#options-list').val();
    var index = selectedOptions.indexOf(value);
    if (index > -1) {
        selectedOptions.splice(index, 1);
        $('#options-list').val(selectedOptions).trigger('change');
    }
}

var typed = new Typed('#heading1', {
    strings: ['Smart Health Analyis', 'AI health Guard'],

    showCursor: true,
    cursorChar: '|',
    typeSpeed: 70,
    backSpeed: 50,

  });