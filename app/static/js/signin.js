import {validateEmailData} from './rmsModule.js'
import {validatePasswordData} from './rmsModule.js'
import {emailInputListener} from './rmsModule.js'
import {passwordInputListener} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'

/* variables for this form*/
let signInForm = document.getElementById('rmsForm');
let inEmail = document.getElementById('rmsEmail');
let inPassword = document.getElementById('rmsPassword');
let signInData;

/* sign in validations*/
emailInputListener(inEmail);
passwordInputListener(inPassword);

function signIn(){
    signInData = {
        email:inEmail.value,
        password:inPassword.value
    };
    rmsFetch('/auth/signin',"POST",signInData,'/fe/who')
}

/* sign in submission */
signInForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateEmailData();
    validatePasswordData();
    signIn();
});

