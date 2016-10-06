(function($) {
    $('.yes_no.yes').on('click', function() {
        $('.yes_no_actions').hide();
        $('.isthisyou').hide();
        $('.social_login').show().removeClass('hidden');
    });

    $('.yes_no.no').on('click', function() {
        $('.yes_no_actions').hide();
        $('.isthisyou').hide();
        $('.is_not_me').show().removeClass('hidden');
    });

    $(window).on('resize', resizeLayers);

    function resizeLayers() {
        $('.layers').height($('.layers').width());
    }

    resizeLayers();
})(jQuery);