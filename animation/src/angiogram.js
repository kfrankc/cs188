import "./angiogram.css";

/**
 * @typedef {Object} Vector - creates a new type named Vector
 * @property {number} x - x component of vector
 * @property {number} y - y component of vecto
 * @property {number} [m] - (optional) magnitude
 */

/**
 * Return a number between start and end, inclusive
 * @param {number} start
 * @param {number} end
 */
let rand_int = (start, end) => {
  return Math.round(start + Math.random()*(end-start));
}

/**
 * Factory function that returns a particle class.
 * Needed to create a closure for canvas dimensions, etc
 * @param {number} canvas_width
 * @param {number} canvas_height
 * @param {number} max_particle_age
 */
let ParticleFactory = (canvas_width, canvas_height, max_particle_age) => {

/**
 * Particle
 */
  class Particle {
  /**
    *
    * @param {number} x
    * @param {number} y
    * @param {number} age
    */
    constructor(x, y, age) {
      this.x = x;
      this.y = y;
      this.age = age;
    }

   /**
    * Returns a new particle at a random location and with a random age
    */
    static rand() {
      // TODO:  needs to go to an actual point on a path
      let x = rand_int(0, canvas_height-1);
      let y = rand_int(0, canvas_height-1);
      let age = rand_int(0, max_particle_age);
      return new Particle(x, y, age);
    }

    randomize() {
      this.x = rand_int(0, canvas_height-1);
      this.y = rand_int(0, canvas_width-1);
      this.age = rand_int(0, max_particle_age);
    }

  /**
   * Moves the particle to (x,y)
   * @param {number} newX
   * @param {number} newY
   */
    moveTo(newX, newY) {
      this.x = newX;
      this.y = newY;
    }
  }

  return Particle;
}



/**
 * Fade the previously drawn lines
 * @param {CanvasRenderingContext2D} ctx
 */
const fade = (ctx) => {
  let prev = ctx.globalCompositeOperation;
  ctx.fillStyle = "rgba(0, 0, 0, 0.97)"; // Reduce 0.97 to make pixel trail shorter
  ctx.globalCompositeOperation = "destination-in";
  ctx.fillRect(0, 0, 150, 150)
  ctx.globalCompositeOperation = prev;
}

/**
*
* @param {Array<Array<Vector>>} vector_field - vector field
* @param {HTMLCanvasElement} canvas - canvas
* @param {Array} colors - canvas.  Should check if getContext('2d') before calling this function
* @param {*} [options] - options
*/
let angiogram = (vector_field, canvas, colors, options) => {
  // Options
  options = options || {};
  const fps = options.fps || 20;
  /**
   * The number of particles to be displayed
   */
  const num_particles = options.NUM_PARTICLES || 10;
  /**
   * The maximum number of frames a particle drawn on the
   * canvas before it stops moving and stays there until it fades.
   */
  const max_particle_age = options.MAX_PARTICLE_AGE || 100;


  const fpsInterval = 1000 / fps;
  const canvas_width = canvas.width;
  const canvas_height = canvas.height;
  const ctx = canvas.getContext('2d');
  const Particle = ParticleFactory(canvas_width, canvas_height, max_particle_age);
  const particles = [];
  let prev = null;

  // Initialize particles
  for (let i=0; i<num_particles; i++) {
    particles.push(Particle.rand());
  }


 /**
  * Move the particles
  */
  let drawNextFrame = () => {
    fade(ctx);

    particles.forEach((particle) => {
      // Particle died, create a new one
      if (particle.age > max_particle_age) {
          particle.randomize()
      }
      particle.age++;

      for (let i=0; i < 1; i++) { // TODO: draw vectors multiple times?
        if (canvas_width <= particle.x || canvas_height <= particle.y) { // out of bounds
          break;
        }
        ctx.beginPath();
        ctx.lineCap = "round";

        let [r,g,b] = colors[Math.round(particle.x/150 * 9)];
        //ctx.strokeStyle = 'red';  // TODO: base it on magnitude
        // let relativeSpeed = getRelativeSpeed()
        // let strokeStyle = getColor(relativeSpeed, colors)
        ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, 1)`;


        ctx.moveTo(particle.x, particle.y);
        let new_x = particle.x + vector_field[particle.x][particle.y].x;
        let new_y = particle.y + vector_field[particle.x][particle.y].y;
        ctx.lineTo(new_x, new_y)
        ctx.stroke();

        // Move the particle
        particle.moveTo(new_x, new_y);
      }

    })
  }

  /**
   *
   * @param {number} - DOMHighResTimeStamp
   */
  let updateAnimation = (timestamp) => {
    // request another frame
    requestAnimationFrame(updateAnimation);

    // calc elapsed time since last loop
    if (!prev) {
      prev = timestamp;
    }
    let elapsed = timestamp - prev;

    // if enough time has elapsed, draw the next frame
    if (true) {
      // Get ready for next frame by setting then=now, but also adjust for your
      // specified fpsInterval not being a multiple of RAF's interval (16.7ms)
      prev = timestamp - (elapsed % fpsInterval);

      // Put your drawing code here

      drawNextFrame();
      return; // TODO: del
    }
  }

  // Start animating
  window.requestAnimationFrame(updateAnimation);
}

export default angiogram;
