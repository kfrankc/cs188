/**
 * @type {HTMLCanvasElement}
 */
let canvas = document.getElementById('canvas');

/**
 * @type {CanvasRenderingContext2D}
 */
let ctx;

const FPS = 20;
const fpsInterval = 1000 / FPS;
let prev = null;


if (canvas.getContext) {
  ctx = canvas.getContext('2d');
  // drawing code here
} else {
  // canvas-unsupported code here
}





ctx.fillStyle = 'rgb(200, 0, 0)';
ctx.fillRect(10, 10, 50, 50);

ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
ctx.fillRect(30, 30, 50, 50);


let test = () => {
  ctx.beginPath();
  ctx.strokeStyle = 'rgb(255,0,0,0.5)';

  ctx.moveTo(10, 10);
  ctx.lineTo(40, 80);
  ctx.stroke();

  ctx.moveTo(50, 80);
  ctx.lineTo(120, 85);
  ctx.stroke();
}
let a=0;
let b=0;


/**
 * Fade the previously drawn lines
 * @param {CanvasRenderingContext2D} ctx
 */
let fade = (ctx) => {
  let prev = ctx.globalCompositeOperation;
  ctx.fillStyle = "rgba(0, 0, 0, 0.97)";
  ctx.globalCompositeOperation = "destination-in";
  ctx.fillRect(0, 0, 150, 150)
  ctx.globalCompositeOperation = prev;
}

let animate = (timestamp) => {
    // request another frame
    requestAnimationFrame(animate);

    // calc elapsed time since last loop
    if (!prev) {
      prev = timestamp;
      console.log('hi');
    }
    let elapsed = timestamp - prev;

    // if enough time has elapsed, draw the next frame
    if (true) {
        // Get ready for next frame by setting then=now, but also adjust for your
        // specified fpsInterval not being a multiple of RAF's interval (16.7ms)
        prev = timestamp - (elapsed % fpsInterval);

        // Put your drawing code here


        fade(ctx)
        ctx.beginPath();
        ctx.strokeStyle = 'rgb(255,0,0,0.5)';

        ctx.moveTo(a,b);
        ctx.lineTo(a+1, b+1);
        a = (a+1)%150;
        b = (b+1)%150;
        ctx.stroke();
        ctx.closePath();
    }
}

// Start animating
requestAnimationFrame(animate);

window.abc = () => { fade(ctx) };
