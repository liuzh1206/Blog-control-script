//add chartjs and mermaid support
var contents = document.getElementsByClassName("chart");
var len = contents.length;
for (i = 0; i < len; i++) {
	var charts_pre = contents[i];
	var code = charts_pre.getElementsByTagName("code")[0];
	var content = code.innerHTML;
	charts_pre.removeChild(code)
	var can = document.createElement("canvas");
	charts_pre.appendChild(can);
	var ctx = can.getContext('2d');
	content = JSON.parse(content)
	var chart = new Chart(ctx, content);
}
var contents = document.getElementsByClassName("mermaid");
var len = contents.length;
for (i = 0; i < len; i++) {
	var mer_pre = contents[i];
	mer_pre.style.display = 'block';
	mer_pre.style.overflow = 'auto'
	var code = mer_pre.getElementsByTagName("code")[0];
	var content = code.innerHTML;
	mer_pre.removeChild(code);
	mer_pre.innerHTML = content;

}


// add change theme function
var title = document.getElementById('title-block-header');
var changeTheme = document.createElement('div');
var changeThemeButton = document.createElement('input');
changeThemeButton.type = 'checkbox';

var changeThemeText = document.createElement('span');
changeThemeText.innerHTML = '暗色模式';
theme = sessionStorage.getItem('theme');

themeLink = document.getElementsByTagName('link')[0];
if (theme == 'panda') {
	themeLink.href = '/static/css/panda/panda.css';
} else if (theme == 'markdown') {
	themeLink.href = '/static/css/markdown/markdown.css';
}

if (themeLink.href == document.location.origin + '/static/css/panda/panda.css') {
	changeThemeButton.checked = true;
} else if (themeLink.href == document.location.origin + '/static/css/markdown/markdown.css') {
	changeThemeButton.checked = false;
}


changeTheme.appendChild(changeThemeText);
changeTheme.appendChild(changeThemeButton);

changeTheme.style.float = 'right';

document.body.insertBefore(changeTheme, title);

changeThemeButton.onchange = function () {
	if (changeThemeButton.checked) {
		var link = document.getElementsByTagName('link')[0];
		link.href = '/static/css/panda/panda.css'
		sessionStorage.setItem('theme', 'panda');

	} else {
		var link = document.getElementsByTagName('link')[0];
		link.href = '/static/css/markdown/markdown.css';
		sessionStorage.setItem('theme', 'markdown');
	}

}



//add comment and bilibiliEmoji form https://github.com/lrhtony/BiliEmoji
var emojiXmlhttp;
var emojiMap = "";
if (window.XMLHttpRequest) {
	emojiXmlhttp = new XMLHttpRequest();
}
else {
	emojiXmlhttp = new ActiveXObject('Microsoft.XMLHTTP')
}
emojiXmlhttp.onreadystatechange = function () {
	if (emojiXmlhttp.readyState == 4 && emojiXmlhttp.status == 200) {
		emojiMap = emojiXmlhttp.responseText;
		emojiMap = JSON.parse(emojiMap);
		new Valine({
			el: '#vcomments',
			appId: 'vrqqWR4cjq8K7TLU7JhzjjME-9Nh9j0Va',
			appKey: 'MRzqDxg1bHE1BNS53lwYAL7O',
			avatar: 'robohash',
			enableQQ: true,
			// visitor: true
			emojiMaps: emojiMap
		})
	}
}
emojiXmlhttp.open('GET', '/biliEmoji.json');
emojiXmlhttp.send();



//add back top button
function addBackTopButton() {
	var topButton = document.createElement('a');
	var divTopShape = document.createElement('div');

	divTopShape.style.borderLeft = '5px white solid';
	divTopShape.style.borderTop = '5px white solid';
	divTopShape.style.width = '25px';
	divTopShape.style.height = '25px';
	divTopShape.style.position = 'relative';
	divTopShape.style.top = '18px';
	divTopShape.style.left = '13px';
	divTopShape.style.transform = 'rotate(45deg)';

	topButton.appendChild(divTopShape);

	topButton.style.width = '50px';
	topButton.style.height = '50px';
	topButton.style.background = 'gray';
	topButton.style.borderRadius = '10px';
	topButton.style.position = 'fixed';
	topButton.style.right = '80px';
	topButton.style.bottom = '100px';
	topButton.style.display = 'block';
	topButton.style.zIndex = '999';
	topButton.style.opacity = ((document.documentElement.scrollTop - 2) / 50) > 0.8 ? 0.5 : ((document.documentElement.scrollTop - 2) / 50);
	topButton.onclick = async function () {
		// document.documentElement.scrollTop=0;
		// divTop.style.display = 'none';
		// var height = document.documentElement.scrollTop
		while (document.documentElement.scrollTop > 0) {
			await sleep(1)
			window.scrollTo(0, document.documentElement.scrollTop - document.documentElement.scrollTop / 4);
		}
	}
	return topButton
}


function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}


var divTop = addBackTopButton();
document.body.appendChild(divTop);
window.onscroll = function () {
	if (document.documentElement.scrollTop < 40) {
		divTop.style.display = 'none';
	} else {
		divTop.style.display = 'block';
		if ((document.documentElement.scrollTop - 40) / 10 < 0.5) {
			divTop.style.opacity = (document.documentElement.scrollTop - 40) / 10;
		} else {
			divTop.style.opacity = 0.5;
		}
	}
}

//add back index page button
function addBackIndexButton() {
	var indexButton = document.createElement('a');
	var indexText = document.createElement('span');
	indexButton.appendChild(indexText);
	indexButton.href = '/';

	indexText.innerHTML = '回到首页'
	indexText.style.color = 'white'
	indexText.style.fontSize = '15px';
	indexText.style.margin = '3px 0 0 10px';
	indexText.style.display = 'inline-block'

	indexButton.style.width = '50px';
	indexButton.style.height = '50px';
	indexButton.style.background = 'gray';
	indexButton.style.borderRadius = '10px';
	indexButton.style.position = 'fixed';
	indexButton.style.right = '80px';
	indexButton.style.bottom = '150px';
	indexButton.style.display = 'block';
	indexButton.style.zIndex = '999';
	indexButton.style.opacity = 0.5;

	return indexButton
}
document.body.appendChild(addBackIndexButton());
