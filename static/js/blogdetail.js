var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method){
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend:function(xhr,settings){
                if(!csrfSafeMethod(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken",csrftoken);
                }
            }
        });
function exeClickEvent(){
    $(".like").click(function(e){
        e.preventDefault();
        $.post('{% url "like" %}',
            {
                id:$(this).data('id'),
                action:$(this).data('action'),
            },
            function(data){
                if(data['status']='ok'){
                    var preaction = $("#likeid").data('action');
                    $("#likeid").data('action',preaction == 'like'?'unlike':'like');
                    $("#likeNum").text( data['likeNum']);

                }
            }
        );
    });

}

/*
$(document).ready(function(){
            $(".like").click(function(e){
                e.preventDefault();
                $.post('{% url "like" %}',
                        {
                            id:$(this).data('id'),
                            action:$(this).data('action'),
                        },
                        function(data){
                            if(data['status']='ok'){
                                var preaction = $("#likeid").data('action');
                                $("#likeid").data('action',preaction == 'like'?'unlike':'like');
                                $("#likeNum").text( data['likeNum']);

                            }
                        }
                    );
            });
        })*/