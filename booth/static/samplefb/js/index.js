/*global createjs, jQuery, console*/
(function ($) {
    'use strict';

    var $enter_code = $('#enter_code'),
        $confirmation = $('#confirmation'),
        $confirmation_actions = $confirmation.find('.actions'),
        $confirmation_login = $confirmation.find('.social_login');



    function resetApp() {
        $confirmation_login.hide();
        $confirmation_actions.hide();
        $confirmation.hide();
        $enter_code.show();
        $enter_code.find('form')[0].reset();
    }

    resetApp();

    $enter_code.find('form').on('submit', function(e) {
        var code = $('#code').val();
        $.ajax($(this).attr('action'), {
            method: 'post',
            data: $(this).serialize(),
            success: function(data) {
                if (data.valid === true) {
                    $enter_code.hide();
                    $confirmation.show();
                    $confirmation.find('img').attr('src', data.url);
                    $confirmation_actions.show();
                }
            },
            error: function (xqr, status, error) {
                console.error(status, error);
            }
        });
        return false;
    });

    $confirmation_actions.find('.no').on('click', function(e) {
        resetApp()
    });

    $confirmation_actions.find('.yes').on('click', function(e) {
        $confirmation_actions.hide();
        $confirmation_login.find('a').each(function (index, item) {
            $(this).attr('href', $(this).attr('href') + '?next=/photo/' + $('#code').val());
        });
        $confirmation_login.show();
    });

    /*var canvas = document.getElementById('image_canvas'),
        stage = new createjs.Stage(canvas),
        pictures = [],
        totalImages = 0,
        imageCount = 0;

    $.ajax('get_media', {
        success: function(data) {
            var i;
            totalImages = data.media.length;
            for (i = 0; i < totalImages; i++) {
                pictures[i] = new Image();
                pictures[i].onload = imageLoaded;
                pictures[i].src = data.media[i].url;
            }
        },
        error: function (xqr, status, error) {
            console.error(status, error);
        }
    });

    function imageLoaded() {
        imageCount++;
        if (imageCount >= totalImages) {
            createBitmaps();
        }
    }

    function createBitmaps() {
        var bitmap, i;
        for (i = 0; i < totalImages; i++) {
            bitmap = new createjs.Bitmap(pictures[i]);
            bitmap.x = 100 * i;
            bitmap.y = canvas.height / 2 - 75;
            bitmap.rotation = 45 * Math.random() | 0;
            stage.addChild(bitmap);
        }

        stage.update();
    }*/

}(jQuery));