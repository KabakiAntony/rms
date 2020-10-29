/* values for sign-up */
let signUpForm = document.getElementById('upForm');
let upEmail = document.getElementById('upEmail');

/* signup validations */

upEmail.addEventListener('input',(e)=>{
    if(isEmail(upEmail.value)){
        document.getElementById("up-error-email").innerHTML = ""; 
    }
    else{
        document.getElementById("up-error-email").innerHTML = "Please enter a valid email address";
    }
});

/* sign up function */
function postSignUp(){
const email = document.getElementById('upEmail').value;
const username = document.getElementById('upUsername').value;
const company = document.getElementById('upCompany').value;
signUpData = {
    username,
    email,
    company
};
fetch('/intent',{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(signUpData)
  })
  .then(response => response.json())
  .then(({data,status,error})=>{
      if(status === 201){
        callToast(data['company']);
        inputReset();
      }
      else if(status === 400){
        document.getElementById('up-error-company').innerHTML = `${error}`;
      }
      else if(status === 409){
        document.getElementById('up-error-company').innerHTML = `${error}`;
      }
  })
  .catch(err => console.log(`This error occured :${err}`));
}

 
/* validaition functions */
function isEmail(my_email){
    let emailRegex =/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/igm;
    return my_email.match(emailRegex);
}
function validateData(){
    if(!isEmail(upEmail.value)){
        document.getElementById("up-error-email").innerHTML = "Please enter a valid email address";
        return false;
    }
}
function callToast(company) {
    let snackbar = document.getElementById("signup-success");
    snackbar.innerHTML = `
    ${company} registered successfully ,<br/>
    see admin email for further instructions.
    `
    snackbar.className = "show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", "");
    }, 5000);
}
/* reset form after success */
function inputReset(){
  document.getElementById('upForm').reset();  
}
/* sign up submission */
signUpForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateData();
    postSignUp();
}); 
