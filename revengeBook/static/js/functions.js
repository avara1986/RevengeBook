// Thanks to: chriszweber. https://djangosnippets.org/snippets/2656/
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


function addMilestone(){
	var _data = getFields('formRevengeMiltestone');
	$('#formErrorGeneric').css('display','none');
    if(_data!=null){
    	$.ajax('/kwsn/add-milestone/', {
	    	type: 'POST',
	    	data: _data,
	    	dataType: 'json'
    	})
    	.success(function(data) {
    		console.log(data.response)
    		if(data.response==true) {
    			/*window.location.replace(window.location.href+'?result_add_milestone=ok');*/
    			// TODO
    			getMilestones('milestones_list',$('#idFriendProfile').val());
    		}
    	})
    	.fail(function() { console.log("lookup error"); });
    }else{
    	$('#formErrorGeneric').css('display','block');
    }
    return false;
}
$('#sendMilestone').click(function() {
	addMilestone();
});

function checkSignUp(){
	var _data = getFields('formSignUp');
	$('#formErrorGeneric').css('display','none');
    if(_data!=null){
    	$('#formSignUp').submit();
    }else{
    	$('#formErrorGeneric').css('display','block');
    }
    return false;
}
function checkConfiguration(){
	var _data = getFields('formConfiguration');
	$('#formErrorGeneric').css('display','none');
    if(_data!=null){
    	$('#formConfiguration').submit();
    }else{
    	$('#formErrorGeneric').css('display','block');
    }
    return false;
}

function searchFriend(sectionLoad){
	var searchFriend = $('#'+sectionLoad).val();
	
	$.ajax('/kwsn/search-friends/', {type: 'POST', data: {
		searchFriend: searchFriend
	}, dataType: 'json'})
	.done(function(data) {
		//console.log(data.response)
		if(data.response==true) {
			//console.log(data.friends);
			var resultSeach = "";
			$.each(data.friends, function(i, friend){
				resultSeach += '<li><div class="dropDownElement">'+
				'<a href="#" onclick="sendFriendRequest(\''+friend.id+'\')"><span class="glyphicon glyphicon-plus pull-right dropDownIcon"></span></a>'+
				'<a href="/profile/'+friend.id+'" target="_blank"><span class="glyphicon glyphicon-eye-open pull-right"></span></a>'+
				''+friend.username+'</div></li>';
				console.log(friend.id);
				console.log(friend.username);
				console.log(friend.first_name);
				console.log(friend.last_name);
				console.log(friend.email);
			});
			resultSeach += '<li class="divider"></li>';
			resultSeach += '<li><a href="#" onclick="$(\'#formSearchFriend\').submit()">See all results</a></li>';
			$('#'+sectionLoad+'Menu').html(resultSeach);
			$('#'+sectionLoad+'Show').dropdown('toggle');
		}
	})
	.fail(function() { console.log("lookup error"); });
	return false;
}
$('#searchFriendNavBar').keyup(function() {
	searchFriend('searchFriendNavBar');
});


function searchMyFriend(sectionLoad){
	var searchFriend = $('#'+sectionLoad).val();
	
	$.ajax('/kwsn/search-my-friend/', {type: 'POST', data: {
		searchFriend: searchFriend
	}, dataType: 'json'})
	.done(function(data) {
		console.log(data.response)
		if(data.response==true) {
			var resultSeach = "";
			var idSelected = $('#affected').val();
			var classSelected = "";
			$.each(data.friends, function(i, friend){
				if(idSelected == friend.id){
					classSelected='class="alert-success"'
				}else{
					classSelected=''
				}
				resultSeach += '<li id="searchFriendFormRevenge_'+friend.id+'" '+classSelected+'>'+
				'<a href="#" onclick="selectAddFriend(\''+friend.id+'\',\''+friend.username+'\'); return false;">'+
				friend.username+'</a></li>';
				console.log(friend.id);
				console.log(friend.username);
				console.log(friend.first_name);
				console.log(friend.last_name);
				console.log(friend.email);
			});
			//resultSeach += '<li class="divider"></li>';
			$('#'+sectionLoad+'Menu').html(resultSeach);
			$('#'+sectionLoad+'Menu').css('display','block');
			$('#'+sectionLoad+'Show').dropdown('toggle');
		}
	})
	.fail(function() { console.log("lookup error"); });
	return false;
}
$('#searchFriendFormRevenge').keyup(function() {
	searchMyFriend('searchFriendFormRevenge');
});
function selectAddFriend(id,name){
	$('#searchFriendFormRevenge').val(name);
	$('#searchFriendFormRevengeMenu').css('display','none');
	$('#affected').val(id)
	$('#searchFriendFormRevenge_'+id).addClass();
}


function sendFriendRequest(friendId){
	$.ajax('/kwsn/send-friend-request/', {type: 'POST', data: {
		friendId: friendId
	}, dataType: 'json'})
	.done(function(data) {
		//console.log(data.response)
		if(data.response==true) {
			window.location.replace(window.location.href+'?result_send_friend_request=ok');
		}
	})
	.fail(function() { console.log("lookup error"); });
	return false;
}
function getMilestoneForm(layer,milestone_id){
	$('#'+layer).html('<h1>Cargando, por favor, espere....</h1>');
    	$.ajax('/milestone_form/?milid='+milestone_id, {
	    	type: 'GET',
	    	dataType: 'html'
    	})
    	.success(function(data) {
    			$('#'+layer).html(data);
    	})
    	.fail(function() { console.log("lookup error"); });
    return false;
}
function getMilestones(layer,idFriend){
	$('#'+layer).html('<h1>Cargando, por favor, espere....</h1>');
    	$.ajax('/milestones/'+idFriend, {
	    	type: 'GET',
	    	dataType: 'html'
    	})
    	.success(function(data) {
    			$('#'+layer).html(data);
    	})
    	.fail(function() { console.log("lookup error"); });
    return false;
}

function showProfileSection(section){
	$('#milestones_list').css('display','none');
	$('#button_milestones_list').removeClass('btn-primary').addClass('btn-default');
	$('#profile_info').css('display','none');
	$('#button_profile_info').removeClass('btn-primary').addClass('btn-default');
	$('#'+section).css('display','block');
	$('#button_'+section).addClass('btn-primary');
}

/**
 * Aux functions to validate Form fields
 * 
 */

/*
 * getFields
 * Guarda en un Array los campos de un formulario
 * */
function getFields(form, validate){
	var $form=$('#'+form),
		focusMe=[];
	if(validate===undefined) validate=true;
	if($form){
		var values={},
			valid=true;
		$form.find(":input").each(function(index,el){
			if(this.type==="radio"){
				if(this.checked)
					if($form.find("input[name="+this.name+"]").length>0)
						values[this.name]=$(this).val();
					else
						values[this.id]=$(this).val();
			}else if(this.type==="checkbox"){
				values[this.id]=this.checked;
			}else{
				if(this.type==="email" && $(this).val()!="" && !isEmail(this.value) && this.required===false){
					valid=false;
					if(validate){
						
						bindError(this);
						focusMe.push(this);
					}
				}else
					values[this.id]=$(this).val();
			}
				
			
			if(this.required!==false && this.required!==undefined){
				if((this.type==="radio" || this.type==="checkbox") && !this.checked){
					if(validate){
						bindError(this);
						focusMe.push(this);
					}
					valid=false;
				}else{
					if(isEmpty(this.value) || (this.type==="email" && !isEmail(this.value)) ){
						valid=false;
						if(validate){
							bindError(this);
							focusMe.push(this);
						}
					}else
						if(validate){
							unbindError(this);
						}
				}
			}
		});
		if(validate){
			if(valid)
				return values;
			else{
				$(focusMe[0]).focus();
				return null;
			}
		}else
			return values;
	}else
		return null;
}


/*
 * isEmail: Thanks to Jose (https://github.com/josex2r)
 * */
function isEmail(email){   
	return email.match(/^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,3})$/);
};

function isEmpty(variable){
	return (typeof variable==="undefined" || variable===null || variable.length==0 || variable.value==="");
};

function haveWhitespaces(variable) {   
    var espacio=[" ","\n","\t","\r"];
    if(!Form.isEmpty(variable))
		for(var i=0; i<variable.length; i++)
			if(espacio.indexOf( variable.substring(i,i+1) ) != -1)
				return true;
    return false;
}
function isNumber(n) {
	  return !isNaN(parseFloat(n)) && isFinite(n);
}


/*
 * bindError: Thanks to Jose (https://github.com/josex2r)
 * */
function bindError(node){
	var $inputNode=$(node);
	if($inputNode.type!=="submit"){
		if($inputNode.nodeName=="OPTION")
			$inputNode=$inputNode.parent();
		$inputNode.addClass("error");
		if($inputNode.type==="checkbox" || $inputNode.type==="radio" || $inputNode.type==="select-one" || $inputNode.type==="select-multiple")
			$inputNode.bind("change.inputError",function(){
				$inputNode.removeClass("error");
				$inputNode.unbind("change.error");
			});
		else if($inputNode.type!=="submit")
			$inputNode.bind("keyup.inputError",function(){
				$inputNode.removeClass("error");
				$inputNode.unbind("keyup.error");
			});
	}
}


/*
 * unbindError: Thanks to Jose (https://github.com/josex2r)
 * */
function unbindError(node){
	var $inputNode=$(node);
	if($inputNode.type!=="submit"){
		if($inputNode.nodeName=="OPTION")
			$inputNode=$inputNode.parent();
		$inputNode.removeClass("input_error");
		if($inputNode.type==="checkbox" || $inputNode.type==="radio" || $inputNode.type==="select-one" || $inputNode.type==="select-multiple")
			$inputNode.unbind("change.inputError");
		else if($inputNode.type!=="submit")
			$inputNode.unbind("keyup.inputError");
	}
}