  $(document).ready(function() {
  console.log("active devices ready");
    $('input[type="checkbox"]').change(function() {
      // evt.preventDefault();
      console.log("Changed checkbox");
      var dict = {};
      dict["id"] = $(this).attr("id");
      if($(this).prop("checked") == true) {
        dict["powerState"] = "ON";
      } else if ($(this).prop("checked") == false) {
        dict["powerState"] = "OFF";
      }
      jsonDict = JSON.stringify(dict)
      console.log(dict);
      console.log(jsonDict);
      $.ajax({
        url: '/active_devices/ajax/setDeviceStatus',
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: jsonDict,
        success: function(response) {
          console.log(response);
        }
      });

    });
    // $('input[type="checkbox"]').change(function() {
  //   if($(this).prop("checked") == true) {
  //     console.log("checked true");
  //     console.log($(this).attr("id"));
  //   }
  //   console.log("clicked");
  // });

});
