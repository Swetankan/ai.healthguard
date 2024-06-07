// Get the input and options container
const searchInput = document.getElementById('searchInput');
const selectedOptionsContainer = document.getElementById('selectedOptions');
const optionsContainer = document.getElementById('optionsContainer');
const options = document.querySelectorAll('.option');

// Add event listener for input
searchInput.addEventListener('input', function() {
    const searchValue = this.value.toLowerCase();
    options.forEach(option => {
        const text = option.textContent.toLowerCase();
        if (text.includes(searchValue)) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
    optionsContainer.style.display = 'block';
});

// Add event listener for option click
options.forEach(option => {
    option.addEventListener('click', function() {
        this.classList.toggle('selected');
        updateSelectedOptions();
    });
});

// Function to update selected options
function updateSelectedOptions() {
    selectedOptionsContainer.innerHTML = '';
    const selected = document.querySelectorAll('.option.selected');
    selected.forEach(option => {
        const selectedOption = document.createElement('div');
        selectedOption.classList.add('selected-option');
        selectedOption.textContent = option.textContent;
        const removeButton = document.createElement('button');
        removeButton.classList.add('remove-option');
        removeButton.textContent = 'x';
        removeButton.addEventListener('click', function() {
            option.classList.remove('selected');
            updateSelectedOptions();
        });
        selectedOption.appendChild(removeButton);
        selectedOptionsContainer.appendChild(selectedOption);
    });
    searchInput.value = ''; // Clear the typed value
}

// Hide options container when clicking outside
document.addEventListener('click', function(event) {
    if (!searchInput.contains(event.target)) {
        optionsContainer.style.display = 'none';
    }
});
