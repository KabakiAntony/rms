import {validateEmailData, validatePasswordData, emailInputListener} from './rmsModule.js'
import {passwordInputListener, rmsFetch, showLoader} from './rmsModule.js'

let SignUpForm = document.getElementById('rmsForm');
let firstname = document.getElementById('rmsFirstName');
let lastname = document.getElementById('rmsLastName');
let mobile = document.getElementById('rmsMobile');
let email = document.getElementById('rmsEmail');
let company = document.getElementById('rmsCompany');
let password = document.getElementById('rmsPassword');
let isActive = document.getElementById('rmsActive');
let role = document.getElementById('rmsRole');
let signUpInfo, adminInfo;

emailInputListener(email);
passwordInputListener(password);

function createAdminEmployee(){
    adminInfo = {
        firstname:firstname.value,
        lastname:lastname.value,
        password:password.value,
        email:email.value,
        company:company.value,
        mobile:mobile.value,
        role:role.value,
        isActive:isActive.value
    };
    rmsFetch('/auth/admin/employees','POST',adminInfo,'/signin','rmsForm');
};

SignUpForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateEmailData();
    validatePasswordData();
    showLoader();
    createAdminEmployee();       
});
