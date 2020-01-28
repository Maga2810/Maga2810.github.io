$(document).ready(function(){
  // Contacts Modal
  $("#openContacts").click(function(){ 
    $("#showCont").modal({backdrop: true});
  });
  // Login & Registration
  $("#register_button").click(function(){
    $("#reGis").modal({backdrop: true});
  });

  $("#login_button").click(function(){
    $("#loGin").modal({backdrop: true});
  });
  // Countries Modal
  $("#kazModal").click(function(){
    $("#kaModal").modal({backdrop: true});
  });
      
       
}); 
    // Hamburger Button   
function openBurger() {
  document.getElementById("myBurger").style.width = "305px";
  document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}
function closeBurger() {
  document.getElementById("myBurger").style.width = "0";
  document.body.style.backgroundColor = "rgba(0,0,0,0)";
}
// Biography Modal
function openUs() {
  document.getElementById("navBio").style.height = "100%";
}
function closeUs() {
  document.getElementById("navBio").style.height = "0%";
}

$("body, html").click(function(event){
  console.log(event.target)
  if (event.target.id != "hui"){
    closeBurger();
  }
})
