import {validateEmailData} from './rmsModule.js'
import {validatePasswordData} from './rmsModule.js'
import {emailInputListener} from './rmsModule.js'
import {passwordInputListener} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'
import {showLoader} from './rmsModule.js'

let adminForm = document.getElementById('rmsForm');
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

adminForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateEmailData();
    validatePasswordData();
    showLoader();
    postSignUp();
});