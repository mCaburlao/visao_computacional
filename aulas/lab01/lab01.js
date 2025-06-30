$(function(){  
  $('.slider-main').each(function(i){
    const $main = $(this);
    const $wrap = $(this).closest('.slider-main_wrap');
    // Busca apenas o .slider-thumbs irmão mais próximo deste slider
    const $thumbs = $wrap.prev('.slider-thumbs').length ? $wrap.prev('.slider-thumbs') : $wrap.next('.slider-thumbs');

    // Limpa thumbs apenas deste slider
    $thumbs.empty();

    // Adiciona thumbs para este slider
    $main.find('img').each(function(idx) {
      const $src = $(this).attr('src'),
            $alt = $(this).attr('alt');
      $thumbs.append(`<img src="${$src}" alt="${$alt}" data-index="${idx}">`);
    });

    // Inicializa o slider principal
    $main.slick({
      arrows: false,
      dots: false
    });

    // Clique no thumb: vai para o slide correspondente
    $thumbs.on('click', 'img', function() {
      const idx = $(this).data('index');
      $main.slick('slickGoTo', idx);
    });

    // Destaca o thumb ativo
    $main.on('afterChange', function(event, slick, currentSlide){
      $thumbs.find('img').removeClass('active');
      $thumbs.find(`img[data-index="${currentSlide}"]`).addClass('active');
    });

    // Define o thumb inicial como ativo
    $thumbs.find('img').first().addClass('active');
  });

  // Remove Slick dos thumbs (caso já inicializado)
  $('.slider-thumbs').each(function(){
    if ($(this).hasClass('slick-initialized')) {
      $(this).slick('unslick');
    }
  });

  // Menu fixo responsivo
  function updateMenuPosition() {
    if (window.innerWidth < 768) {
      $('.container').css('top', '0');
    } else {
      $('.container').css('top', $(window).scrollTop() + 'px');
    }
  }
  $(window).on('scroll resize', updateMenuPosition);
  updateMenuPosition();
});