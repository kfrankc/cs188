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
 * @param {(string|Array)} starting_points - Either "ALL" or array of {x:x,y:y} coordinates
 */
let ParticleFactory = (canvas_width, canvas_height, max_particle_age, starting_points) => {

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
    * Gives the  particle a random location and age
    */
    randomize() {
      if (starting_points === "ALL") {
        this.x = rand_int(0, canvas_height-1);
        this.y = rand_int(0, canvas_width-1);
        this.age = rand_int(0, max_particle_age);
      } else {
        let starting_point = starting_points[rand_int(0, starting_points.length - 1)];
        this.x = starting_point.x;
        this.y = starting_point.y;
        this.age = rand_int(0, max_particle_age);
      }
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
*
* @param {Array<Array<Vector>>} vector_field - vector field
* @param {(string|Array)} starting_points - Either "ALL" or array of {x:x,y:y} coordinates
* @param {HTMLCanvasElement} canvas - canvas
* @param {Array} colors - canvas.  Should check if getContext('2d') before calling this function
* @param {*} [options] - options
*/
let angiogram = (vector_field, starting_points, canvas, colors, options) => {
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
  const Particle = ParticleFactory(canvas_width, canvas_height, max_particle_age, starting_points);
  const particles = [];
  let prev = null;

  // Initialize particles
  for (let i=0; i<num_particles; i++) {
    let p = new Particle(0,0,0);
    p.randomize();
    particles.push(p);
  }

  /**
   * Fade the previously drawn lines
   * @param {CanvasRenderingContext2D} ctx
   */
  const fade = (ctx) => {
      ctx.save();
      ctx.globalAlpha = 0.1;
      ctx.globalCompositeOperation='destination-out';
      ctx.fillStyle= '#FFF';
      ctx.fillRect(0,0,canvas_width, canvas_height);
      ctx.restore();
  }

 /**
  * Move the particles
  */
  const drawNextFrame = () => {
    fade(ctx);

    particles.forEach((particle) => {
      // Particle died, create a new one
      if (particle.age > max_particle_age) {
          particle.randomize()
      }
      particle.age++;

      for (let i=0; i < 2; i++) { // TODO: draw vectors multiple times?
        if (canvas_width <= particle.x || canvas_height <= particle.y) { // out of bounds
          break;
        }
        ctx.beginPath();
        ctx.lineCap = "round";

        // let [r,g,b] = colors[Math.round(particle.x/canvas_width * 9)]; // TODO:
        let [r,g,b] = colors[8]; // TODO:
        //ctx.strokeStyle = 'red';  // TODO: base it on magnitude
        // let relativeSpeed = getRelativeSpeed()
        // let strokeStyle = getColor(relativeSpeed, colors)
        ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, 1)`;


        ctx.moveTo(particle.x, particle.y);
        let v = vector_field;
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
