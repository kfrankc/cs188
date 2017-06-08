
/**
 * STUFF TO BE PASSED IN LATER
 */
const CANVAS_WIDTH = 150;
const CANVAS_HEIGHT = 150;
const particles = [];

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

/**
 * The maximum number of frames a particle is drawn on the 
 * canvas before it stops moving and stays there until it fades.
 */
const MAX_PARTICLE_AGE = 100;

/**
 * The number of particles to be displayed
 */
const NUM_PARTICLES = 10;
let prev = null;


if (canvas.getContext) {
  ctx = canvas.getContext('2d');
  // drawing code here
} else {
  // canvas-unsupported code here
}


class Particle {
 /**
  * 
  * @param {number} x 
  * @param {number} y 
  * @param {number} age 
  */
  constructor(x, y, age) {
    this.x = x;
    this.width = y;
    this.age = age;
  }

  static rand() {
    // TODO:  needs to go to an actual point on a path
    let x = Math.random() * CANVAS_HEIGHT;
    let y = Math.random() * CANVAS_WIDTH;
    let age = Math.random() * MAX_PARTICLE_AGE;
    return new Particle(x, y, age);
  }

 /**
  * Returns a new particle at a random location and with a random age
  */
  randomize() {
    this.x = Math.random() * CANVAS_HEIGHT;
    this.y = Math.random() * CANVAS_WIDTH;
    this.age = Math.random() * MAX_PARTICLE_AGE;
  }
}


// Initialize particles
for (let i=0; i<NUM_PARTICLES; i++) {
  particles.push(Particle.rand());
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

/**
 * 
 * @param {number} - DOMHighResTimeStamp
 */
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

        // Fade the canvas
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
window.requestAnimationFrame(animate);

window.abc = () => { fade(ctx) };
