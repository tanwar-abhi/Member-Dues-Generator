const { NONAME } = require("dns");


function getButtonValue(){
	var x = document.getElementById("logoutBtn").value;
}


// function disableFunction(option){
// 	document.getElementsByName(option).disabled = true;
// }

function enableAllInputs(){
	enableFlatInput();
	enableMemberInput();
}


function enableFlatInput(){
	document.getElementById("fltNo").removeAttribute("disabled");
}


function enableMemberInput(){
	document.getElementById("memberNo").removeAttribute("disabled");
}


function disableMemberInput(){
	document.getElementById("memberNo").disabled = true;
	enableFlatInput();
}

function disableFlatInput(){
	document.getElementById("fltNo").disabled = true;
	enableMemberInput();
}


function disableAllInputs(argParameter){

	docuement.getElementById(argParameter).value = "All";
	// docuement.getElementById(argParameter).setAttribute("value", "All");

	document.getElementById("fltNo").disabled = true;
	document.getElementById("memberNo").disabled = true;
}



function disableAllInputs(){
	document.getElementById("fltNo").disabled = true;
	document.getElementById("memberNo").disabled = true;
}



function displayFlatNoInput(){
	let textbox = document.getElementById("fltNo");
	textbox.style.display = "block";
}

function disapayMemberNoInput(){
	let textbox = document.getElementById("memeberNo");
	textbox.style.display = "block";
	// style="display: none;
}

// function alertFailedUpload(data){
// 	if (data.uploadSuccess === false){
// 		alert("This file extension is not allowed.\nPlease upload only .xls* or .pdf files")
// 	}
// }