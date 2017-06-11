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
    const component = this;
    axios.get(this.props.data_url)
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
        options={this.props.options}
      />
    );
  }
}

AppContainer.propTypes = {
  // URL to json data
  data_url: PropTypes.string.isRequired,
  options: PropTypes.object.isRequired,
}

class App extends Component {
  componentDidMount() {
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');
    if (!canvas.getContext) {
        // canvas-unsupported code here
    }

    // DEBUG
    ctx.fillStyle = 'rgb(200, 0, 0)';
    ctx.fillRect(10, 10, 50, 50);
    ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
    ctx.fillRect(30, 30, 50, 50);


    // Start animating
    angiogram(this.props.vector_field,
      this.props.starting_points,
      canvas,
      colors,
      this.props.options,
    );

    // Start event listener for hover
    const onKeyDown = (e) => {
      if(e.ctrlKey) {
        window.addEventListener('mousemove', this.onMouseMove);
      }
      /*
      if(e.shiftKey) {
        window.addEventListener('mousemove', this.onMouseMoveShift);
      }
      */
    }
    const onKeyUp = (e) => {
      if(!e.ctrlKey) {
        const overlay = document.querySelector('#canvas-overlay');
        overlay.style.display = "none";
        window.removeEventListener('mousemove', this.onMouseMove);
      }
      /*
      if(!e.shiftKey) {
        const background = document.querySelector('#canvas-hidden-bg');
        background.style.display = "none";
        window.removeEventListener('mousemove', this.onMouseMoveShift);
      }
      */
    }
    window.addEventListener('keydown', onKeyDown);
    window.addEventListener('keyup', onKeyUp);
    /*
    */
  }

  onMouseMove(e) {
    const overlay = document.querySelector('#canvas-overlay');
    overlay.style.webkitMaskPosition = `${e.pageX-75}px ${e.pageY-75}px`;
    overlay.style.display = "inline-block";
  }

  onMouseMoveShift(e) {
    const background = document.querySelector('#canvas-hidden-bg');
    background.style.webkitMaskPosition = `${e.pageX-75}px ${e.pageY-75}px`;
    background.style.display = "inline-block";
  }

  render() {
    let style = {
      width: this.props.width,
      height: this.props.height,
    }

    let overlay_style = {
        width: this.props.width,
        height: this.props.height,
        background: `url(${process.env.PUBLIC_URL + "/angiogram.gif"})`,
    }

    let background_style = {
        width: this.props.width,
        height: this.props.height,
        background: `url(${process.env.PUBLIC_URL + "/angiogram.gif"})`,
    }

    return (
      <div className="canvas-container">
        <div id="canvas-overlay" style={overlay_style}></div>
        <canvas id="canvas" width={this.props.width} height={this.props.height}></canvas>
        <div className="background-overlay" style={style}></div>
        <div id="canvas-background" style={background_style}></div>
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
  options: PropTypes.object.isRequired,
};

export default AppContainer;
