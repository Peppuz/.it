/*
 * pz_tools.js
 *   A DOM using cookies as storage for theme settings and colors
 *   List of functions:
 *    ~ setCookie: recieves the identifier and the new value, than stores the cookie
 *    ~ getCookie: returns the value from recieved identifier
 *    ~ onLoadTheme: renders all colors according on CSS vars
 *    ~ changeTheme: recieves an integer, and loads new theme
 *    ~ changeText &: recieves
 * Peppuz (me@peppuz.it) - WTF Licence
 */

function setCookie(id,value) {
    var expires = "";
    var date = new Date();
    date.setTime(date.getTime() + (30*24*60*60*1000));
    expires = "; expires=" + date.toUTCString();
    document.cookie = id + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(id) {
    var idEQ = id + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(idEQ) == 0) return c.substring(idEQ.length,c.length);
    }
    return null;
}

function onLoadTheme(){
  let rt = getCookie('text-r')
  let gt = getCookie('text-g')
  let bt = getCookie('text-b')
  let rbg = getCookie('bg-r')
  let gbg = getCookie('bg-g')
  let bbg = getCookie('bg-b')

  let color = `${rt},${gt},${bt}`
  let bg = `${rbg},${gbg},${bbg}`
  let element  = document.getElementById('main')

  element.style.setProperty("--main-bg-color", `rgb(${bg})`);
  element.style.setProperty("--main-color", `rgb(${color})`);
}

function setText(where, val){
  setCookie(`text-${where}`, val)
  onLoadTheme()
}

function setBg(id,val) {
  setCookie(`bg-${id}`, val)
  onLoadTheme()
}

function setTheme(val){
  let rt= ""
  let gt= ""
  let bt= ""
  let rbg= ""
  let gbg= ""
  let bbg= ""
  switch (val) { // text & bg
    case 1: // red & black
      rt= "255"
      gt= "0"
      bt= "0"
      rbg= "0"
      gbg= "0"
      bbg= "0"
      break;
    case 2: // black & red
      rt= "0"
      gt= "0"
      bt= "0"
      rbg= "255"
      gbg= "0"
      bbg= "0"
      break;
    case 3: // yellow & blue
      rt= "255"
      gt= "255"
      bt= "0"
      rbg= "0"
      gbg= "0"
      bbg= "255"
      break;
    case 4: // black & green
      rt= "0"
      gt= "0"
      bt= "0"
      rbg= "0"
      gbg= "255"
      bbg= "0"
      break;

    default:
      return console.error("default call on setTheme");
  }


  setCookie("text-r", rt)
  setCookie("text-g", gt)
  setCookie("text-b", bt)
  setCookie("bg-r", rbg)
  setCookie("bg-g", gbg)
  setCookie("bg-b", bbg)
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
