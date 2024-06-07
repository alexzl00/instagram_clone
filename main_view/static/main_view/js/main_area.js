
document.addEventListener('DOMContentLoaded', function() {
    // makes the publish button visible and invisible if the area with comment is filled
    let comments = document.querySelectorAll('.add-comment');
    let add_comment_buttons = document.querySelectorAll('.publish-comment-button');

    comments.forEach((TextInput, index) => {

        let add_comment_button = add_comment_buttons[index];

        TextInput.addEventListener('input', () => {
            if (TextInput.value.trim() !== '') {
                add_comment_button.style.display = 'block';

            } else {
                add_comment_button.style.display = 'none';

            };

        });
    });
});

