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

    // Toggle expanding and contracting tweets on click
    $('div.tweet').click(function(e) {
        console.log(e.target.nodeName);
        if(!$(e.target).is('.tweet a, ' +
            'a>div, ' +
            '.tweet i, ' +
            '.tweet span')) {
            $(this).find('.actions').toggle('fast');
        }
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

    // Twitter web intent JS from https://dev.twitter.com/web/intents
    (function() {
      if (window.__twitterIntentHandler) return;
      var intentRegex = /twitter\.com(\:\d{2,4})?\/intent\/(\w+)/,
          windowOptions = 'scrollbars=yes,resizable=yes,toolbar=no,location=yes',
          width = 550,
          height = 420,
          winHeight = screen.height,
          winWidth = screen.width;

      // Regex for status links to open statuses in sized window
      var replyRegex = /twitter\.com?\/(\w+)?\/(status)\/(\w+)/,
          replyWidth = 700,
          replyHeight = 500;

      function handleIntent(e) {
        e = e || window.event;
        var target = e.target || e.srcElement,
            m, r, left, top;

        while (target && target.nodeName.toLowerCase() !== 'a') {
          target = target.parentNode;
        }

        if (target && target.nodeName.toLowerCase() === 'a' && target.href) {
          m = target.href.match(intentRegex);
          r = target.href.match(replyRegex);
          if (m || r) {
            if(m) {
              left = Math.round((winWidth / 2) - (width / 2));
              top = 0;

              if (winHeight > height) {
                top = Math.round((winHeight / 2) - (height / 2));
              }

              window.open(target.href, 'intent', windowOptions + ',width=' + width +
                ',height=' + height + ',left=' + left + ',top=' + top);
                console.log(target.href, 'intent', windowOptions + ',width=' + width +
                ',height=' + height + ',left=' + left + ',top=' + top)
            } else if(r) {
              left = Math.round((winWidth / 2) - (replyWidth / 2));
              top = 0;

              if (winHeight > replyHeight) {
                top = Math.round((winHeight / 2) - (replyHeight / 2));
              }

              window.open(target.href, 'reply', windowOptions + ',width=' +
                replyWidth + ',height=' + replyHeight + ',left=' + left +
                ',top=' + top);
                console.log(target.href, 'reply', windowOptions + ',width=' +
                replyWidth + ',height=' + replyHeight + ',left=' + left +
                ',top=' + top);
            }
            e.returnValue = false;
            e.preventDefault && e.preventDefault();
          }
        }
      }

      if (document.addEventListener) {
        document.addEventListener('click', handleIntent, false);
      } else if (document.attachEvent) {
        document.attachEvent('onclick', handleIntent);
      }
      window.__twitterIntentHandler = true;
    }());
});