let filename= location.pathname.split('/').pop();

/* this is a module that will hold all data validations*/
function isEmail(my_email){
    let emailRegex =/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/igm;
    return my_email.match(emailRegex);
}
function isValidPassword(my_password){
    let passwordRegex = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){6,20}$/igm;
    return my_password.match(passwordRegex);
}
/* this function gets called on a status code of 200 or 201 */
function inputReset(theform){
 document.getElementById(theform).reset();  
}
function callToast(msg,redirectUrl) {
  let x = document.getElementById("showAlert");
  document.getElementById('showAlert').innerHTML = `${msg}`;
  x.className = "show";
  setTimeout(function(){ 
    x.className = x.className.replace("show", ""); 
    location.href= redirectUrl;
  }, 4000);
}
function exitLoader(){
  document.getElementById('showLoader').style.display = " none";
  document.getElementById('submit').style.display = " block";
}
function showError(err, errDiv){
  if (filename === 'dashboard'){
    showAlert(err,errDiv);
  }
  else{
    document.getElementById('emailError').innerHTML = `${err}`;
  }
}
function showAlert(myData,divId){
  if (divId === 'success'){
    document.getElementById('success').innerHTML = `${myData} <span class="closebtn">&times;</span>`;
    document.getElementById('success').style.display = " block";
    closeDiv(divId);
  }
  else {
    document.getElementById('error').innerHTML = `${myData} <span class="closebtn">&times;</span>`;
    document.getElementById('error').style.display = " block";
    closeDiv(divId);
  }
  let close = document.getElementsByClassName("closebtn");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function(){
      let div = this.parentElement;
      setTimeout(function(){ div.style.display = "none"; });
    }
}

}
function closeDiv(myDivId){
  setTimeout(function(){ 
    document.getElementById(myDivId).style.display = "none";
  }, 10000);
}
function showFilesData(files_data,viewDiv){
  for(let i=0; i < files_data.length;i++){
    viewDiv.innerHTML=`
    ${files_data.map(function(filesData){
      return `
        <table id="show_files">
          <tr>
          <td>${filesData.fileType}</td>
          <td>${filesData.project_name.split('.')[0]}</td>
          <td>${filesData.fileStatus}</td>
          <td>${filesData.fileAmount}</td>
          <td>${filesData.dateCreated}</td>
          <td><a href="uploads/${filesData.fileType.toLowerCase()}/${filesData.fileName}">Preview</a></td>
          </tr>
        </table>
                  `
        }).join('')}
    `
  }
}
function showProjectFilesData(files_data,viewDiv){
  for(let i=0; i < files_data.length;i++){
    viewDiv.innerHTML=`
    ${files_data.map(function(filesData){
      return `
        <table id="show_files">
          <tr>
          <td>${filesData.fileType}</td>
          <td>${filesData.fileStatus}</td>
          <td>${filesData.fileAmount}</td>
          <td>${filesData.dateCreated}</td>
          <td><a href="uploads/${filesData.fileType.toLowerCase()}/${filesData.fileName}">Preview</a></td>
          </tr>
        </table>
                  `
        }).join('')}
    `
  }
}
function showEmployeeData(employee_data,viewDiv){
  for (let i = 0; i < employee_data.length; i++) {
    viewDiv.innerHTML=`
      ${employee_data.map(function(employeeData){
        return `
      <table>
          <tr>
          <td>${employeeData.firstname +" "+ employeeData.lastname}</td>
          <td>${employeeData.email}</td>
          <td>${'+'+employeeData.mobile}</td>
          </tr>
        </table>
                    `
          }).join('')}
        `
    }
}
function showProjectData(project_data,viewDiv){
  for (let i = 0; i < project_data.length; i++) {
    viewDiv.innerHTML=`
      ${project_data.map(function(projectData){
        return `
            <table>
              <tr>
              <td>${projectData.project_name.split('.')[0]}</td>
              <td>${projectData.date_from}</td>
              <td>${projectData.date_to}</td>
              <td>${projectData.project_status}</td>
              </tr>
            </table>   
            `
          }).join('')}
        `
    }

}
/* this function validates data on submit */
export function validateEmailData(){
    if(!isEmail(rmsEmail.value)){
        document.getElementById("emailError").innerHTML = "Please enter a valid email address";
        return false;
    }
}
export function validatePasswordData(){
  if(!isValidPassword(rmsPassword.value)){
    document.getElementById("passwordError").innerHTML = 
    `Password should contain atleast 
    1 uppercase character,
    1 lowercase character,
    1 number, 
    1 special character,
    atleast 6 characters
    & not more than 20.`;
    return false;
}
}
/* this two functions below validate data as the user inputs */
export function emailInputListener(theEmailInput){
    theEmailInput.addEventListener('input',(e)=>{
        if(isEmail(theEmailInput.value)){
            document.getElementById("emailError").innerHTML = ""; 
        }
        else{
            document.getElementById("emailError").innerHTML = "Please enter a valid email address";
        }
    });
}
export function passwordInputListener(thePasswordInput){
  thePasswordInput.addEventListener('input',(e)=>{
    if(isValidPassword(thePasswordInput.value))
    {
        document.getElementById("passwordError").innerHTML = "";
    }else{
        document.getElementById("passwordError").innerHTML = 
        `Password should contain atleast 
        1 uppercase character,
        1 lowercase character,
        1 number, 
        1 special character,
        atleast 6 characters
        & not more than 20`;
    }
});
}
/* this is the fetch api for post, put, delete */
export function rmsFetch(theUrl,theMethod,theBody, redirectUrl="",theForm){
    fetch(theUrl,{
            method: theMethod,
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(theBody)
          })
          .then(response => response.json())
          .then(({data,status,error})=>{
              if(status === 201 || status === 200 || status === 202){
                // inputReset(theForm);
                if (filename === 'dashboard'){
                  showAlert(data,'success');
                }
                else{
                  callToast(data,redirectUrl);
                }
                exitLoader();
              }
              else {
                showError(error,'error')
                exitLoader();
              }
          })
          // remove console log at the end
          .catch(err => console.log(`This error occured :${err}`));
}
// this fetch uploads files
export function rmsFileUpload(theUrl,theMethod,theBody, redirectUrl="", theForm){
  fetch(theUrl,{
          method: theMethod,
          body:theBody
        })
        .then(response => response.json())
        .then(({data,status,error})=>{
            if(status === 201 || status === 200 || status === 202){
              inputReset(theForm);
              if (filename === 'dashboard'){
                showAlert(data,'success');
              }
              else{
                callToast(data,redirectUrl);
              }
              exitLoader();
            }
            else {
              showError(error,'error')
              exitLoader();
            }
        })
        // remove console log at the end
        .catch(err => console.log(`This error occured :${err}`));
}
export function rmsFetchGet(theUrl,redirectUrl="",theDiv){
  fetch(theUrl,{
    method: "GET",
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    },
  })
  .then(response => response.json())
  .then(({data,status,error})=>{
      if(status === 201 || status === 200 || status === 202){
        if (filename === 'dashboard'){
          if (theDiv.id == "employeesView"){
            showEmployeeData(data,theDiv);
          }
          else if(theDiv.id == "projectsView"){
            showProjectData(data,theDiv);
          }
          else if(theDiv.id == "listFiles"){
            showProjectFilesData(data,theDiv);
          }
          else if(theDiv.id == "authorizerViewFiles"){
            showFilesData(data,theDiv);
          }
          else{
            callToast(data,"");
          }
          
        }
        else{
          callToast(data,redirectUrl);
        }
        exitLoader();
      }
      else {
        showError(error,'error')
        exitLoader();
      }
  })
  // remove console log at the end
  .catch(err => console.log(`This error occured :${err}`));

}
export function showLoader(){
  document.getElementById('showLoader').style.display = " block";
  document.getElementById('submit').style.display = " none";
}
export function clearErrorDivs(){
  document.getElementById('success').style.display = " none";
  document.getElementById('error').style.display = " none";
}