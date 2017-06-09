import React from 'react';
import ReactDOM from 'react-dom';
import AppContainer from './App';

let options = {
    fps: 20,
    num_particles: 10,
    max_particle_age: 100,
};

// TODO: public folder node env
ReactDOM.render(<AppContainer data_url="/data-paths.json" options={options}/>,
 document.getElementById('root'));
