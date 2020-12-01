import {validateEmailData} from './rmsModule.js'
import {emailInputListener} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'
import {showLoader} from './rmsModule.js'

/* variables for this form */
let forgotForm = document.getElementById('rmsForm');
let forgotEmail = document.getElementById('rmsEmail');
let forgotData;

/* validate on input */
emailInputListener(forgotEmail);

function Forgot(){
forgotData = {
    email:forgotEmail.value
};
rmsFetch('/auth/forgot','POST',forgotData,'/signin');
}

/* reset submission */
forgotForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateEmailData();
    showLoader();
    Forgot();
});


