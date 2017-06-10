import React from 'react';
import ReactDOM from 'react-dom';
import AppContainer from './App';

let options = {
    fps: 20,
    num_particles: 20,
    max_particle_age: 100,
};

let url = process.env.PUBLIC_URL + "/data-paths.json";

// TODO: public folder node env
ReactDOM.render(<AppContainer data_url={url} options={options}/>,
 document.getElementById('root'));
