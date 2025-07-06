class ImageSlider2x extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  connectedCallback() {
    const images = JSON.parse(this.getAttribute('images') || '[]');
    // Agrupa as imagens de 2 em 2
    const slides = [];
    for (let i = 0; i < images.length; i += 2) {
      const img1 = images[i];
      const img2 = images[i + 1];
      slides.push({
        left: img1,
        right: img2 || null
      });
    }
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
        .slider-thumbs img.active { border-color: #e91e63; opacity: 1; }
        .slider-main .slide-pair { display: flex; justify-content: center; align-items: center; gap: 16px; width: 100%; }
        .slider-main img { width: 48%; max-width: 280px; max-height: 300px; object-fit: contain; display: block; margin: 0 auto; }
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
        .slick-list {
            width: 100% !important;
            box-sizing: border-box;
        }
        .slick-track {
            width: 100% !important;
            box-sizing: border-box;
            left: 0 !important;
            transform: none !important;
        }
      </style>
    `;
    // Thumbs: só a primeira de cada par
    const thumbs = slides.map((slide, i) =>
      `<img src="${slide.left.src}" alt="${slide.left.alt}" data-index="${i}">`
    ).join('');
    // Slides: cada par de imagens
    const slidesHtml = slides.map(slide =>
      `<div class="slide-pair">
        <img src="${slide.left.src}" alt="${slide.left.alt}">
        ${slide.right ? `<img src="${slide.right.src}" alt="${slide.right.alt}">` : ''}
      </div>`
    ).join('');
    this.shadowRoot.innerHTML = `
      ${style}
      <div class="slider-thumbs">${thumbs}</div>
      <div class="slider-main_wrap">
        <div class="slider-main">${slidesHtml}</div>
        <div class="arrow_box"></div>
      </div>
    `;
    // Native slider logic for Shadow DOM compatibility
    const sliderMain = this.shadowRoot.querySelector('.slider-main');
    const thumbImgs = Array.from(this.shadowRoot.querySelectorAll('.slider-thumbs img'));
    const slidePairs = Array.from(this.shadowRoot.querySelectorAll('.slide-pair'));
    let currentIndex = 0;

    function showSlide(index) {
      slidePairs.forEach((el, i) => {
        el.style.display = i === index ? 'flex' : 'none';
      });
      thumbImgs.forEach((img, i) => {
        if (i === index) img.classList.add('active');
        else img.classList.remove('active');
      });
      currentIndex = index;
    }

    thumbImgs.forEach((img, i) => {
      img.addEventListener('click', () => showSlide(i));
    });

    // Show the first slide by default
    showSlide(0);
  }
}
customElements.define('image-slider-2x', ImageSlider2x);
