$(function(){  
  $('.slider-main').each(function(){
    const $main = $(this);
    const $wrap = $(this).parent('.slider-main_wrap');
    const $thumbs = $wrap.siblings('.slider-thumbs');
    
    $(this).find('img').each(function() {
      const $src = $(this).attr('src'),
            $alt = $(this).attr('alt');
      $thumbs.append(`<img src="${$src}" alt="${$alt}">`);
    });
    
    $(this).slick({
      arrows: false,
      asNavFor: $thumbs
    });
  });
  
  // Ajustando o slider-thumbs
  $('.slider-thumbs').each(function(){
    const $main = $(this).siblings('.slider-main_wrap').children('.slider-main');
    $(this).slick({
      focusOnSelect: true,
      arrows: false,
      asNavFor: $main,
      slidesToShow: 12      // sempre mostrar 2
    });
  });
});
