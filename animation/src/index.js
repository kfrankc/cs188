import React from 'react';
import ReactDOM from 'react-dom';
import AppContainer from './App';

let options = {
    fps: 20,
    num_particles: 20,
    max_particle_age: 10,
};

// TODO: public folder node env
ReactDOM.render(<AppContainer data_url="/data-paths.json" options={options}/>,
 document.getElementById('root'));
