$(document).ready(function() {
    $('a.abstract').click(function() {
        $(this).parent().parent().find(".abstract.hidden").toggleClass('open');
    });
    $('a.bibtex').click(function() {
        $(this).parent().parent().find(".bibtex.hidden").toggleClass('open');
    });
    $('a').removeClass('waves-effect waves-light');
});

document.addEventListener("DOMContentLoaded", function () {
    // Initialize Clipboard.js for elements with the class 'copy-bibtex'
    new ClipboardJS('.copy-bibtex', {
        text: function(trigger) {
            // Get the target element specified in data-clipboard-target
            const targetSelector = trigger.getAttribute('data-clipboard-target');
            const targetElement = document.querySelector(targetSelector);

            // Return only the text content of the target element
            return targetElement.textContent.trim();
        }
    });

    // Optional: Add feedback when the text is copied
    document.querySelectorAll('.copy-bibtex').forEach(button => {
        button.addEventListener('click', () => {
            // Provide feedback
            button.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i> Copy';
            }, 2000); // Reset after 2 seconds

            // Clear text selection
            if (window.getSelection) {
                window.getSelection().removeAllRanges();
            } else if (document.selection) {
                document.selection.empty();
            }
        });
    });
});