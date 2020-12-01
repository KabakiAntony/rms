import {showLoader} from './rmsModule.js'
import {rmsFetch} from './rmsModule.js'
import {clearErrorDivs} from './rmsModule.js'

let createProjectForm = document.getElementById('rmsForm');
let projectName = document.getElementById('rmsProject');
let dateFrom = document.getElementById('dateFrom');
let dateTo = document.getElementById('dateTo');
let theBody;

function compareDates(dateOne, dateTwo){
    
  }
  
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


