document.addEventListener('DOMContentLoaded', function() {
    let generatedRecommendations = '';
    user_profiles_list.forEach((element) => {
        generatedRecommendations += `
            <div id='user-profile-${element.id}' class="user-profile">
                <a href="http://127.0.0.1:8000/profile">
                    <img class="user-profile-image" src=${element.profile_picture_path}>
                <a>
                <div class="user-nickname-name-container">
                    <a href="http://127.0.0.1:8000/profile">
                        <p class="user-nickname">${element.nickname}</p>
                    <a>
                    <p class="user-name">${element.name}</p>
                </div>
                <p id='subscribe_button' class="subscribe-recommendation-button">Subscribe</p>
            </div>
        `;
    });
    document.querySelector('.subscribe-recommendations').innerHTML = generatedRecommendations;
    
    document.querySelectorAll('.subscribe-recommendation-button').forEach((element) => {
        element.addEventListener('click', () => {
            if (element.textContent === 'Subscribe'){
                element.textContent = 'Subscibed';
                element.classList.add('subscribed-reccomendation-batton');
            } else {
                element.textContent = 'Subscribe';
                element.classList.remove('subscribed-reccomendation-batton');
            }
        });
    });
     
    function generatePostDescription(post, user_nickname, user_id) {
        if (post.post_description.length > 20) {
            // console.log(post.post_description);
            let text = post.post_description.slice(0, 17) + '...';
            return `<span class="user_nickname">${user_nickname}</span> ${text} <span data-user-id="${user_id}" data-post-id="${post.id}" class="extend-post-description">more</span>`
        } else {
            return `<span class="user_nickname">${user_nickname}</span> ${post.post_description}`
        }
    };
    
    let generatedPosts = '';
    for (let [user_id, element] of Object.entries(user_posts_list)) {
        const element_name = element.user.name;
        const user_nickname = element.user.nickname;
        // console.log(element.posts);
        for (let post of Object.values(element.posts)) {
            const post_id = post.id;
            const post_image = post.post_image_path;
            const post_description = post.post_description;
            let post_hashtags = '';
    
            const now = new Date();
            const targetDate = new Date(post.created_at);
    
            const diffInMilliseconds = now - targetDate;
    
            let diffTime = Math.floor(diffInMilliseconds / (1000 * 60 * 60 * 24)); // days
            let postTime = ``
            if (diffTime > 1) {
                postTime = `${diffTime} days ago`;
            } else if (diffTime === 1) {
                postTime = `1 day ago`;
            } else if (Math.floor(diffTime * 24) > 1) {
                postTime = `${diffTime * 24} hours ago`;
            } else if (Math.floor(diffTime * 24) > 1) {
                postTime = `1 hour ago`;
            } else if (Math.floor(diffTime * 24 * 60) > 1) {
                postTime = `${diffTime * 24 * 60} minutes ago`;
            } else if (Math.floor(diffTime * 24 * 60) === 1) {
                postTime = `1 minute ago`;
            } else if (Math.floor(diffTime * 24 * 60 * 60) > 1) {
                postTime = `${diffTime * 24 * 60 * 60} seconds ago`;
            } else {
                postTime = `one second ago`;
            }
    
            try {
                post.post_hashtags.forEach((hashtag, index) => {
                    if (index === 0){
                        post_hashtags += `#${hashtag}`
                    }
                    else {
                        post_hashtags += ` #${hashtag}`
                    }
                })
            } catch (TypeError) {
            }
            generatedPosts += `
                <div id='post-index-${post_id}' class="post1-container">
                    <div class="publisher1-profile">
                        <a href="http://127.0.0.1:8000/profile">
                            <img id='profile1-image-${post_id}'class="profile1-image" src=${element.user.profile_picture_path}>
                        </a>
                        <a href="http://127.0.0.1:8000/profile">
                            <p id='user-name-${post_id}' class="user1-name">${element_name}</p>
                        </a>
                        <p>&#x2022;</p>
                        <p class="publishing-time" id="publishing-time-${post_id}" data-post-time='${postTime}'>${postTime}</p>
                    </div>
                    <img id='post-image1-${post_id}' class="post-image1" src=${post_image}>
                    <div class="underpost-container">
                        <div class="like-share-comment-save-container">
                            <div class="like-share-comment-container">
                                <div class="underpost-image-container">
                                    <img class='like' src="${staticUrl}images/like.svg">
                                </div>
                                <div class="underpost-image-container">
                                    <img id='post-index-${post_id}' data-user-id="${user_id}" class='comment' src="${staticUrl}images/comment.svg">
                                </div>
                                <div class="underpost-image-container">
                                    <img class='share' src="${staticUrl}images/share.svg">
                                </div>
                            </div>
                            <div class="underpost-image-container">
                                <img class='save' src="${staticUrl}images/bookmark.svg">
                            </div>
                        </div>
                        <p class="likes-counter">224 450 Likes</p>
                        <p id='post-description-${post_id}' data-full-description='${post_description}' class="post-description">${generatePostDescription(post, user_nickname, user_id)}</p>
                        <p id='post-hashtags-${post_id}' class="post-hashtags">${post_hashtags}</p>
                        <p id='post-index-${post_id}' data-user-id="${user_id}" class="show-comments-text">Show all comments (${4})</p>
                        <div class="comment-section">
                            <textarea class="add-comment" placeholder="Add comment..."></textarea>
                            <p data-index="${post_id}" class="publish-comment-button">Publish</p>
                        </div>
                    </div>
                    <div class="line-between-posts"></div>
                </div>
            `
        }
    };

    document.querySelector('.posts-container').innerHTML = generatedPosts;
    
    // add ability to click on 'more' in the post description in order to show the whole description
    let post_descriptions = document.querySelectorAll('.post-description');
    document.querySelectorAll('.extend-post-description').forEach((element, index) => {
        const user_id = parseInt(element.dataset.userId);
        const post_id = parseInt(element.dataset.postId);
        // console.log(user_posts_list[user_id].user.nickname);
        element.addEventListener('click', () => {
            let full_description = `<span class="user_nickname">${user_posts_list[user_id].user.nickname}</span> ${user_posts_list[user_id].posts[post_id].post_description}`;
    
            post_descriptions[index].innerHTML = full_description;
        });
    });
});





