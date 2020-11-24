import {showLoader} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'

let createProjectForm = document.getElementById('rmsForm');
let projectName = document.getElementById('rmsProject');
let dateFrom = document.getElementById('dateFrom');
let dateTo = document.getElementById('dateTo');
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
    showLoader();
    createResource();
});


