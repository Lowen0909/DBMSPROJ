$(document).ready(function () {
     $("input#fav").on('click',function (){
      var id=$(this).data("id");
      var citycode=$(this).data("citycode");
      var method=$(this).attr("class");
      
      var button=$(this);
      if(method=="add"){
         console.log("hi add");
         $.ajax({
            type: 'POST',
            url:  '/favorite',
            data: {"id":id,"citycode":citycode,"method":"insert"},
            datatype:'JSON',
            success: function(data) {
               if(data=="False"){
                  window.location.href = "/login";
               }
               button.val("刪除最愛停車場");
               button.attr("class","del");
               $(".alert").css("background-color","rgba(227, 224, 83, 0.9)");
               $(".txt").text("新增成功")
               $('.alert').show(100).delay(1500).fadeOut('slow');
            } ,
            error:function(data){
               $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
               $(".txt").text("發生錯誤請稍後重試")
               $('.alert').show(100).delay(1500).fadeOut('slow');
            }
         });
      }else{
         console.log("hi delete");
         $.ajax({
            type: 'POST',
            url:  '/favorite',
            data: {"id":id,"citycode":citycode,"method":"delete"},
            datatype:'JSON',
            success: function(data) {
               if(data=="False"){
                  window.location.href = "/login";
               }
               button.val("加入最愛停車場");
               button.attr("class","add");
               $(".alert").css("background-color","rgba(227, 224, 83, 0.9)");
               $(".txt").text("刪除成功")
               $('.alert').show(100).delay(1500).fadeOut('slow');
            } ,
            error:function(data){
               $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
               $(".txt").text("發生錯誤請稍後重試")
               $('.alert').show(100).delay(1500).fadeOut('slow');
            }
          });

      }
   });
   //   彈出視窗
     $("input#com").on('click',function(){
         var id=$(this).data("id");
         var name=$(this).data("name");
         var citycode=$(this).data("citycode");
         $("#popid").text(String(id));
         $("#popsegname").text(String(name));
         $("#popcitycode").text(String(citycode));
         $(".popupouter").css("display","block");
         $("body").css("overflow","hidden");
         $.ajax({

            type: 'POST',
            url: '/comment_parklot_show',
            data: {"id":id,"citycode":citycode},
            datatype:'JSON',
            success: function(data) {
                var data1 = Array.from(data)
                showcomment_parklot(data1);
            }
            })
         function showcomment_parklot(data){
            var table = $('#show');
            table.empty();
            if(data.length!=0){
            table.append('<tr><td>用戶名</td><td>評論</td></tr>');
             for (var i=0;i<data.length;i++){
              str='<tr class="respd"><td>'+data[i]["user_id"]+'</td><td>'+data[i]["comment"]+'</td></tr>'
              table.append(str);
              }
            }else{
              var str="<h1 align='center'>尚無評論</h1>";
              table.append(str);
            }
        }

     });
     $("#comsub").on('click',function(){
        var id=$("#popid").text();
        var citycode=$("#popcitycode").text();//其他類的html要用text取裡面的字
        var comment=$("#content").val();//input、textarea類要用val取裡面的字
        if($.trim(comment)==""){//如果沒填東西或是只按空白鍵就不給評論
         return;
        }
        $.ajax({
            type: 'POST',
            url:  '/comment_parklot',
            data: {"id":id,"citycode":citycode,"method":"insert","comment":comment},
            datatype:'JSON',
            success: function(data) {
               //成功提示
               $(".alert").css("background-color","rgba(227, 224, 83, 0.9)");
               $(".txt").text("新增成功")
               $('.alert').show(100).delay(1500).fadeOut('slow');
               $('#content').val("");//清空textarea
               $(".popupouter").css("display","none");//自動關閉彈出視窗
            } ,
            error:function(data){
               //錯誤提示
               $(".alert").css("background-color","rgba(244, 67, 54,0.9)");
               $(".txt").text("發生錯誤請稍後重試")
               $('.alert').show(100).delay(1500).fadeOut('slow');
            }
          });
       });

     $(".closebtn").on('click',function(){//提示關閉按鈕
         $(".alert").hide(); 
     });

     $("#popclose").on('click',function(){//彈出視窗關閉按鈕
      $('#content').val("");//清空textarea
      $(".popupouter").css("display","none");
      $("body").css("overflow","scroll");
     });
});
let button = document.querySelector(".showmap");
let map = document.querySelector(".map");
let close = document.querySelector(".closemap");
let inputplace =  document.getElementById("pac-input");
let googlemap;
let currentposition;
let selectedplace;
button.addEventListener("click",show_google_map);
close.addEventListener("click", close_map);

function show_google_map(){
    setTimeout(()=>{
    map.showModal();},'3000')
}

function close_map(){
    map.close();
}

function initMap(){
    googlemap = new google.maps.Map(document.querySelector(".googlemap"),
    {   center:{lat:23.553118,lng:121.0211024},zoom:7}
    );
    navigator.geolocation.getCurrentPosition(function(position){
        currentposition = {
            lat:position.coords.latitude,
            lng:position.coords.longitude
        }
        googlemap.setCenter(currentposition);
        googlemap.setZoom(16);

    })
    const input = document.getElementById("pac-input");
    const searchBox = new google.maps.places.SearchBox(input);

    googlemap.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
    googlemap.addListener("bounds_changed", () => {
    searchBox.setBounds(googlemap.getBounds());
    });

    

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
    searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();
    let markers = [];


    if (places.length == 0) {
      return;
    }
    
    markers.forEach((marker) => {
        marker.setMap(null);
      });
      markers = [];
  
    

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          googlemap,
          icon,
          title: place.name,
          position: place.geometry.location,
        })
      );
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    googlemap.fitBounds(bounds);
    markers.forEach((marker) => {
        marker.setMap(googlemap);
      });
    
  });
}

