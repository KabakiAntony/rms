let adminForm = document.getElementById('adminUpForm');
let username = document.getElementById('adminUsername');
let email = document.getElementById('adminEmail');
let company = document.getElementById('adminCompany');
let password = document.getElementById('adminPassword');

email.addEventListener('input',(e)=>{
    if(isEmail(email.value)){
        document.getElementById("admin-up-error-email").innerHTML = ""; 
    }
    else{
        document.getElementById("admin-up-error-email").innerHTML = "Please enter a valid email address";
    }
});
password.addEventListener('input',(e)=>{
    if(isValidPassword(password.value))
    {
        document.getElementById("admin-up-error-password").innerHTML = "";
    }else{
        document.getElementById("admin-up-error-password").innerHTML = 
        `Password should contain atleast 
        1 uppercase character,
        1 lowercase character,
        1 number, 
        1 special character,
        atleast 6 characters
        & not more than 20`;
    }
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
        document.getElementById("admin-up-error-email").innerHTML = "Please enter a valid email address";
        return false;
    }
    if(!isValidPassword(password.value)){
        document.getElementById("admin-up-error-password").innerHTML = 
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
adminForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateData();
    signUpInfo = {
        email:email.value,
        password:password.value,
        username:username.value,
        company:company.value
    }
    postSignUp(signUpInfo);
});

function postSignUp(signUpData){
    fetch(`/admin/signup`,{
    method : 'POST',
    headers :{
        'Content-Type': 'application/json'
    },
    body:JSON.stringify(signUpData)
    
})
.then(response =>response.json())
.then(({data,status,error}) => {
    if (status === 201){
        callToast();
        inputReset();
        console.log(data);
        location.href='/fe/signin'
    }
    else if (status === 401)
    {
        document.getElementById('admin-up-error-email').innerText = error;
    }
    else if(status === 409){
        document.getElementById('admin-up-error-email').innerText = error;
    }
    else if(status === 400){
        document.getElementById('admin-up-error-username').innerText = error;
    } 
})
.catch(err => console.log(err));
}
function callToast() {
    let snackbar = document.getElementById("signup-success");
    snackbar.innerHTML = `Registration successful`;
    snackbar.className = "show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", "");
    }, 6000);
}
/* reset form after success */
function inputReset(){
  document.getElementById('adminUpForm').reset();  
}
