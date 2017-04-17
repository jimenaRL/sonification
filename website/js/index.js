var vid = document.getElementById("bgvid");
// var pauseButton = document.querySelector(".notes button");
var transportButton = document.getElementById("transport");
var volumeButton = document.getElementById("volume");


if (window.matchMedia('(prefers-reduced-motion)').matches) {
    vid.removeAttribute("autoplay");
    vid.pause();
    transportButton.innerHTML = "▶";
}

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