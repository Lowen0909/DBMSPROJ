$(document).ready(function () {
    function showfavparkinglot(data){
        var table=$('#show');
        table.empty();
        if(data.length!=0){
          table.append('<tr><td>名稱</td><td>描述</td><td>地址</td><td>收費</td><td>所在城市</td>');
          for (var i=0;i<data.length;i++){
          str='<tr class="respd"><td>'+data[i]["parklot_name"]+'</td><td>'+data[i]["descrip"]+'</td><td>'+data[i]["address"]+'</td><td>'+data[i]["fare"]+'</td><td>'+data[i]["city"]+'</td>'
          str=str+'<td><input type="button" value="刪除" class="del" data-id="'+data[i]["parklot_id"]+'" data-citycode="'+data[i]["citycode"]+'"></td>';
          str=str+'<td><input type="button" value="查看" class="search" data-id="'+data[i]["parklot_id"]+'" data-citycode="'+data[i]["citycode"]+'" data-name="'+data[i]["parklot_name"]+'"></td></tr>';
          table.append(str);
          }
        }else{
          var str="<h1 align='center'>尚無資料</h1>";
          table.append(str);
        }
     
    }
    function showfavparkingseg(data){
        var table=$('#show');
        table.empty();
        if(data.length!=0){
          table.append('<tr><td>名稱</td><td>描述</td><td>收費</td><td>所在城市</tr>');
          for (var i=0;i<data.length;i++){
          str='<tr class="respd"><td>'+data[i]["segmentname"]+'</td><td>'+data[i]["description"]+'</td><td>'+data[i]["fare"]+'</td><td>'+data[i]["city"]+'</td>'
          str=str+'<td><input type="button" value="刪除" class="delseg" data-id="'+data[i]["segmentID"]+'" data-citycode="'+data[i]["citycode"]+'"></td></tr>'
          table.append(str);
          }
        }else{
          var str="<h1 align='center'>尚無資料</h1>";
          table.append(str);
        }
     
     }
     function showAfavparkinglot(data){
      var table=$('#show1');
      table.empty();
      if(data.length!=0){
        table.append('<tr><td>名稱</td><td>剩餘車位</td><td>營業狀態</td><td>車位類型</td><td>所在城市</td>');
        for (var i=0;i<data.length;i++){
        str='<tr class="respd"><td>'+data[i]["名稱"]+'</td><td>'+data[i]["剩餘車位"]+'</td><td>'+data[i]["營業狀態"]+'</td><td>'+data[i]["車位類型"]+'</td><td>'+data[i]["citycode"]+'</td></tr>';
        table.append(str);
        }
      }else{
        var str="<h1 align='center'>尚無資料</h1>";
        table.append(str);
      }
     }  


    $("input#parkinglot").on('click',function(){
       console.log("hi");
       $.ajax({
           type: 'POST',
           url:  '/favorite',
           data: {"id":"None","citycode":"None",method:"select"},
           datatype:'JSON',
           success: function(data) {
             var data1=Array.from(data)
             showfavparkinglot(data1); 
             $(".del").on('click',function (){
              var id=$(this).data("id");
              var citycode=$(this).data("citycode");
              
              var button=$(this);
               //   
                 $.ajax({
                    type: 'POST',
                    url:  '/favorite',
                    data: {"id":id,"citycode":citycode,"method":"delete"},
                    datatype:'JSON',
                    success: function(data) {
                       if(data['msg']=="Fail"){
                          $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
                          $(".txt").text("無法刪除不存在資料!")
                          $('.alert').show(100).delay(1500).fadeOut('slow');
                       }else{     
                          button.closest("tr").css("display","none");
                          if ($("#show tr:visible").length==1){
                            $('#show').empty();
                            $('#show').append("<h1 align='center'>尚無資料</h1>")
                          }        
                          $(".alert").css("background-color","rgba(227, 224, 83, 0.9)");
                          $(".txt").text("刪除成功")
                          $('.alert').show(100).delay(1500).fadeOut('slow');
                       }
                    } ,
                    error:function(data){
                       $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
                       $(".txt").text("發生錯誤請稍後重試")
                       $('.alert').show(100).delay(1500).fadeOut('slow');
                    }
                  });                  
              });
            //   
            $(".search").on('click',function(){
               console.log("search");
               id=$(this).data("id");
               parkname=$(this).data("name");
               citycode=$(this).data("citycode");
               console.log(parkname);
               $.ajax({
                   type: 'POST',
                   url:  '/searchparklotapi',
                   data: {"id":id,"parkname":parkname,"citycode":citycode},
                   datatype:'JSON',
                   success: function(data) {
                     if(data['msg']=="not found"){
                        $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
                        $(".txt").text("查不到停車場!")
                        $('.alert').show(100).delay(1500).fadeOut('slow');
                     
                     }else{
                        // $(".alert").css("background-color","rgba(227, 224, 83, 0.9)");
                        // $(".txt").text("查詢成功")
                        // $('.alert').show(100).delay(1500).fadeOut('slow');
                        // console.log(data['result']);
                        var data1=Array.from(data['result']);
                        showAfavparkinglot(data1); 
                        $(".popupouter1").css("display","block");
                     }
                     
                   } ,
                   error:function(data){
                    $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
                    $(".txt").text("發生錯誤請稍後重試")
                    $('.alert').show(100).delay(1500).fadeOut('slow');
                   }
                 });
               });
               // 
           } ,
           error:function(data){
            $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
            $(".txt").text("發生錯誤請稍後重試")
            $('.alert').show(100).delay(1500).fadeOut('slow');
           }
         });
    });
    $("input#parkingseg").on('click',function(){
        console.log("hi");
        $.ajax({
            type: 'POST',
            url:  '/favorite_seg',
            data: {"id":"None","citycode":"None",method:"select"},
            datatype:'JSON',
            success: function(data) {
              var data1=Array.from(data)
              showfavparkingseg(data1); 
              $(".delseg").on('click',function (){
                var id=$(this).data("id");
                var citycode=$(this).data("citycode");
                
                var button=$(this);
                   $.ajax({
                      type: 'POST',
                      url:  '/favorite_seg',
                      data: {"id":id,"citycode":citycode,"method":"delete"},
                      datatype:'JSON',
                      success: function(data) {
                         if(data['msg']=="Fail"){
                            $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
                            $(".txt").text("無法刪除不存在資料!")
                            $('.alert').show(100).delay(1500).fadeOut('slow');
                         }else{     
                            button.closest("tr").css("display","none");   
                            if ($("#show tr:visible").length==1){
                              $('#show').empty();
                              $('#show').append("<h1 align='center'>尚無資料</h1>")
                            }     
                            $(".alert").css("background-color","rgba(227, 224, 83, 0.9)");
                            $(".txt").text("刪除成功")
                            $('.alert').show(100).delay(1500).fadeOut('slow');
                         }
                      } ,
                      error:function(data){
                         $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
                         $(".txt").text("發生錯誤請稍後重試")
                         $('.alert').show(100).delay(1500).fadeOut('slow');
                      }
                   });
                });
            } ,
            error:function(data){
              $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
              $(".txt").text("發生錯誤請稍後重試")
              $('.alert').show(100).delay(1500).fadeOut('slow');
            }
          });
     });
     
     $('.closepop').on('click',function(){
         $('.popupouter1').css('display','none');
     });
   
  
})