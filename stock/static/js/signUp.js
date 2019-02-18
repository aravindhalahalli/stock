$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){ 
                $("#dd").html("<h1>User Created!!!</h1>");
                console.log(response);
			},
			error: function(error){
                alert("Error!!! try again");
				console.log(error);
			}
		});
	});
});
