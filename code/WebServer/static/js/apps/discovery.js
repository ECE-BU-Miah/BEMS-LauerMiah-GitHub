$(document).ready(function() {
  // var ws = new WebSocket();
  $("#find_devices").click( function(evt) {
    // Prevent the default behavior from occurring.
    evt.preventDefault();
    var ids = [];
    $("input[type=checkbox]:checked").each(function() {
      ids.push($(this).attr("id"));
    });
    jsonIDs = JSON.stringify(ids)
    // alert(jsonDevices);
    $.ajax({
      url: '/discovery/ajax',
      type: 'POST', // Send a POST request
      contentType: 'application/json;charset=UTF-8',
      data: jsonIDs,
      success: function(response) {
        console.log(response);
      }
    });
  });

});
