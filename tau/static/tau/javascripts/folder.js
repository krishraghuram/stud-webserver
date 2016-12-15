//AJAX SUCCESS AND FAIL
function ajax_success(data, status, jqxhr) {
	location.reload()
}
function ajax_error(jqxhr, status, error) {
	$("#error").text(jqxhr.responseText)
}

//FOLDER 
	//CONTEXT MENU
		$(function(){
			$('#folder-list').contextMenu({
				selector: 'a.context-menu-folder', 
				callback: function(key, options) {
					var m = "clicked : " + key + " on " + $(this).text().trim();
					console.log(m.replace(/\r?\n|\r/g,""))
					if(key=="delete")
					{
						data =	{
									action:"delete",
									path:path,
									name:$(this).text().trim(),
									csrfmiddlewaretoken: csrftoken
								}
						$.ajax({
						  method : 'POST',
						  url : folderView,
						  data : data,
						  success : ajax_success,
						  error : ajax_error
						});						

					}
					// else if(key=="send")
					// {
					// 	//For Sending, we need to prompt user for the id of the receiver
					// 	//http://www.w3schools.com/jsref/met_win_prompt.asp
					// }
				},
				items: {
					"delete": {name: "Delete", icon: "fa-trash"},
					// "send": {name: "Send", icon: "fa-send"},
				}
			});
		});




//FILE 
	//UPLOAD
		// "upload" is the camelized version of the HTML element's ID
		Dropzone.options.uploadzone = {
			paramName: "file", // The name that will be used to transfer the file
			maxFilesize: 25, // MB
			uploadMultiple: false, //Only one file will get uploaded
			maxFiles: 1,
			init: function () {
				// Set up any event handlers
				this.on("addedfile", function(){
					console.log("submit");
					$("#form").submit();
				});
				//If File Uploaded Successfully
				this.on("success", function(){
					console.log("success");
					location.reload()
				});
				//If Upload wasnt successful
				this.on("error", function(file, error, xhr){
					console.log("error");
					window.location = errorView.substring(0, errorView.length-1) + error
				});			
			}
		};
	//CONTEXT MENU
		$(function(){
			$('#file-list').contextMenu({
				selector: 'a.context-menu-file', 
				callback: function(key, options) {
					var m = "clicked : " + key + " on " + $(this).text().trim();
					console.log(m.replace(/\r?\n|\r/g,""))
					if(key=="delete")
					{
						data =	{
									action:"delete",
									path:path,
									name:$(this).text().trim(),
									csrfmiddlewaretoken: csrftoken
								}
						$.ajax({
						  method : 'POST',
						  url : fileView,
						  data : data,
						  success : ajax_success,
						  error : ajax_error
						});							
					}
					// else if(key=="send")
					// {
					// 	//For Sending, we need to prompt user for the id of the receiver
					// 	//http://www.w3schools.com/jsref/met_win_prompt.asp
					// }
				},
				items: {
					"delete": {name: "Delete", icon: "fa-trash"},
					// "send": {name: "Send", icon: "fa-send"},
				}
			});
		});









//JUMBOTRON
	//CONTEXT MENU
		$(function(){
			$.contextMenu({
				selector: '.context-menu-jumbotron', 
				callback: function(key, options) {
					if(key=="create")
					{
						var name = prompt("Please enter the folder name", "");
						data =	{
									action:"create",
									path:path,
									name:name,
									csrfmiddlewaretoken: csrftoken
								}
						$.ajax({
						  method : 'POST',
						  url : folderView,
						  data : data,
						  success : ajax_success,
						  error : ajax_error
						});							
					}					
					else if(key=="upload")
					{
						$('#uploadzone').click()
					}
				},
				items: {
					"create": {name: "Create Folder", icon: "fa-folder"},
					"upload": {name: "Upload File", icon: "fa-file"},
				}
			});
		});