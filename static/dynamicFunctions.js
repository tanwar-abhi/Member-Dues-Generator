
// const { NONAME } = require("dns");

// const { NONAME } = require("dns");


function getButtonValue(){
	var x = document.getElementById("logoutBtn").value;
}


// function disableFunction(option){
// 	document.getElementsByName(option).disabled = true;
// }

// function enableAllInputs(){
// 	enableFlatInput();
// 	enableMemberInput();
// }


// function enableFlatInput(){
// 	document.getElementById("fltNo").removeAttribute("disabled");
// }


// function enableMemberInput(){
// 	document.getElementById("memberNo").removeAttribute("disabled");
// }


// function disableMemberInput(){
// 	document.getElementById("memberNo").disabled = true;
// 	enableFlatInput();
// }

// function disableFlatInput(){
// 	document.getElementById("fltNo").disabled = true;
// 	enableMemberInput();
// }


// function disableAllInputs(argParameter){

// 	docuement.getElementById(argParameter).value = "All";
// 	// docuement.getElementById(argParameter).setAttribute("value", "All");

// 	document.getElementById("fltNo").disabled = true;
// 	document.getElementById("memberNo").disabled = true;
// }


// function disableAllInputs(){
// 	document.getElementById("fltNo").disabled = true;
// 	document.getElementById("memberNo").disabled = true;
// }


function allInputsHidden(){
	document.getElementById('ifFlatNoSelected').style.visibility = 'hidden';
	document.getElementById('ifMemberNoSelected').style.visibility = 'hidden';
	document.getElementById('textboxFlat').value = "All";
	document.getElementById("textboxMember").value = "All";
}


function displayFlatInput(){
	document.getElementById('textboxFlat').value = "";
	if (document.getElementById('flatSelected').checked){
		document.getElementById('ifFlatNoSelected').style.visibility = 'visible';
		document.getElementById('ifMemberNoSelected').style.visibility = 'hidden';
		document.getElementById("textboxMember").value = "All"
	}
}


function disapayMemberInput(){
	document.getElementById('textboxMember').value = "";
	if (document.getElementById('memberSelected').checked){
		document.getElementById('ifMemberNoSelected').style.visibility = 'visible';
		document.getElementById('ifFlatNoSelected').style.visibility = 'hidden';
		document.getElementById('textboxFlat').value = "All";
	}
}


// function alertFailedUpload(data){
// 	if (data.uploadSuccess === false){
// 		alert("This file extension is not allowed.\nPlease upload only .xls* or .pdf files")
// 	}
// }