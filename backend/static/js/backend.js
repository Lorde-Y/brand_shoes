$(function(){
    selectMenu();
});
//二级 导航 联动
function selectMenu(){
	 $(document).on('change','#parentMenu',function(){
			  $.ajax({
			         url: "/backend/Twolink/",
			         type: "POST",
			         data: {id:$(this).val()},
			         dataType: "html",
			         success: function(data){
			          $('#selectOption').html('');
			          $('#selectOption').append(data);
			           }  
			     });
   });
    //三级 联动
    $(document).on('change','#secondMenu',function(){
		   $.ajax({
			         url: "/backend/Twolink/",
			         type: "POST",
			         data: {
			         	id:$(this).val(),
			         	pid:$('#parentMenu option:selected').val(),
			         },
			         dataType: "html",
			         success: function(data){
			         	 $('#selectOption').html('');
			          $('#selectOption').append(data);
			           }  
			     });
    });

     //三级 联动
    $(document).on('change','#secondMenu2',function(){
		   $.ajax({
			         url: "/backend/Twolink2/",
			         type: "POST",
			         data: {
			         	id:$(this).val(),
			         	pid:$('#parentMenu option:selected').val(),
			         },
			         dataType: "html",
			         success: function(data){
			         	 $('#selectOption').html('');
			          $('#selectOption').append(data);
			           }  
			     });
    });

}