import {showLoader, rmsFileUpload} from './rmsModule.js'
import {clearErrorDivs} from './rmsModule.js'

let budgetDropDown = document.getElementById('rmsCreatorBudgetTag');
let paymentDropDown = document.getElementById('rmsCreatorPaymentTag');

// variables for budget file upload
let budgetUploadForm = document.getElementById('rmsBudgetForm');
let budgetInput = document.getElementById('budgetFile');
// payment file upload
let paymentUploadForm = document.getElementById('rmsPaymentForm');
let paymentInput = document.getElementById('paymentFile');


function uploadFile(drop_down,file_input,url,excelFile,theForm){
    const theProjectName = drop_down.value;
    const theFile = new FormData();
    theFile.append(excelFile,file_input.files[0]);
    theFile.append('projectName',theProjectName);
    rmsFileUpload(url,'POST',theFile,'',theForm)
}

budgetUploadForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    uploadFile(budgetDropDown,budgetInput,'/auth/upload/budget','budgetExcelFile','rmsBudgetForm');
});

paymentUploadForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    clearErrorDivs();
    showLoader();
    uploadFile(paymentDropDown,paymentInput,'/auth/upload/payments','paymentExcelFile','rmsPaymentForm');
})
