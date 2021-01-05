import {validateEmailData, validatePasswordData, emailInputListener} from './rmsModule.js'
import {passwordInputListener, rmsFetch, showLoader} from './rmsModule.js'

let SignUpForm = document.getElementById('rmsSignUpForm');
let username = document.getElementById('rmsUsername');
let email = document.getElementById('rmsEmail');
let company = document.getElementById('rmsCompany');
let password = document.getElementById('rmsPassword');
let isActive = document.getElementById('rmsActive');
let role = document.getElementById('rmsRole');
let signUpInfo;

emailInputListener(email);
passwordInputListener(password);

function postSignUp(){
    signUpInfo = {
        email:email.value,
        password:password.value,
        username:username.value,
        company:company.value,
        role:role.value,
        isActive:isActive.value
    };
    rmsFetch('/auth/signup','POST',signUpInfo,'/signin');    
}

SignUpForm.addEventListener('signUpSubmit',(e)=>{
    e.preventDefault();
    validateEmailData();
    validatePasswordData();
    showLoader();
    postSignUp();
});
