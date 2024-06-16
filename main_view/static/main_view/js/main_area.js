
document.addEventListener('DOMContentLoaded', function() {

    async function add_comment_to_db (post_id, comment_text) {
        try {
            const response = await fetch(`/add_comment_to_db/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
                },
                body: new URLSearchParams({
                    'post_id': post_id,
                    'comment_text': comment_text
                })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();

            return data

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    // makes the publish button visible and invisible if the area with comment is filled
    function updatePublishCommentButton () {
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

        add_comment_buttons.forEach((button, index) => {
            button.addEventListener('click', () => {
                let comment = comments[index];

                // has the following pattern publish-comment-button-1
                const post_id = button.id.slice(23);
                //add_comment_to_db(post_id, comment.value);

                comment.value = '';
            })
        })
    }
    // add anitial eventListener to publish comment button
    updatePublishCommentButton();


    // to fetch the post comments to load
    async function fetchCommentsById(itemId) {
        try {
            const response = await fetch(`/get-comments/?id=${itemId}`);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();

            return data

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    function renderPostComments(comments_for_post) {
        let post_comments = '';

        comments_for_post.forEach((comment) => {
            post_comments += `
                <div class='single-comment'>
                    <img class='user-profile-picture' src="${comment.profile_picture}">
                    <div class='general-comment-container'>
                        <div class='nickanme-comment-container'>
                            <p class='user-comment'><span class='user-nickname'>${comment.nickname}</span> ${comment.comment}</p>
                        </div>
                        <div class='comment-description'>
                            <p class='comment-publish-time'>${comment.post_time}</p>
                            <p class='comment-likes-counter'>Liked ${comment.comment_likes} ${comment.comment_likes == 1 ? 'time' : 'times'}</p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        return post_comments;
    }

    function renderPostCommentsContainer(comments_for_post, element_id) {
        let post_comments = renderPostComments(comments_for_post);

        const profile_picture = document.getElementById(`profile1-image-${element_id}`).src;
        const user_name = document.getElementById(`user-name-${element_id}`).textContent;
        const post_image = document.getElementById(`post-image1-${element_id}`).src;
        const post_description = document.getElementById(`post-description-${element_id}`).dataset.fullDescription;
        const post_hashtags = document.getElementById(`post-hashtags-${element_id}`).textContent;

        let comment_innerHTML = `
            <div class='post-image-container'>
                <img class='post-image' src='${post_image}'>
            </div>
            <div class='comments-section-container'>
                <div class='user-profile-container-upper'>
                    <img class='user-profile-picture' src='${profile_picture}'>
                    <p class='user-nickname'>${user_name}</p>
                </div>
        
                <div id='general-comments-container-${element_id}' class='general-comments-container'>
                    <div class='user-post-description'>
                        <div class='user-profile-container-under'>
                            <img class='user-profile-picture' src='${profile_picture}'>
                            <p class='post-description'> <span class='user-nickname'>${user_name}</span> ${post_description}</p>
                        </div>
                        <div class='general-info'>
                            <div class='post-tags'>
                                <p class='single-post-tag'>${post_hashtags}</p>
                            </div>
                            <p class='publish-time'>
                                2 days ago
                            </p>
                        </div>
                    </div>
        
                    <div class='comments-container'>
                        ${post_comments}
                    </div>
                </div>
        
                <div class='under-comments-section'>
                    <div class='like-comment-share-container'>
                        <div class="like-share-comment-container">
                            <div class="underpost-image-container">
                                <img class='like' src="static/main_view/images/like.svg">
                            </div>
                            <div class="underpost-image-container">
                                <img class='comment' src="static/main_view/images/comment.svg">
                            </div>
                            <div class="underpost-image-container">
                                <img class='share' src="static/main_view/images/share.svg">
                            </div>
                        </div>
                        <div class="underpost-image-container">
                            <img class='save' src="static/main_view/images/bookmark.svg">
                        </div>
                    </div>
        
                    <div class='likes-publish-time-container'>
                        <p class='post-likes-counter'>1 234 Likes</p>
                        <p class='post-publish-time'>2 days ago</p>
                    </div>
        
                    <div class='publish-comment-container'>
                        <textarea class="add-comment" placeholder="Add comment..."></textarea>
                        <p id='publish-comment-button-${element_id}' class="publish-comment-button">Publish</p>
                    </div>
                </div>
            </div>
        `;

        return comment_innerHTML;
    }

    function updateScrollComments() {
        let comment_list_view = document.querySelector('.general-comments-container');
        comment_list_view.addEventListener('scroll', async () => {
            
            // it has following pattern general-comments-container-1
            let commets_container_id = comment_list_view.id.slice(27);
    
            const new_comments_for_post = await fetchCommentsById(commets_container_id);
    
            if (comment_list_view.scrollTop + comment_list_view.clientHeight >= comment_list_view.scrollHeight) {
                console.log('scrolls bottom');
                comment_list_view.innerHTML += renderPostComments(new_comments_for_post);
            }
        });
    }

    function generatePostComments(elements) {
        elements.forEach((element) => {

            // it has the following pattern post-index-1
            const element_id = element.id.slice(11);

            element.addEventListener('click', async () => {
                const comments_for_post = await fetchCommentsById(element_id);
                

                const comment = document.getElementById('post-comments');
                comment.innerHTML = renderPostCommentsContainer(comments_for_post, element_id);

                // it is a need, because while rendering new html it loses onscroll
                updateScrollComments();
                // it is a need, because while rendering new html it loses onclick
                updatePublishCommentButton();

                comment.style.display = 'flex';
                document.body.classList.add("popup-opened");
            });
        });
    }
    generatePostComments(document.querySelectorAll('.comment'));
    generatePostComments(document.querySelectorAll('.show-comments-text'));

});

document.addEventListener('mouseup', function(e) {
    let container = document.getElementById('post-comments');
    if (!container.contains(e.target)) {
        container.style.display = 'none';
        document.body.classList.remove("popup-opened"); // Remove class to remove the dark overlay
    }
});
