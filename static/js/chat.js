$(document).ready(function() {
	$('#message').keyup(function(e){
	    if(e.keyCode == 13)
	    {
	        message = $('#message').val();
	        $('#message').val('');
	        $('.messages').append('<div class="chip own">'+message+'</div>');
	        window.scrollTo(0,document.body.scrollHeight);
	    }
	});
})