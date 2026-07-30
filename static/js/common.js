function showLoader(){

const loader=document.getElementById("loader");

if(loader){

loader.style.display="block";

}

}

function hideLoader(){

const loader=document.getElementById("loader");

if(loader){

loader.style.display="none";

}

}

function showAlert(message,type="success"){

const alertBox=document.getElementById("alertBox");

if(alertBox){

alertBox.innerHTML=`

<div class="alert alert-${type} alert-dismissible fade show">

${message}

<button
class="btn-close"
data-bs-dismiss="alert">

</button>

</div>

`;

}

}