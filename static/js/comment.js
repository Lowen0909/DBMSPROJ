(document).ready(function () {
     $("input#com").on('click',function(){
        var id=$(this).data("id");
        var citycode=$(this).data("citycode");
        console.log("hi");
        $.ajax({
            type: 'POST',
            url:  '/comment_parklot',
            data: {"id":id,"citycode":citycode,"method":"insert"},
            datatype:'JSON',
            success: function(data) {
                console.log(data);
                alert("加入成功");
            } ,
            error:function(data){
                alert("發生錯誤，請稍後並重新嘗試");
            }
          });
     })
})

