function like(){
    $('#like_btn').click(function(){
        $.ajax($('#like_btn').data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    'like_id': $('#like_btn').val()
                    },
                    'success': function(data){
                        document.getElementById('like_btn').innerHTML = data['like'];
                        document.getElementById('likes').innerHTML = data['likes'];
                    }
            })
        })
    }
    $(document).ready(function(){
        like()
    })