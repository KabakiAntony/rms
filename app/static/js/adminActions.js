import {clearErrorDivs} from './rmsModule.js'
import {validateEmailData, emailInputListener} from './rmsModule.js'
import {rmsFetch, showLoader, rmsFileUpload} from './rmsModule.js'

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
// the following part goes into employee file upload
let fileUploadForm = document.getElementById('rmsEmployeeFile');
let fileInput = document.getElementById('employeeFile');
// the below variables go into suspend form
let suspendForm = document.getElementById('rmsSuspendForm');
let suspendEmail = document.getElementById('rmsSuspendEmail');
let suspendBody;
// variables for the reactivation form
let reactivateForm = document.getElementById('rmsReactivateForm');
let reactivateEmail = document.getElementById('rmsReactivateEmail');
let reactivateBody;

// project creation  
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

// system user creation
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
// master file upload
function uploadEmployeeFile(){
    const theFile = new FormData();
    theFile.append('employeeExcelFile',fileInput.files[0]);
    rmsFileUpload('/auth/upload/employees','POST',theFile,'')
}

fileUploadForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    uploadEmployeeFile();
});
// suspend user
emailInputListener(suspendEmail);

function suspendUser(){
    suspendBody = {
        email:suspendEmail.value
    }
    rmsFetch('/auth/suspend','POST',suspendBody,'')
}
suspendForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    suspendUser();
})
// reactivate user
emailInputListener(reactivateEmail);
function reactivateUser(){
    reactivateBody = {
        email:reactivateEmail.value
    }
    rmsFetch('/auth/reactivate','POST',reactivateBody,'')
}
reactivateForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    reactivateUser();
})