import {validateEmailData} from './rmsModule.js'
import {validatePasswordData} from './rmsModule.js'
import {emailInputListener} from './rmsModule.js'
import {passwordInputListener} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'

// variables for this form
let passwordForm = document.getElementById('rmsForm');
let email = document.getElementById('rmsEmail');
let newPassword = document.getElementById('rmsPassword');
let newPasswordData;

/* validate input data */
emailInputListener(email);
passwordInputListener(newPassword);

function updatePassword(){
newPasswordData = {
    email:email.value,
    password:newPassword.value
};
rmsFetch('/auth/newpass','PUT',newPasswordData,'/fe/signin');
}
/* reset submission */
passwordForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateEmailData();
    validatePasswordData();
    updatePassword();
});