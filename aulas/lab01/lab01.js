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
});