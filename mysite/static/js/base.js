document.addEventListener("DOMContentLoaded", function(){
  var container = document.querySelector('.callback-popup-container')
  var Buttons = document.querySelectorAll('.callback-popup');
  for (let i = 0; i < Buttons.length; i++) {
    Buttons[i].addEventListener('click', function(){
      container.style.display = 'flex';
    });
  }
  container.addEventListener('click', function(event){
    if(event.target == container){
      container.style.display = 'none';
    }
  });
});


document.addEventListener("DOMContentLoaded", function(){
  var container = document.querySelector('.profile__avatar-popup-edit')
  var Button = document.querySelector('.avatar-edit-popup');
  document.addEventListener('click', function(event){
    if (event.composedPath().includes(Button)) {
      container.style.display = 'flex';
    } 
    else {
      container.style.display = 'none';
    }
  });
});


document.addEventListener("DOMContentLoaded", function(){
  var container = document.querySelector('.header__main-tooltip')
  var Button = document.querySelector('.header__main-link');
  Button.addEventListener("mouseover", show_func, True);
  Button.addEventListener("mouseout", hide_func, True);

  function show_func(){ 
    container.style.display = 'flex';
  }
  function hide_func(){ 
    container.style.display = 'none';
  }
});






document.addEventListener("DOMContentLoaded", function(){
  var container = document.querySelector('.main__slider-container-slides')
  var NextButton = document.querySelector('.main__slider-button-next');
  var PrevButton = document.querySelector('.main__slider-button-prev');
  var NextElement = document.getElementById("NextBTN");
  var PrevElement = document.getElementById("PrevBTN");
  var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  let lastTranslateX = 0;
  
  if (lastTranslateX == 0) {
    PrevElement.disabled = true;
  }

  document.addEventListener('click', function(event){
    if (event.composedPath().includes(NextButton)) {
      PrevElement.disabled = false;
      lastTranslateX -= 201;
      container.style.transform = "translateX(" + (lastTranslateX) + "px)";
      if (width <= 940) {
        if (lastTranslateX <= -804) {
          NextElement.disabled = true;
        }
      }
      else if (width <= 1150) {
        if (lastTranslateX <= -603) {
          NextElement.disabled = true;
        }
      }
      else if (width <= 1350) {
        if (lastTranslateX <= -402) {
          NextElement.disabled = true;
        }
      }
      else {
        if (lastTranslateX <= -201) {
          NextElement.disabled = true;
        }
      }
    } 
    if (event.composedPath().includes(PrevButton)) {
      NextElement.disabled = false;
      lastTranslateX += 201;
      container.style.transform = "translateX(" + (lastTranslateX) + "px)";
      if (lastTranslateX >= 0) {
        PrevElement.disabled = true;
      }
    }
  });

});

