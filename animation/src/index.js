import angiogram from './angiogram.js';

let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
const colors = [
  [255,255,0],
  [255,226,0],
  [255,198,0],
  [255,170,0],
  [255,141,0],
  [255,113,0],
  [255,85,0],
  [255,56,0],
  [255,28,0],
  [255,0,0],
]
const vector_field = [];
for(let x = 0; x < canvas.width; x++) {
  vector_field.push([]);
  for(let y = 0; y < canvas.height; y++) {
    vector_field[x].push({ x: 1, y: 1 })
  }
}


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

angiogram(vector_field, canvas, colors);
