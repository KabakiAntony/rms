/* handle signing out here */
let signOut = document.getElementById('signout-button');

signOut.addEventListener('click', (e)=>{
    e.preventDefault();
    SignOut();
});

function SignOut(){
    fetch(`/auth/signout`)
    .then(response =>response.json())
    .then(({data,status}) => {
        if (status === 200){
            location.href='/signin';
        }
    })
    .catch(err => console.log(err));
}