
/* JS for homepage.html */

console.log("hello world1")


function getLang() {
	l = getLang2();
	console.log(l);
}

function getLang2() {
	console.log("hello world2")
	if (navigator.languages != undefined)
		return navigator.languages[0];
	else
		return navigator.language;
	}
