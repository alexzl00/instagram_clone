document.addEventListener("DOMContentLoaded", function() {
    const postsContainer = document.querySelector('.posts');

    function renderPosts(posts) {
        posts.forEach(post => {
            console.log(post.img);
            const postElement = document.createElement('div');
            postElement.className = 'post-container';

            const imageElement = document.createElement('img');
            imageElement.src = post.img;
            imageElement.className = 'post-image'

            postElement.appendChild(imageElement);

            postsContainer.appendChild(postElement);
        });
    }

    // Render the initial posts
    renderPosts(initial_posts);
});