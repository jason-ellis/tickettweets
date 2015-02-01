$(document).ready(function() {

    // Respects debugging in JS
    var debug = false;
    if($('#debug').data('debug') == 'True') {
        debug = true;
        console.log('Debugging is enabled');
    }

    // Event for clicking the update button.
    // Submits cursor to _new_tweets and receives new tweet objects
    $(function () {
        $('a#update').bind('click', function () {
            $.getJSON($SCRIPT_ROOT + '/_new_tweets',
                {cursor: getCursor()},
                function(new_tweets) {
                    if(debug) {
                        logNewTweets(new_tweets);
                    }
                    updateStream(new_tweets, 'new');
                });
            return false;
        });
    });

    // Event for clicking the older tweets button.
    // Submits cursor to _more_tweets and receives older tweet objects
    $(function () {
        $('a#more_tweets').bind('click', function () {
            $.getJSON($SCRIPT_ROOT + '/_more_tweets',
                {last_tweet_id: getOldest()},
                function(old_tweets) {
                    if(debug) {
                        logNewTweets(old_tweets);
                    }
                    updateStream(old_tweets, 'old');
                });
            return false;
        });
    });

    function logNewTweets(tweets) {
        console.log(tweets.length + ' tweets returned');
                    console.log('new_tweets: ');
                    console.log(tweets);
    }

    // Fetches data-tweet of each tweet and returns the highest value as cursor
    function getCursor() {
        var tweetIds = [];
        $.each($('.tweet'), function(tweet) {
            tweetIds.push($(this).attr('data-tweet'));
        });
        tweetIds.sort(function(a, b) {return a-b});
        if(debug) {
            console.log('Tweet IDs on page: ' + tweetIds);
        }
        var cursor = tweetIds.pop();
        if(debug) {
            console.log('Cursor popped and sent: ' + cursor);
        }
        return cursor;
    }

    // Fetches data-tweet of each tweet and returns the lowest value
    function getOldest() {
        var tweetIds = [];
        $.each($('.tweet'), function(tweet) {
            tweetIds.push($(this).attr('data-tweet'));
        });
        tweetIds.sort(function(a, b) {return b-a});
        if(debug) {
            console.log('Tweet IDs on page: ' + tweetIds);
        }
        var oldestTweet = tweetIds.pop();
        if(debug) {
            console.log('Oldest tweet popped and sent: ' + oldestTweet);
        }
        return oldestTweet;
    }

    getCursor();

    // Add new tweets to DOM
    function updateStream(newTweets, age) {
        var sortedTweets = newTweets.sort(function(a,b) {
            return parseInt(a['_id']) - parseInt(b['_id'])
        });
        var addedTweets = [];
        $.each(sortedTweets, function(k, v) {
            addedTweets.push(v['_id']);
            if(age=='new') {
                $('#tweet_container').prepend(formatTweet(v));
            } else if(age=='old') {
                $('#tweet_container').append(formatTweet(v));
            }
        });
        if(debug) {
            console.log('Added these new tweets: ' + addedTweets);
        }
    }

    // Create link to profile
    function linkProfile(id) {
        return "https://twitter.com/intent/follow?user_id=" + id + "/"
    }

    // Create link to status
    function linkStatus(id, statusId) {
        return "http://twitter.com/" + id + "/status/" + statusId + "/"
    }

    // format individual tweet for output to the DOM
    function formatTweet(tweet) {
        var tweetId = tweet['id_str'];
        var userId = tweet['user']['id_str'];
        var profileImageUrl = tweet['user']['profile_image_url'];
        var userName = tweet['user']['name'];
        var screenName = tweet['user']['screen_name'];
        var tweetText = tweet['text'];

        return '<div class="tweet" data-tweet="' + tweetId + '">' +
            '<a href="' + linkProfile(userId) + '" target="_blank">' +
            '<img class="profile_img" src="' + profileImageUrl + '" alt="profile image">' +
            '<span class="user_name">' + userName + '</span><br>' +
            '<span class="screen_name">@' + screenName + '</span></a><br>' +
            '<div class="tweet_text">' + tweetText + '</div>' +
                '<a href="' + linkStatus(screenName,tweetId) + '" target="_blank">Link to tweet</a>' +
            '</div>';
    }

    // Process media entities for a tweet
    function formatTweetText(tweet) {
        var tweetText = tweet['text']
    }
});