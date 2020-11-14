let passwordForm = document.getElementById('newPasswordForm');
let email = document.getElementById('newPasswordEmail');
let newPassword = document.getElementById('newPassword');

email.addEventListener('input',(e)=>{
    if(isEmail(email.value)){
        document.getElementById("new-password-error-email").innerHTML = ""; 
    }
    else{
        document.getElementById("new-password-error-email").innerHTML = "Please enter a valid email address";
    }
});
newPassword.addEventListener('input',(e)=>{
    if(isValidPassword(newPassword.value))
    {
        document.getElementById("new-password-error").innerHTML = "";
    }else{
        document.getElementById("new-password-error").innerHTML = 
        `Password should contain atleast 
        1 uppercase character,
        1 lowercase character,
        1 number, 
        1 special character,
        atleast 6 characters
        & not more than 20`;
    }
});



function postNewPassword(){
newPasswordData = {
    email:email.value,
    password:newPassword.value
};
fetch('/auth/newpass',{
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(newPasswordData)
  })
  .then(response => response.json())
  .then(({data,status,error})=>{
    if(status === 200){
        callToast(data);             
    }
    else if(status === 400){
      document.getElementById('new-password-error-email').innerHTML = `${error}`;
    }
    else if(status === 401){
      document.getElementById('new-password-error-email').innerHTML = `${error}`;
    }
})
// when cleaning code stop posting to the console
.catch(err => console.log(`This error occured :${err}`));
}
/* reset submission */
passwordForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateData();
    postNewPassword();
});

/* validaition functions */
function isEmail(my_email){
    let emailRegex =/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/igm;
    return my_email.match(emailRegex);
}
function isValidPassword(my_password){
    let passwordRegex = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){6,20}$/igm;
    return my_password.match(passwordRegex);
}
function validateData(){
    if(!isEmail(email.value)){
        document.getElementById("new-password-error-email").innerHTML = "Please enter a valid email address";
        return false;
    }
    if(!isValidPassword(newPassword.value)){
        document.getElementById("in-error-password").innerHTML = 
        `Password should contain atleast 
        1 uppercase character,
        1 lowercase character,
        1 number, 
        1 special character,
        atleast 6 characters
        & not more than 20.`;
        return false;
    }
}
function callToast(data) {
    let snackbar = document.getElementById("signup-success");
    snackbar.innerHTML = `
    ${data}
    </br>
    </br>We will now take you to the sign in page.
    `
    snackbar.className = "show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", "");
    location.href ='/fe/signin';
    }, 5000);
}