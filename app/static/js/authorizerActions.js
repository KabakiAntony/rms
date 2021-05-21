import { showLoader, rmsFetchGet, rmsFetch, remove_row_highlight } from './rmsModule.js'

let selectFileType = document.getElementById('rmsFileType');
let companyId = document.getElementById('rmsCompanyId');
let listFiles = document.getElementById('authorizerViewFiles');
let project_files = document.getElementById('show_files');
let fileId = document.getElementById('rmsFileId');
let authorizeButton = document.getElementById('authorizeFile');
let rejectButton = document.getElementById("rejectFile");
let authorizeBody = "",  rejectBody="";

selectFileType.addEventListener('change',()=>{
    if (selectFileType.value != "none"){
        showLoader();
        project_files.innerHTML = "";
        let filesUrl = `/auth/files/${companyId.value}/${selectFileType.value}`;
        rmsFetchGet(filesUrl,"",listFiles);
    }
})

function show_error_notification(errorMsg){
    document.getElementById('error').innerHTML = `${errorMsg}`;
    document.getElementById('error').style.display = " block";
    setTimeout(function(){ 
        document.getElementById('error').style.display = "none";
    }, 10000);
    
}
function authorization_rejection_action(actionBody){
    if (fileId.value ===""){
        let error = "Select the file you want to authorize on the table";
        show_error_notification(error);
    }
    else {
        showLoader();
        let patch_url = `/action/files/${fileId.value}`;
        rmsFetch(patch_url,'PATCH',actionBody,'','')
        fileId.value = "";
        remove_row_highlight();
        setTimeout(()=>{ 
            project_files.innerHTML="";
            selectFileType.selectedIndex = 0;
        },10000);
    }
}

authorizeButton.addEventListener('click', ()=>{
    authorizeBody = {
        new_status:"Authorized",
    }
    authorization_rejection_action(authorizeBody);
})

rejectButton.addEventListener('click', ()=>{
    rejectBody = {
        new_status:"Rejected",
    }
    authorization_rejection_action(rejectBody);
})




