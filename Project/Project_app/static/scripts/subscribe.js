function subscribe(){
    $('#subscribe_btn').click(function(){
        $.ajax($('#subscribe_btn').data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    'success': function(data){
                        document.getElementById('subscribe_btn').innerHTML = data['follow'];
                        document.getElementById('followers').innerHTML = data['followers'];
                    }
            })
        })
    }
    $(document).ready(function(){
        subscribe()
    })


