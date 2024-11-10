async function add_comment_to_db(post_id, comment_text, user_id) {
    try {
        const response = await fetch('/add-comment-to-db/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
            },
            body: new URLSearchParams({
                'post_id': post_id,
                'comment_text': comment_text,
                'user_id': user_id
            })
        });
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function get_logged_user() {
    try {
        const response = await fetch('/get-logged-user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
            }
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
// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// makes the publish button visible and invisible if the area with comment is filled
function updatePublishCommentButton (comments, add_comment_buttons) {
    console.log(add_comment_buttons);

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
        button.addEventListener('click', async () => {
            let comment = comments[index];
            console.log(comment.value.trim() !== '')
            if (comment.value.trim() !== '') {
                const post_id = button.dataset.index;
                let user = await get_logged_user();
                user.result.comment_text = comment.value;

                // render html with new comment
                document.querySelector('.comments-container').innerHTML += renderPostComments([user.result]);

                // set 'Publish' button to be invisible
                add_comment_buttons[index].style.display = 'none';
                
                // we need  to define user_id of user that created post to add comment to db, so we can attach data-user-id
                await add_comment_to_db(post_id, comment.value, user.result.User.id);

                // add to the storage in python to already loaded comments
                await insertCommentById(post_id, user.result.created_at, comment.value);

                comment.value = '';
            }
        })
    })
}

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

// insert comment in already loaded post in python
async function insertCommentById(post_id, post_time,  comment) {
    try {
        const response = await fetch('/insert-comment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
            },
            body: new URLSearchParams({
                'post_id': post_id,
                'post_time': post_time,
                'comment': comment
            })
        });
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

function renderPostComments(comments_for_post) {
    let post_comments = '';

    comments_for_post.forEach((comment) => {
        let comment_likes = 1;
        post_comments += `
            <li class='single-comment'>
                <img class='user-profile-picture' src="${comment.User.profile_picture_path}">
                <div class='general-comment-container'>
                    <div class='nickanme-comment-container'>
                        <p class='user-comment'><span class='user-nickname'>${comment.User.nickname}</span> ${comment.comment_text}</p>
                    </div>
                    <div class='comment-description'>
                        <p class='comment-publish-time'>${comment.created_at}</p>
                        <p class='comment-likes-counter'>Liked ${comment_likes} ${comment_likes == 1 ? 'time' : 'times'}</p>
                    </div>
                </div>
            </li>
        `;
    });
    return post_comments;
}

function renderPostCommentsContainer(comments_for_post, element_id, user_id) {
    let post_comments = renderPostComments(comments_for_post);

    // const profile_picture = document.getElementById(`profile1-image-${element_id}`).src;
    // const user_name = document.getElementById(`user-name-${element_id}`).textContent;
    // const post_image = document.getElementById(`post-image1-${element_id}`).src;
    // const post_description = user_posts_list[user_id].posts[element_id].post_description;
    // const post_time = document.getElementById(`publishing-time-${element_id}`).dataset.postTime;
    // const post_hashtags = document.getElementById(`post-hashtags-${element_id}`).textContent;
    
    const profile_picture = user_posts_list[user_id].user.profile_picture_path;
    const user_name = user_posts_list[user_id].user.name;
    const post_image = user_posts_list[user_id].posts[element_id].post_image_path;
    const post_description = user_posts_list[user_id].posts[element_id].post_description;
    const post_time = user_posts_list[user_id].posts[element_id].created_at;
    const post_hashtags = '';
    try {
        user_posts_list[user_id].posts[element_id].post_hashtags.forEach((hashtag, index) => {
            if (index === 0){
                post_hashtags += `#${hashtag}`
            }
            else {
                post_hashtags += ` #${hashtag}`
            }
        })
    } catch (TypeError) {
    }

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
                            ${post_time}
                        </p>
                    </div>
                </div>
    
                <ul class='comments-container'>
                    ${post_comments}
                </ul>
            </div>
    
            <div class='under-comments-section'>
                <div class='like-comment-share-container'>
                    <div class="like-share-comment-container">
                        <div class="underpost-image-container">
                            <img class='like' src="${staticUrl}images/like.svg">
                        </div>
                        <div class="underpost-image-container">
                            <img class='comment' src="${staticUrl}images/comment.svg">
                        </div>
                        <div class="underpost-image-container">
                            <img class='share' src="${staticUrl}images/share.svg">
                        </div>
                    </div>
                    <div class="underpost-image-container">
                        <img class='save' src="${staticUrl}images/bookmark.svg">
                    </div>
                </div>
    
                <div class='likes-publish-time-container'>
                    <p class='post-likes-counter'>1 234 Likes</p>
                    <p class='post-publish-time'>2 days ago</p>
                </div>
    
                <div class='publish-comment-container'>
                    <textarea class="add-comment add-comment-popup" placeholder="Add comment..."></textarea>
                    <p data-index='${element_id}' class="publish-comment-button publish-comment-button-popup">Publish</p>
                </div>
            </div>
        </div>
    `;

    return comment_innerHTML;
}

function updateScrollComments() {
    let comment_list_view = document.querySelector('.general-comments-container');
    comment_list_view.addEventListener('scroll', async () => {
        if (comment_list_view.scrollTop + comment_list_view.clientHeight >= comment_list_view.scrollHeight) {
            // it has following pattern general-comments-container-1
            let commets_container_id = comment_list_view.id.slice(27);
    
            const new_comments_for_post = await fetchCommentsById(commets_container_id);
            comment_list_view.innerHTML += renderPostComments(new_comments_for_post);
        }
    });
}

export function openPostComments(element, post_id, user_id){
    element.addEventListener('click', async () => {
        const comment = document.getElementById('post-comments');

        const post_comments = await fetchCommentsById(post_id);
        comment.innerHTML = renderPostCommentsContainer(post_comments, post_id, user_id);

        // it is a need, because while rendering new html it loses onscroll
        updateScrollComments();
        // it is a need, because while rendering new html it loses onclick
        updatePublishCommentButton(document.querySelectorAll('.add-comment-popup'), document.querySelectorAll('.publish-comment-button-popup'));

        comment.style.display = 'flex';
        document.body.classList.add("popup-opened");
        //comment.setAttribute('data-hidden', 'false');
        //document.querySelector('.publish-comment-button-popup')
        //comment.style.content = '';
    });
}
function generatePostComments(elements) {
    elements.forEach((element) => {

        // it has the following pattern post-index-1
        const post_id = element.id.slice(11);
        const user_id = element.dataset.userId;

        openPostComments(element, post_id, user_id);
    });
}

export function closeCommentsPopUp() {
    document.addEventListener('mouseup', function(e) {
        let container = document.getElementById('post-comments');
        if (!container.contains(e.target) && container.style.display != 'none') {
            container.style.display = 'none';
            document.body.classList.remove("popup-opened"); // Remove class to remove the dark overlay
            //container.setAttribute('data-hidden', 'true');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {

    // add anitial eventListener to publish comment button
    updatePublishCommentButton(document.querySelectorAll('.add-comment'), document.querySelectorAll('.publish-comment-button'));

    generatePostComments(document.querySelectorAll('.comment'));
    generatePostComments(document.querySelectorAll('.show-comments-text'));

    closeCommentsPopUp();
});

