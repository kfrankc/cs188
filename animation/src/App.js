import React, { Component } from 'react';
import PropTypes from 'prop-types';
import angiogram from './angiogram.js';
import "./angiogram.css";

class AppContainer extends Component {

  componentDidMount() {
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');
    if (!canvas.getContext) {
        // canvas-unsupported code here
    }
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

    ctx.fillStyle = 'rgb(200, 0, 0)';
    ctx.fillRect(10, 10, 50, 50);
    ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
    ctx.fillRect(30, 30, 50, 50);

    angiogram(vector_field, canvas, colors);
  }

  render() {
    return (
      <App
        width={150}
        height={150}
      />
    );
  }
}

class App extends Component {
    render() {
    let style = {
      width: this.props.width,
      height: this.props.height,
    }

    return (
      <div className="canvas-container">
        <div id="canvas-overlay" style={style}></div>
        <canvas id="canvas" width={this.props.width} height={this.props.height}></canvas>
        <div id="canvas-background" style={style}
        ></div>
      </div>
    );
  }
}

App.propTypes = {
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
};

export default AppContainer;
