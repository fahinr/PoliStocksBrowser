const html = document.documentElement;
const canvas = document.getElementById("subtitle-canvas");
const context = canvas.getContext("2d");
const heading = document.getElementById("table_name");

const frameCount = 255;
const currentFrame = index => (
  `image-frames/congressbw9sec${index.toString().padStart(4, '0')}.png`
)
window.addEventListener('resize', resizeCanvas, false);
function resizeCanvas(){

  canvas.width = 1920;
  canvas.height = 1080; 
  const img = new Image()
img.src = currentFrame(1);

img.onload=function(){
  context.drawImage(img, 0, 0);
}

const updateImage = index => {
  img.src = currentFrame(index);
  context.drawImage(img, 0, 0);
}

window.addEventListener('scroll', () => {  
  // how far has the user scrolled 
  const scrollTop = html.scrollTop;
  // maximum that the user can scroll inside the current window
  const maxScrollTop = html.scrollHeight - window.innerHeight
  const scrollFraction = scrollTop / maxScrollTop;
  // when hits half way then opacity is 1 otherwise opacity moves towards 0
  
  heading.style.opacity = scrollFraction > 0.5 ? (1 - scrollFraction) : scrollFraction * 2;
  const frameIndex = Math.min(
    frameCount - 1,
    Math.ceil(scrollFraction * frameCount)
  );
  
  // The window.requestAnimationFrame() method tells the browser that you wish to perform an animation and requests that the browser calls a specified function to update an animation before the next repaint
  requestAnimationFrame(() => updateImage(frameIndex + 1))
});


}

resizeCanvas();