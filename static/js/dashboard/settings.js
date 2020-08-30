var first_name = document.getElementById("edit_first").value;
var last_name = document.getElementById("edit_last").value;
var email_address = document.getElementById("edit_email").value;
document.getElementById("submit-change-btn").disabled = true; //disable the button as default
//This function will compare to see if the user's first,last,and email are the same
//Purpose of this is so that users arent able to trigger a change if the first,last,and email are currently the same
function checkIfCrudentialsAreDifferent() {
  const button = document.getElementById("submit-change-btn");
  const fn = document.getElementById("edit_first").value;
  const ln = document.getElementById("edit_last").value;
  const em = document.getElementById("edit_email").value;
  if (first_name == fn && last_name == ln && email_address == em) {
    button.disabled = true;
  } else {
    button.disabled = false;
  }
}

function checkPasswordMatch() { //function to check if the passwords match each other
  var password = $("#first-pass").val();
  var confirmPassword = $("#second-pass").val();
  // if passwords don't match, prompt user and disable the save changes button
  if (password != confirmPassword || password == "" || confirmPassword == "") {
    document.getElementById('signup-btn').disabled = true;
    if (password == "" || confirmPassword == "") { //if the field is empty
      $("#divCheckPasswordMatch").html("Dont Leave fields empty!");
    } else {
      $("#divCheckPasswordMatch").html("Passwords do not match!");
    }
  } else {
    document.getElementById('signup-btn').disabled = false;
    $("#divCheckPasswordMatch").html("");
  }
}
$(document).ready(function() {
  $("#txtNewPassword, #txtConfirmPassword").keyup(checkPasswordMatch);
});
