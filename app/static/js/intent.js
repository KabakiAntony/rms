// this registers a company 
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
        // display this success message better.
        // but for now display it on the error portion
        document.getElementById('up-error-company').innerHTML = `Registration successful`;
      }
      else if(status === 400){
        document.getElementById('up-error-email').innerHTML = `${error}`;
      }
      else if(status === 409){
        document.getElementById('up-error-email').innerHTML = `${error}`;
      }
  })
  .catch(err => console.log(`This error occured :${err}`));
}

 
/* validaition functions */
function isEmail(my_email){
    let emailRegex =/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/igm;
    return my_email.match(emailRegex);
}
// function isValidPassword(my_password){
//     let passwordRegex = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){6,20}$/igm;
//     return my_password.match(passwordRegex);
// }
function validateData(){
    if(!isEmail(upEmail.value)){
        document.getElementById("up-error-email").innerHTML = "Please enter a valid email address";
        return false;
    }
    // if(!isValidPassword(upPassword.value)){
    //     document.getElementById("up-error-password").innerHTML = 
    //     `Password should contain atleast 
    //     1 uppercase character,
    //     1 lowercase character,
    //     1 number, 
    //     1 special character,
    //     atleast 6 characters
    //     & not more than 20.`;
    //     return false;
    // }
}
// function callToast(name,email) {
//     let snackbar = document.getElementById("signup-success");
//     snackbar.innerHTML = `
//     Congratulations &nbsp;<span>${name}</span>,&nbsp;&nbsp;
//     Please check &nbsp;<span>${email}</span>&nbsp;for sign in instructions.
//     </br>
//     </br>We will now redirect you to the homepage....
//     `
//     snackbar.className = "show";
//     setTimeout(function(){ snackbar.className = snackbar.className.replace("show", "");
//     location.href ='/';
//     }, 10000);
// }
/* sign up submission */
signUpForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateData();
    postSignUp();
}); 
