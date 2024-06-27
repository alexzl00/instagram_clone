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
     
    function generatePostDescription(element) {
        if (element.post_description.length > 20) {
            let text = element.post_description.slice(0, 17) + '...';
            return `<span class="user_nickname">${element.nickname}</span> ${text} <span class="extend-post-description">more</span>`
        } else {
            return `<span class="user_nickname">${element.nickname}</span> ${element.comment}`
        }
    };
    
    
    let generatedPosts = '';
    user_posts_list.forEach((element) => {

        generatedPosts += `
            <div id='post-index-${element.id}' class="post1-container">
                <div class="publisher1-profile">
                    <a href="http://127.0.0.1:8000/profile">
                        <img id='profile1-image-${element.id}'class="profile1-image" src=${element.profile_picture}>
                    </a>
                    <a href="http://127.0.0.1:8000/profile">
                        <p id='user-name-${element.id}' class="user1-name">${element.name}</p>
                    </a>
                    <p>&#x2022;</p>
                    <p class="publishing-time">${element.post_time}</p>
                </div>
                <img id='post-image1-${element.id}' class="post-image1" src=${element.post_image}>
                <div class="underpost-container">
                    <div class="like-share-comment-save-container">
                        <div class="like-share-comment-container">
                            <div class="underpost-image-container">
                                <img class='like' src="static/main_view/images/like.svg">
                            </div>
                            <div class="underpost-image-container">
                                <img id='post-index-${element.id}' class='comment' src="static/main_view/images/comment.svg">
                            </div>
                            <div class="underpost-image-container">
                                <img class='share' src="static/main_view/images/share.svg">
                            </div>
                        </div>
                        <div class="underpost-image-container">
                            <img class='save' src="static/main_view/images/bookmark.svg">
                        </div>
                    </div>
                    <p class="likes-counter">224 450 Likes</p>
                    <p id='post-description-${element.id}' data-full-description='${element.post_description}' class="post-description">${generatePostDescription(element)}</p>
                    <p id='post-hashtags-${element.id}' class="post-hashtags">#donutislife #lovedonut</p>
                    <p id='post-index-${element.id}' class="show-comments-text">Show all comments (${element.number_of_comments})</p>
                    <div class="comment-section">
                        <textarea class="add-comment" placeholder="Add comment..."></textarea>
                        <p id='publish-comment-button-${element.id}' class="publish-comment-button">Publish</p>
                    </div>
                </div>
                <div class="line-between-posts"></div>
            </div>
        `
    });
    document.querySelector('.posts-container').innerHTML = generatedPosts;
    
    // add ability to click on 'more' in the post description in order to show the whole description
    let post_descriptions = document.querySelectorAll('.post-description');
    document.querySelectorAll('.extend-post-description').forEach((element, index) => {
        element.addEventListener('click', () => {
            let full_description = `<span class="user_nickname">${user_posts_list[index].nickname}</span> ${user_posts_list[index].post_description}`;
    
            post_descriptions[index].innerHTML = full_description;
        });
    });
});





