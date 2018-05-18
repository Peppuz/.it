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
  let color = getCookie('text')
  let bg = getCookie('bg')
  element.style.setProperty("--main-color", color);
  element.style.setProperty('--main-bg-color', bg)
}

function changeTheme(val){
  let element = document.getElementById('main')
  element.style.setProperty("--main-bg-color", val);
  setCookie("bg",val)
}
function changeText(val){
  let element = document.getElementById('main')
  element.style.setProperty("--main-color", val);
  setCookie("text",val)
}


function showPickers(){
  let tap = document.getElementById('tap')
  let bg = document.getElementById('bg-picker')
  let text = document.getElementById('text-picker')

  if (tap.classList.contains('active')) {
    tap.classList.remove("active")
    tap.classList.add("hidden")

    bg.classList.add("active")
    bg.classList.remove("hidden")

    text.classList.add("active")
    text.classList.remove("hidden")
  }
  else {
      tap.classList.add("active")
      tap.classList.remove("hidden")

      bg.classList.remove("active")
      bg.classList.add("hidden")

      text.classList.remove("active")
      text.classList.add("hidden")
  }
}
