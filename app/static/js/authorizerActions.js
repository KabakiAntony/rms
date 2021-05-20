import { showLoader, rmsFetchGet, rmsFetch, remove_row_highlight } from './rmsModule.js'

let selectFileType = document.getElementById('rmsFileType');
let companyId = document.getElementById('rmsCompanyId');
let listFiles = document.getElementById('authorizerViewFiles');
let project_files = document.getElementById('show_files');
let fileId = document.getElementById('rmsFileId');
let authorizeButton = document.getElementById('authorizeFile');
let rejectButton = document.getElementById("rejectFile");
let authorizeBody = "";

selectFileType.addEventListener('change',()=>{
    showLoader();
    project_files.innerHTML = "";
    let filesUrl = `/auth/files/${companyId.value}/${selectFileType.value}`;
    rmsFetchGet(filesUrl,"",listFiles)
})

authorizeButton.addEventListener('click', ()=>{
    authorizeBody = {
        new_status:"Authorized",
    }
    if (fileId.value ==""){
        alert("Select the file you want to authorize.");
    }
    else{
        showLoader();
        let patch_url = `/action/files/${fileId.value}`;
        rmsFetch(patch_url,'PATCH',authorizeBody,'','')
        fileId.value = "";
        remove_row_highlight();
    }
})





