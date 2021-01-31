theme = sessionStorage.getItem('theme');

themeLink = document.getElementsByTagName('link')[0];
if (theme != null) {
	themeLink.href = '/static/css/' + theme + '/' + theme + '.css';
}
