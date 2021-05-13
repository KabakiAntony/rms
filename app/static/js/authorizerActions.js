import { showLoader, rmsFetchGet } from './rmsModule.js'

let selectFileType = document.getElementById('rmsFileType');
let companyId = document.getElementById('rmsCompanyId');
let listFiles = document.getElementById('authorizerViewFiles');
let project_files = document.getElementById('show_files');


selectFileType.addEventListener('change',()=>{
    showLoader();
    project_files.innerHTML = "";
    let filesUrl = `/auth/files/${companyId.value}/${selectFileType.value}`;
    rmsFetchGet(filesUrl,"",listFiles)
})


