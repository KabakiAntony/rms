import {clearErrorDivs} from './rmsModule.js'
import {validateEmailData, emailInputListener} from './rmsModule.js'
import {rmsFetch, showLoader} from './rmsModule.js'

let createProjectForm = document.getElementById('rmsForm');
let projectName = document.getElementById('rmsProject');
let dateFrom = document.getElementById('dateFrom');
let dateTo = document.getElementById('dateTo');
let signUpForm = document.getElementById('rmsRegForm');
let username = document.getElementById('rmsUsername');
let email = document.getElementById('rmsEmail');
let companyId = document.getElementById('rmsCompanyId');
let isActive = document.getElementById('rmsActive');
let role = document.getElementById('rmsRole');
let signUpInfo;
let theBody;
  
function createResource(){
    theBody = {
        project_name:projectName.value,
        date_from:dateFrom.value,
        date_to:dateTo.value
    }
    rmsFetch('/auth/projects',"POST",theBody)
}
createProjectForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    createResource();
});

dateTo.addEventListener('input',(e)=>{
    let startDate, endDate;
    startDate = new Date(dateFrom.value);
    endDate = new Date(dateTo.value);
    startDate.setHours(0,0,0,0);
    endDate.setHours(0,0,0,0);
    if (endDate < startDate){
        document.getElementById('emailError').innerHTML =` Start date cannot be later than End date`;
        document.getElementById('submit').disabled = true;
    }
    else{
        document.getElementById('emailError').innerHTML =``;
        document.getElementById('submit').disabled = false;
        clearErrorDivs();
    }
})

emailInputListener(email);

function postSignUp(){
    signUpInfo = {
        email:email.value,
        username:username.value,
        companyId:companyId.value,
        role:role.value,
        isActive:isActive.value
    }
    rmsFetch('/auth/signup','POST',signUpInfo,'')
}

signUpForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    validateEmailData();
    showLoader();
    postSignUp();
});
