import { showLoader, rmsFetchGet } from './rmsModule.js'

let selectFileType = document.getElementById('rmsFileType');
let companyId = document.getElementById('rmsCompanyId');
let listFiles = document.getElementById('authorizerViewFiles');


selectFileType.addEventListener('change',()=>{
    document.getElementById('authorizerViewFiles').innerHTML = "";
    showLoader();
    let filesUrl = `/auth/files/${companyId.value}/${selectFileType.value}`;
    rmsFetchGet(filesUrl,"",listFiles)
})



