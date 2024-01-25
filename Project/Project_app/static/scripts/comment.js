function comment(){
    $('#comment_btn').click(function(){
        $.ajax($('#comment_btn').data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    'text': $('#comment').val()
                    },
                    'success': function(data){
                        document.getElementById('comments').innerHTML += data['resp'];
                    }
            })
        })
    }
    $(document).ready(function(){
        comment()
    })
