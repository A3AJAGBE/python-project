
// Get aside
var asideNav = document.getElementById("nav");

// Get all <a class="nav"> inside aside
var menu = asideNav.getElementsByClassName("nav");

// Loop through the link and add the active class to the current/clicked link
for (var i = 0; i < menu.length; i++) {
  menu[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
