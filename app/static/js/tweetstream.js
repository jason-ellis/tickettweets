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
            $.get($SCRIPT_ROOT + '/_new_tweets',
                {cursor: getCursor()},
                function(new_tweets) {
                    $('#tweet_container').prepend(new_tweets);
                    flask_moment_render_all();
                });
            $('html,body').animate({ scrollTop: 0 }, 'slow');
            return false;
            })
        });

    // Event for clicking the older tweets button.
    // Submits cursor to _more_tweets and receives older tweet objects
    $(function () {
        $('a#more_tweets').bind('click', function () {
            $.get($SCRIPT_ROOT + '/_more_tweets',
                {last_tweet_id: getOldest()},
                function(old_tweets) {
                    $('#tweet_container').append(old_tweets);
                    flask_moment_render_all();
                });
            return false;
        });
    });

    // Fetches data-tweet of each tweet and returns the highest value as cursor
    function getCursor() {
        if(debug) {
            var tweetIds = [];
            $.each($('.tweet'), function(tweet) {
                tweetIds.push($(this).attr('data-tweet'));
            });
            tweetIds.sort(function(a, b) {return a-b});
            console.log('Tweet IDs on page: ' + tweetIds);
            console.log('Cursor should be: ' + tweetIds.pop());
        }
        var cursor = $('.tweet').first().attr('data-tweet');
        if(debug) {
            console.log('Cursor sent: ' + cursor);
        }
        return cursor;
    }

    // Fetches data-tweet of each tweet and returns the lowest value
    function getOldest() {
        if(debug) {
            var tweetIds = [];
            $.each($('.tweet'), function(tweet) {
                tweetIds.push($(this).attr('data-tweet'));
            });
            tweetIds.sort(function(a, b) {return b-a});
            console.log('Tweet IDs on page: ' + tweetIds);
            console.log('Oldest should be: ' + tweetIds.pop());
        }
        var oldestTweet = $('.tweet').last().attr('data-tweet');
        if(debug) {
            console.log('Oldest sent: ' + oldestTweet);
        }
        return oldestTweet;
    }
});