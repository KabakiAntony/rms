function openAction(evt, actionName) {
    let i, actioncontent, actionlinks;
    actioncontent = document.getElementsByClassName("actionContent");
    for (i = 0; i < actioncontent.length; i++) {
        actioncontent[i].style.display = "none";
    }
    actionlinks = document.getElementsByClassName("action-links");
    for (i = 0; i < actionlinks.length; i++) {
        actionlinks[i].className = actionlinks[i].className.replace(" active", "");
    }
    document.getElementById(actionName).style.display = "block";
    document.getElementById('profileInstruction').style.display = "none";
    evt.currentTarget.className += " active";
    
    if (actionName === "UploadPayment" || actionName === "UploadBudget" || actionName === "ViewFiles"){
        getProject(actionName);
        console.log(actionName);
    }
  }


let budgetDropDown = document.getElementById('rmsCreatorBudgetTag');
let paymentDropDown = document.getElementById('rmsCreatorPaymentTag');
let filesDropDown = document.getElementById('rmsCreatorSelectProject');
let defaultOption = document.createElement('option');
defaultOption.text = 'Select project';
let companyId = document.getElementById('rmsCreatorBudgetCompanyId');

// we are hooking the fetch projects to the tab the user is on
// determine the the open tab then cascade the  dropdown accordingly

function getProject(theTab){
    let dropDown = null;

    if (theTab === "UploadPayment"){
        dropDown = paymentDropDown;
    }
    if(theTab === "UploadBudget"){
        dropDown = budgetDropDown;
    }
    if (theTab === "ViewFiles"){
        console.log(theTab)
        dropDown = filesDropDown;
    }

    dropDown.length = 0 ;
    dropDown.add(defaultOption);
    dropDown.selectedIndex = 0;

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
}