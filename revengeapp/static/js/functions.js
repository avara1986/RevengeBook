// Django CSRF framework
$(document).ajaxSend(function(event, xhr, settings) {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	function sameOrigin(url) {
		// url could be relative or scheme relative or absolute
		var host = document.location.host; // host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
			(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
			// or any other URL that isn't scheme relative or absolute i.e relative.
			!(/^(\/\/|http:|https:).*/.test(url));
	}
	function safeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
});
function searchFriend(){
	var searchFriend = $('#searchFriend').val();
	
	$.ajax('/kwsn/search-friends/', {type: 'POST', data: {
		searchFriend: searchFriend
	}, dataType: 'json'})
	.done(function(data) {
		console.log(data.response)
		if(data.response==true) {
			//console.log(data.friends);
			var resultSeach = "";
			$.each(data.friends, function(i, friend){
				resultSeach += '<li><a href="/profile/'+friend.id+'" target="_blank">'+friend.username+'</a></li>';
				console.log(friend.id);
				console.log(friend.username);
				console.log(friend.first_name);
				console.log(friend.last_name);
				console.log(friend.email);
			});
			resultSeach += '<li class="divider"></li>';
			resultSeach += '<li><a href="/search-friends/?searchFriend='+searchFriend+'" target="_blank">See all results</a></li>';
			$('#searchFriendMenu').html(resultSeach);
			$('#showSearch').dropdown('toggle');
		}
	})
	.fail(function() { console.log("lookup error"); });
}
$('#searchFriend').keyup(function() {
	searchFriend();
});