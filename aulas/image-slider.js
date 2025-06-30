class ImageSlider extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() {
    const images = JSON.parse(this.getAttribute('images') || '[]');
    console.log('Images:', images);
    const style = `
      <style>
.slider-main_wrap { position: relative;
    max-width: 600px;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;  overflow: hidden;
}
.slider-main_wrap,.slider-thumbs { 
    margin-left: auto;
    margin-right: auto;
    display: block;
    text-align: center;
    max-width: 600px; 
}
        .slider-thumbs img { width: 60px; height: 40px; object-fit: cover; cursor: pointer; border: 2px solid transparent; }
        .slider-thumbs img.active { border-color: #e91e63; }
        .slider-main img { width: 100%; max-height: 300px; object-fit: contain;  }
        .arrow_box { display: none; }
.slider-thumbs .slick-slide {
    width: 8% !important;
    height: auto;
    cursor: pointer;

    img {
        border-radius: 5px;
    }

    &:not(:nth-of-type(5n)) {
        padding-right: 2.5%;
    }
}
.slider-thumbs img {
    opacity: 0.7;
    cursor: pointer;
    margin-right: 5px;
    border-radius: 5px;
    transition: opacity 0.2s, border 0.2s;
    max-height: 50px;
    max-width: 50px;
}
.slick-track:after,
.slick-track:before {
    content: none;
}
      </style>
    `;
    const thumbs = images.map((img, i) =>
      `<img src="${img.src}" alt="${img.alt}" data-index="${i}">`
    ).join('');
    const slides = images.map(img =>
      `<img src="${img.src}" alt="${img.alt}">`
    ).join('');
    this.shadowRoot.innerHTML = `
      ${style}
      <div class="slider-thumbs">${thumbs}</div>
      <div class="slider-main_wrap">
        <div class="slider-main">${slides}</div>
        <div class="arrow_box"></div>
      </div>
    `;
    // Carrega Slick do host
    const $main = $(this.shadowRoot.querySelector('.slider-main'));
    const $thumbs = $(this.shadowRoot.querySelector('.slider-thumbs'));
    $main.slick({ arrows: false, dots: false });
    $thumbs.on('click', 'img', function() {
      $main.slick('slickGoTo', $(this).data('index'));
    });
    $main.on('afterChange', function(event, slick, currentSlide){
      $thumbs.find('img').removeClass('active');
      $thumbs.find(`img[data-index="${currentSlide}"]`).addClass('active');
    });
    $thumbs.find('img').first().addClass('active');
  }
}
customElements.define('image-slider', ImageSlider);