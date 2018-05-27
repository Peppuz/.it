function setCookie(name,value) {
    var expires = "";
    var date = new Date();
    date.setTime(date.getTime() + (30*24*60*60*1000));
    expires = "; expires=" + date.toUTCString();
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function onLoadTheme(){
  let element  = document.getElementById('main')
  let bg = getCookie('bg')
  if (bg == null)
    bg = '0'
  let hue = `hsl(${bg}, 100%, 50%)`
  console.log(hue);
  element.style.setProperty("--main-bg-color", hue);

  let r = getCookie('text-r')
  let g = getCookie('text-g')
  let b = getCookie('text-b')
  let color = `rgb(${r},${g},${b})`
  if (r == null)
    color = 'rgb(0,0,0)'
  console.log(color);
  element.style.setProperty("--main-color", color);

}

function changeTheme(val){
  setCookie("bg",val)
  onLoadTheme()
}
function changeText(where, val){
  let element = document.getElementById('main')
  setCookie(`text-${where}`, val)
  onLoadTheme()
}
function showPickers(){
  let tap = document.getElementById('tap')
  let theme = document.getElementById('theme-div')
  if (tap.innerHTML == 'tap me ! &gt;') {
    tap.innerHTML = 'tap to close ! >';
    theme.classList.add("active")
    theme.classList.remove("hidden")
  }
  else {
    tap.innerHTML = 'tap me ! >';
    theme.classList.remove("active")
    theme.classList.add("hidden")
  }
}
