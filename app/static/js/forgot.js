let forgotForm = document.getElementById('forgotForm');
let forgotEmail = document.getElementById('forgotEmail');


forgotEmail.addEventListener('input',(e)=>{
    if(isEmail(forgotEmail.value)){
        document.getElementById("forgot-error-email").innerHTML = ""; 
    }
    else{
        document.getElementById("forgot-error-email").innerHTML = "Please enter a valid email address";
    }
});



function postForgot(){
const email = document.getElementById('forgotEmail').value;
forgotData = {
    email
};
fetch('/auth/forgot',{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(forgotData)
  })
  .then(response => response.json())
  .then(({data,status,error})=>{
    if(status === 202){
        callToast(data);             
    }
    else if(status === 400){
      document.getElementById('forgot-error-email').innerHTML = `${error}`;
    }
    else if(status === 404){
      document.getElementById('forgot-error-email').innerHTML = `${error}`;
    }
})
// when cleaning code stop posting to the console
.catch(err => console.log(`This error occured :${err}`));
}
/* reset submission */
forgotForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateData();
    postForgot();
});

/* validaition functions */
function isEmail(my_email){
    let emailRegex =/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/igm;
    return my_email.match(emailRegex);
}
function validateData(){
    if(!isEmail(forgotEmail.value)){
        document.getElementById("forgot-error-email").innerHTML = "Please enter a valid email address";
        return false;
    }
}
function callToast(data) {
    let snackbar = document.getElementById("signup-success");
    snackbar.innerHTML = `
    ${data}
    </br>
    </br>We will now take you to the home page.
    `
    snackbar.className = "show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", "");
    location.href ='/Welcome';
    }, 5000);
}


