var vid = document.getElementById("bgvid");
// var pauseButton = document.querySelector(".notes button");
var transportButton = document.getElementById("transport");
var volumeButton = document.getElementById("volume");


// if (window.matchMedia('(prefers-reduced-motion)').matches) {
//     vid.removeAttribute("autoplay");
//     vid.pause();
//     transportButton.innerHTML = "▶";
// }

function vidFade() {
  vid.classList.add("stopfade");
}

vid.addEventListener('ended', function()
{
// only functional if "loop" is removed
vid.pause();
// to capture IE10
vidFade();
});


transportButton.addEventListener("click", function() {
  vid.classList.toggle("stopvolume");
  if (vid.paused) {
    vid.play();
    transportButton.innerHTML = "❚❚";
  } else {
    vid.pause();
    transportButton.innerHTML = "▶";
  }
});

volumeButton.addEventListener("click", function() {
  if (vid.muted) {
    vid.muted = false;
    volumeButton.innerHTML = '<i class="fa fa-volume-up audio-control"></i>';
  } else {
    vid.muted = true;
    volumeButton.innerHTML = '<i class="fa fa-volume-off audio-control"></i>';
  }
});



// based on Todd Motto functions
// http://toddmotto.com/labs/reusable-js/

// hasClass
function hasClass(elem, className) {
    return new RegExp(' ' + className + ' ').test(' ' + elem.className + ' ');
}
// addClass
function addClass(elem, className) {
    if (!hasClass(elem, className)) {
        elem.className += ' ' + className;
    }
}
// removeClass
function removeClass(elem, className) {
    var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ') + ' ';
    if (hasClass(elem, className)) {
        while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
            newClass = newClass.replace(' ' + className + ' ', ' ');
        }
        elem.className = newClass.replace(/^\s+|\s+$/g, '');
    }
}
// toggleClass
function toggleClass(elem, className) {
    var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, " " ) + ' ';
    if (hasClass(elem, className)) {
        while (newClass.indexOf(" " + className + " ") >= 0 ) {
            newClass = newClass.replace( " " + className + " " , " " );
        }
        elem.className = newClass.replace(/^\s+|\s+$/g, '');
    } else {
        elem.className += ' ' + className;
    }
}

var theToggle = document.getElementById('toggle');

theToggle.onclick = function() {
   toggleClass(this, 'on');
   return false;
};

var onload_toggleClass = function(){
    toggleClass(theToggle, 'on');
};

window.onload = function() {
  setTimeout(onload_toggleClass, 20000);
};
