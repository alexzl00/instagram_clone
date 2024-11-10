import {closeCommentsPopUp, openPostComments} from '/static/main_view/js/main_area.js';

document.addEventListener("DOMContentLoaded", function() {
    const postsContainer = document.querySelector('.posts');

    for (let user_data of Object.values(initial_posts)) {
        for (let post of Object.values(user_data.posts)) {
            const postElement = document.createElement('div');
            postElement.className = 'post-container';
            postElement.dataset.postId = post.id;
            postElement.dataset.userId = user_data.user.id;

            const imageElement = document.createElement('img');
            imageElement.src = post.post_image_path;
            imageElement.className = 'post-image-in-profile'

            imageElement.onerror = () => {
                console.error('Failed to load image:', post.post_image_path);
            };

            postElement.appendChild(imageElement);

            postsContainer.appendChild(postElement);
        }
    };

    document.querySelectorAll('.post-container').forEach((element, index) => {
        const post_id = element.dataset.postId;
        const user_id = element.dataset.userId;
        openPostComments(element, post_id, user_id);
        
    })

    closeCommentsPopUp();

    // Render the initial posts
    // renderPosts(initial_posts); leah PIDOR
});

// console.log(posts);
// for (let user_posts of Object.values(posts)) {
//     for (let post of Object.values(user_posts)) {
//         const postElement = document.createElement('div');
//         postElement.className = 'post-container';

//         const imageElement = document.createElement('img');
//         imageElement.src = post.post_image_path;
//         imageElement.className = 'post-image'

//         postElement.appendChild(imageElement);

//         postsContainer.appendChild(postElement);
//     }
// };
// }