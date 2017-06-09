import React, { Component } from 'react';
import PropTypes from 'prop-types';
import angiogram from './angiogram.js';
import axios from 'axios';
import "./angiogram.css";

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


class AppContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      dimensions: null,
      vector_field: null,
      starting_points: null,
    };
  }

  componentDidMount() {
    /*
    const vector_field = [];
    const canvas_width = 150;
    const canvas_height = 150;
    for(let x = 0; x < canvas_width; x++) {
        vector_field.push([]);
        for(let y = 0; y < canvas_height; y++) {
            vector_field[x].push({ x: 1, y: 1 })
        }
    }
    this.setState({
      dimensions: {
        height: 150,
        width: 150,
      },
      vector_field: vector_field,
    })
    */




    const component = this;
    axios.get('/test-all.json') // todo: public folder node env
      .then((response) => {
        const vector_field = response.data.vector_field;
        const starting_points = response.data.starting_points;
        const width = vector_field.length;
        const height = vector_field[0].length;
        component.setState({
          dimensions: {
            width: width,
            height: height,
          },
          vector_field: vector_field,
          starting_points: starting_points,
        })
      })
      .catch(function (error) {
        console.log(error);
      });
    /*
    */
  }

  render() {
    // TODO: what is default?  need canvas rendered in order to get context
    // TODO: better state check
    if (this.state.dimensions === null && this.state.vector_field === null) {
      return null;
    }

    return (
      <App
        width={this.state.dimensions.width}
        height={this.state.dimensions.height}
        vector_field={this.state.vector_field}
        starting_points={this.state.starting_points}
      />
    );
  }
}

class App extends Component {
  componentDidMount() {
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');
    if (!canvas.getContext) {
        // canvas-unsupported code here
    }

    ctx.fillStyle = 'rgb(200, 0, 0)';
    ctx.fillRect(10, 10, 50, 50);
    ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
    ctx.fillRect(30, 30, 50, 50);
    angiogram(this.props.vector_field, this.props.starting_points, canvas, colors);
  }

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
  //vector_field: PropTypes.arrayOf(PropTypes.array.isRequired).isRequired,
  //starting_points: PropTypes.array,
  vector_field: PropTypes.arrayOf(PropTypes.array.isRequired).isRequired,
  starting_points: PropTypes.oneOfType([PropTypes.string.isRequired, PropTypes.array.isRequired]).isRequired, // TOOD: array of objects
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
};

export default AppContainer;
