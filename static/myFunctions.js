

function getButtonValue(){
	var x = document.getElementById("logoutBtn").value;
}


// function disableFunction(option){
// 	document.getElementsByName(option).disabled = true;
// }

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


function disableAllInputs(){
	// document.getElementsById("fltNo").disabled = true;
	// document.getElementById("memberNo").disabled = true;
	disableFlatInput();
	disableMemberInput();
}