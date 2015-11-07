$(document).ready(function() {
	$.getJSON('/account', function(data) {
		console.log(data.length);
		$('#accounts').html('');
		for(i = 0; i < data.length; i++) {
			account = data[i];
			if (account['balance'] >= 0) {
				$('#accounts').append('<li class="collection-item">'+account['name']+'<span class="collection-amount">€ '+account['balance']+'</span></li>');
			}else {
				$('#accounts').append('<li class="collection-item">'+account['name']+'<span class="collection-amount deep-orange-text">€ '+account['balance']+'</span></li>');
			}
		}
	});
});