function event_retriever(date=jQuery('#dateField').text()){
			jQuery.post(
			EventView,
			{date: date, csrfmiddlewaretoken: csrftoken},
			function(data){
				console.log("Updating Events")
				// console.log(data);
				jQuery("#event-list").html("\n");
				for (var i=0; i<data.length; i++){
					var title = data[i].fields['title'].toString();
					var pk = data[i].pk.toString();
					var start_dt = new Date(data[i].fields['start_dt']);
					var date = jQuery.format.date(start_dt, "E MMM dd yyyy");
					var time = jQuery.format.date(start_dt, "hh:mm a");
					var venue = data[i].fields['venue'].toString();
					jQuery("#event-list").append(
						"<li onmouseover=\'	show_detail(\""+pk+"\")\' onmouseout=\'hide_detail(\""+pk+"\")\'>"+"\n"+
						title+"\n"+
						"<div id=\'" + pk + "\' class=\'li-detail\'>"+"\n"+
						date+"<br/>"+"\n"+
						time+"<br/>"+"\n"+
						venue+"<br/>"+"\n"+
						"</div>"+"\n"+
						"</li>"+"\n"
					);
				}
			}
		);
}

jQuery(document).ready(function(){
	console.log("Ready!");
	//Set Current Date to dateField
	var now = new Date();
		now = jQuery.format.date(now, "yyyy-MM-dd");
	jQuery('#dateField').text(now);
	//Call event_retriever to populate the list immediately
	event_retriever(now);
	//Call event_retriever based on interval
	//Not good since it destroys the css
	//The method below is far better, since its based on clicks in the document
	// setInterval(function(){
	// 	event_retriever();
	// },1000);
	//Call event_retriever based on clicks in document
	jQuery(document).click(function() {
    	event_retriever();
	});
})