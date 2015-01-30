$(document).ready(function() {

    // Event for clicking the update button.
    // Submits cursor to _new_tweets and receives new tweet objects
    $(function () {
        $('a#update').bind('click', function () {
            $.getJSON($SCRIPT_ROOT + '/_new_tweets',
                {cursor: getCursor()},
                function(new_tweets) {
                    console.log(new_tweets.length + ' tweets returned');
                    console.log('new_tweets: ' + new_tweets);
                    console.log(new_tweets);
                    updateStream(new_tweets);
                });
            return false;
        });
    });

    // Fetches data-tweet of each tweet and returns the highest value as cursor
    function getCursor() {
        var tweetIds = [];
        $.each($('.tweet'), function(tweet) {
            tweetIds.push($(this).attr('data-tweet'));
        });
        tweetIds.sort(sortNumber);
        console.log(tweetIds);
        var cursor = tweetIds.pop();
        console.log(cursor);
        return cursor;
    }

    // Sort the tweetIds from getCursor
    function sortNumber(a,b) {
        return a - b;
    }

    getCursor();

    // Add new tweets to DOM
    function updateStream(newTweets) {
        $.each(newTweets, function(k, v) {
            console.log(v);
            $('#tweet_container').prepend(formatTweet(v));
        })
    }

    function formatTweet(tweet) {
        var tweetId = tweet['_id'];
        var profileImageUrl = tweet['user']['profile_image_url'];
        var userName = tweet['user']['name'];
        var screenName = tweet['user']['screen_name'];
        var tweetText = tweet['text'];

        return '<div class="tweet" data-tweet="' + tweetId + '">' +
            '<img class="profile_img" src="' + profileImageUrl + '" alt="profile image">' +
            '<span class="user_name">' + userName + '</span><br>' +
            '<span class="screen_name">@' + screenName + '</span><br>' +
            '<div class="tweet_text">' + tweetText + '</div>' +
            '</div><hr>';
    }
});