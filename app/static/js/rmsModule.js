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
function inputReset(){
  document.getElementById('rmsForm').reset();  
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
function showError(err){
  if (filename === 'dashboard'){
    showAlert(err);
  }
  else{
    document.getElementById('emailError').innerHTML = `${err}`;
  }
}
function showAlert(myData,divId){
  if (divId === 'success'){
    document.getElementById('success').style.display = " block";
    document.getElementById('success').innerHTML = `${myData} <span class="closebtn">&times;</span>`
  }
  else{
    document.getElementById('error').style.display = " block";
    document.getElementById('error').innerHTML = `${myData} <span class="closebtn">&times;</span>`
  }
  let close = document.getElementsByClassName("closebtn");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function(){
      var div = this.parentElement;
      div.style.opacity = "0";
      setTimeout(function(){ div.style.display = "none"; }, 600);
    }
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
export function rmsFetch(theUrl,theMethod,theBody, redirectUrl=""){
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
                inputReset();
                if (filename === 'dashboard'){
                  showAlert(data,'success');
                }
                else{
                  callToast(data,redirectUrl);
                }
                exitLoader();
              }
              else if(status === 400){
                showError(error,'error')
                exitLoader();
              }
              else if(status === 409){
                showError(error,'error');
                exitLoader();
              }
              else if(status === 401){
                showError(error,'error');
                exitLoader();
              }
              else if(status === 404){
                showError(error,'error');
                exitLoader();
              }
          })
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