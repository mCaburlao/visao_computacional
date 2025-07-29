$(function(){  
  $('.slider-main').each(function(){
    const $main = $(this);
    const $wrap = $(this).parent('.slider-main_wrap');
    const $thumbs = $wrap.siblings('.slider-thumbs');
    
    // Clear thumbs in case of re-init
    $thumbs.empty();

    // Add thumbs
    $(this).find('img').each(function(idx) {
      const $src = $(this).attr('src'),
            $alt = $(this).attr('alt');
      $thumbs.append(`<img src="${$src}" alt="${$alt}" data-index="${idx}">`);
    });

    // Init main slider
    $main.slick({
      arrows: false,
      dots: false,
      // Remove asNavFor
      // asNavFor: $thumbs
    });

    // Thumb click: go to slide
    $thumbs.on('click', 'img', function() {
      const idx = $(this).data('index');
      $main.slick('slickGoTo', idx);
    });

    // Highlight active thumb
    $main.on('afterChange', function(event, slick, currentSlide){
      $thumbs.find('img').removeClass('active');
      $thumbs.find(`img[data-index="${currentSlide}"]`).addClass('active');
    });

    // Set initial active thumb
    $thumbs.find('img').first().addClass('active');
  });

  // Remove Slick from thumbs (if previously initialized)
  $('.slider-thumbs').each(function(){
    if ($(this).hasClass('slick-initialized')) {
      $(this).slick('unslick');
    }
  });

  // Make the menu container follow the user's scrolling (fluid and mobile-friendly)
  function updateMenuPosition() {
    // Only apply on desktop (fixed menu), not on mobile where menu is overlay
    if (window.innerWidth < 768) {
      $('.container').css('top', '0');
    } else {
      $('.container').css('top', $(window).scrollTop() + 'px');
    }
  }
  $(window).on('scroll resize', updateMenuPosition);
  updateMenuPosition();
});

// Add JavaScript - para passar slide

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (slides.length === 0) return; // Guard: no slides
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  if (dots[slideIndex-1]) {
    dots[slideIndex-1].className += " active";
  }
}

document.addEventListener("DOMContentLoaded", function() {
  showSlides(slideIndex);

  // Fullscreen functionality for slideshow
  const fsBtn = document.getElementById("fullscreen-btn");
  const slideshow = document.getElementById("slideshow-container");

  if (fsBtn && slideshow) {
    fsBtn.addEventListener("click", function() {
      if (
        document.fullscreenElement === slideshow ||
        document.webkitFullscreenElement === slideshow
      ) {
        // Exit fullscreen
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        }
      } else {
        // Enter fullscreen
        if (slideshow.requestFullscreen) {
          slideshow.requestFullscreen();
        } else if (slideshow.webkitRequestFullscreen) {
          slideshow.webkitRequestFullscreen();
        }
      }
    });
  }
});

function abrirPopup(id) {
      document.getElementById(id).style.display = 'flex';
    }

    function fecharPopup(id) {
      document.getElementById(id).style.display = 'none';
    }