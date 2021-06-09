var LoginForm = document.getElementById("LoginForm");
var RegForm = document.getElementById("RegForm");
var Indicator = document.getElementById("Indicator");

function register(){
    RegForm.style.transform = "translateX(0px)";
    LoginForm.style.transform = "translateX(0px)";
    Indicator.style.transform = "translateX(155px)";
}
function login(){
    RegForm.style.transform = "translateX(600px)";
    LoginForm.style.transform = "translateX(600px)";
    Indicator.style.transform = "translateX(0px)";
}
