import {clearErrorDivs} from './rmsModule.js'
import {validateEmailData, emailInputListener} from './rmsModule.js'
import {rmsFetch, showLoader, rmsFileUpload, rmsFetchGet } from './rmsModule.js'

let createProjectForm = document.getElementById('rmsForm');
let projectName = document.getElementById('rmsProject');
let dateFrom = document.getElementById('dateFrom');
let dateTo = document.getElementById('dateTo');
let signUpForm = document.getElementById('rmsRegForm');
let email = document.getElementById('rmsEmail');
let companyId = document.getElementById('rmsCompanyId');
let isActive = document.getElementById('rmsActive');
let role = document.getElementById('rmsRole');
let fetchEmployeesButton = document.getElementById("fetchButton");
let employeesView = document.getElementById("employeesView");
let fetchProjectsButton = document.getElementById("fetchProjectsButton");
let projectsView = document.getElementById("projectsView");
let employeeTable = document.getElementById('show_files');
let projectsTable = document.getElementById('list_projects');
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
    rmsFetch('/auth/projects',"POST",theBody,'','rmsForm')
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
        // username:username.value,
        companyId:companyId.value,
        role:role.value,
        isActive:isActive.value
    }
    rmsFetch('/auth/signup','POST',signUpInfo,'','rmsRegForm')
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
    rmsFileUpload('/auth/upload/employees','POST',theFile,'','rmsEmployeeFile')
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
    rmsFetch('/auth/suspend','POST',suspendBody,'','rmsSuspendForm')
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
    rmsFetch('/auth/reactivate','POST',reactivateBody,'','rmsReactivateForm')
}
reactivateForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    reactivateUser();
})
// fetch the employee master file from the database 
const employeesUrl = '/employees/'+companyId.value;
fetchEmployeesButton.addEventListener("click",()=>{
    showLoader();
    employeeTable.innerHTML = "";
    rmsFetchGet(employeesUrl,'',employeesView);
    }
    );

//fetch projects
const projectsUrl = '/projects/'+companyId.value
fetchProjectsButton.addEventListener("click", ()=>{
        showLoader();
        projectsTable.innerHTML = "";
        rmsFetchGet(projectsUrl,'',projectsView);
    }
    );