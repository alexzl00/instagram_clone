document.getElementById('uploadPostImage').addEventListener('change', function() {
    let file = this.files[0];

    if (file && file.type.startsWith('image/')) {
        let reader = new FileReader();

        reader.onload = function(e) {
            let newPostImage = document.getElementById('newPostImage');
            newPostImage.src = e.target.result;
            newPostImage.style.display = 'block';

            document.getElementById('uploadImageButton').style.display = 'none';
            document.getElementById('uploadPostImageText').style.display = 'none';
        }
        reader.readAsDataURL(file);
    }

    this.style.display = 'none'
});

document.addEventListener('mouseup', function(e) {
    let container = document.getElementById('createPostContainer');
    if (!container.contains(e.target) && container.style.display != 'none' ) {
        container.style.display = 'none';
        document.body.classList.remove("popup-opened"); // Remove class to remove the dark overlay

        let newPostImage = document.getElementById('newPostImage');
        newPostImage.src = '';
        newPostImage.style.display = 'none';

        document.getElementById('uploadImageButton').style.display = 'block';
        document.getElementById('uploadPostImageText').style.display = 'block';
        document.getElementById('addPostDescription').value = '';
        document.getElementById('addPostHashtags').value = '';
    }
});

document.getElementById('create-post-button').addEventListener('click', function() {
    document.getElementById('uploadForm').submit();
});
