var $datePicker = $("div#datepicker");

var $datePicker = $("div");


$datePicker.datepicker({
  beforeShowDay: function(date) {
    var day = date.getDay();
    return [(day != 0 && day != 6)];
  },
  changeMonth: true,
  maxDate: "+2m",
  minDate: "+0d",
  changeYear: false,
  inline: true,
  altField: "#actualDate",
  onSelect: function(dateText, inst) {
    var date = $(this).datepicker('getDate'),
      day = date.getDate(),
      month = date.getMonth() + 1;

    console.log(month + "/" + day);
    window.location.replace("https://www.google.com");
  }
})
