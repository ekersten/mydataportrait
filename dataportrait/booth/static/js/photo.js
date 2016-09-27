(function($) {
    $('.yes_no.yes').on('click', function() {
        $('.yes_no_actions').hide();
        $('.isthisyou').hide();
        $('.social_login').show().removeClass('hidden');
    });
})(jQuery);