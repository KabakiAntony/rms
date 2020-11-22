import {validateEmailData} from './rmsModule.js'
import {emailInputListener} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'
import {showLoader} from './rmsModule.js'

/* variables for this form */
const signUpForm = document.getElementById('rmsForm');
const upEmail = document.getElementById('rmsEmail');
const username = document.getElementById('rmsUsername');
const company = document.getElementById('rmsCompany');
let intentData;

/* validate inputs*/
emailInputListener(upEmail);

/* sign up submission */
signUpForm.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateEmailData();
  showLoader();
  SignUp();
}); 

/* this function sends data to the server */
function SignUp(){
intentData = {
    username:username.value,
    email:upEmail.value,
    company:company.value
};
rmsFetch('/intent',"POST",intentData)
}


