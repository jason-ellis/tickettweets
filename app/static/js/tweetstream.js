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
                    if(debug) {
                        console.log('New tweets: ' + new_tweets);
                    }
                    $('#tweet_container').prepend(new_tweets);
                });
            return false;
        });
    });

    // Event for clicking the older tweets button.
    // Submits cursor to _more_tweets and receives older tweet objects
    $(function () {
        $('a#more_tweets').bind('click', function () {
            $.get($SCRIPT_ROOT + '/_more_tweets',
                {last_tweet_id: getOldest()},
                function(old_tweets) {
                    if(debug) {
                        console.log('Added tweets: ' + old_tweets);
                    }
                    $('#tweet_container').append(old_tweets);
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

});