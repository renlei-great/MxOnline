$('#zjg').click(function () {
    $.get('/captcha/refresh', function (data) {
        image_url = data.image_url
        key = data.key
        $('#zjg').find('img').attr('src', image_url)
        $('#zjg').find('input[name=captcha_0]').val(key)
    })
})