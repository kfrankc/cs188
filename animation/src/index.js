import React from 'react';
import ReactDOM from 'react-dom';
import AppContainer from './App';

// TODO: public folder node env
ReactDOM.render(<AppContainer data_url="/data-paths.json"/>,
 document.getElementById('root'));
