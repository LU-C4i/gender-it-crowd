/*
 * Use the DataProxy.post / DataProxy.jsonPost methods. This will ensure the savedData event gets triggered.
 */
var DataProxy = function () {
    $.ajax({ cache: false });

    this.save_gender = function(gender, id, callback, error_callback) {
        var data = {};
        data.gender = gender;
        data.id = id;

        var url = '/api/gender/save';
        this.jsonPost({
            url: url,
            type: 'POST',
            data: data,
            success: function (data) {
                callback(data);
            },
            error: error_callback
        });
    };

    this.get_next_twitter_user = function(callback, error_callback) {
        var url = '/api/twitter_user/get';
        this.jsonPost({
            url: url,
            type: 'GET',
            success: function (data) {
                callback(data);
            },
            error: function(err) {
                error_callback(err);
            }
        });
    };

    this.get_leaderboard = function(callback, error_callback) {
        var url = '/api/leaderboard/get';
        this.jsonPost({
            url: url,
            type: 'GET',
            success: callback,
            error: error_callback
        });
    };

    this.jsonPost = function (cfg) {
        console.log(cfg.url);
        cfg.data = $.toJSON(cfg.data);
        cfg.contentType = 'application/json';
        cfg.cache = false;
        cfg.processData = false;

        // Default to post, but also allow this method to create delete and update requests.
        if (cfg.type === undefined)
            cfg.type = 'POST';

        $.ajax(cfg);
    };
};

var Proxy = new DataProxy();

//Get leaderboard
function createLeaderboard() {
    Proxy.get_leaderboard(function (data) {
            console.log("get_leaderboard:");
            console.log(data);

            if (data.leaderboard === undefined) return;
            if (data.leaderboard.length == 0) return;

            var topN = 10;

            $("#leaderboard").remove();

            var leaderboardDiv = $('#js-leaderboard');
            leaderboardDiv.html('');
            var table = $("<table></table>").html("<h3>Leaderboard</h3>").appendTo(leaderboardDiv);

            for (var i = 0; i < topN; ++i) {
                if (data.leaderboard.length <= i) break;
                table.append($("<tr>")
                    .append($("<td id='user-name'>").html(data.leaderboard[i].usr_login))
                    .append($("<td>").html(data.leaderboard[i].score)));
            }
        },
        function (err) {
            console.error("ERROR : " + err);
        });
}


//sidebar
$(document).ready(function()
{
  var easing = 1; //enable or disable easing | 0 or 1
  var easing_effect = 'easeOutBounce';
  var animation_speed = 500; //ms

  var slider_width = $('#sidebar').width();//get width automatically
  $('#btnSidebar').click(function()
  {
    //check if slider is collapsed
    var is_collapsed = $(this).css("margin-right") == slider_width+"px" && !$(this).is(':animated');

    //minus margin or positive margin
    var sign = (is_collapsed) ? '-' : '+';

      if(!$(this).is(':animated')) //prevent double margin on double click
      {
        if(easing) $('.willSlide').animate({"margin-right": sign+'='+slider_width},animation_speed,easing_effect);
        else $('.willSlide').animate({"margin-right": sign+'='+slider_width},animation_speed);
      }
     //if you need you can add class when expanded
      (is_collapsed) ? $('.willSlide').removeClass('expanded') : $('.willSlide').addClass('expanded');

  });
 });