      var socket = io.connect('http://localhost:8000');
   
      socket.on('recMsg', function(data){
        console.log('recMsg: ',data)
        $('.messages').append('<div class="chip">'+data.message+'</div>');
	        window.scrollTo(0,document.body.scrollHeight);
      }) 
      
      function sendMsg(data){
        console.log('sending msg: ' + data);
        socket.emit('sendMsg', data)
      }

$(document).ready(function() {
	$('#message').keyup(function(e){
	    if(e.keyCode == 13)
	    {
	        message = $('#message').val();
	        $('#message').val('');
	      	sendMsg(message);
	        $('.messages').append('<div class="chip own">'+message+'</div>');
	        window.scrollTo(0,document.body.scrollHeight);
	    }
	});
})