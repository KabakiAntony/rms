import {showLoader, rmsFileUpload} from './rmsModule.js'
import {clearErrorDivs} from './rmsModule.js'

let companyId = document.getElementById('rmsCreatorBudgetCompanyId');
let dropDown = document.getElementById('rmsCreatorBudgetTag');
let defaultOption = document.createElement('option');
defaultOption.text = 'Select project';
dropDown.length = 0 ;
dropDown.add(defaultOption);
dropDown.selectedIndex = 0;
// variables for budget file upload
let budgetUploadForm = document.getElementById('rmsBudgetForm');
let budgetInput = document.getElementById('budgetFile');

// getting project data from the db
const url = 'projects/name/'+companyId.value;

fetch(url,{
        method: "GET"
      })
      .then(response => response.json())
      .then(({data,status,error})=>{
          let option;
          let name_only;
          if (status == 200)
          {
            for (let i = 0; i < data.length; i++) {
                option = document.createElement('option');
                name_only = data[i].project_name.split('.')[0] 
                option.text = name_only;
                dropDown.add(option);
              }
          }
          else
          {
              console.log(`an error occured ${error}`)
          }

      })
    .catch(err => console.log(`This error occured :${err}`));

// budget file upload
function uploadBudgetFile(){
    const theProjectName = dropDown.value;
    const theFile = new FormData();
    theFile.append('budgetExcelFile',budgetInput.files[0]);
    theFile.append('projectName',theProjectName);
    rmsFileUpload('/auth/upload/budget','POST',theFile,'','rmsBudgetForm')
}

budgetUploadForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    uploadBudgetFile();
});
