import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

const element = (
  <h1 className="title">
    Hello, world!
  </h1>
);

const default_element = (
    <div className="App">
            <div className="App-header">
              <img src={logo} className="App-logo" alt="logo" />
              <h2>Politoxi App</h2>
            </div>
            <p className="App-intro">
              Fernando eres un primor de los primores...
            </p>
          </div>
);

class App extends Component {
  render() {
    return (element);
  }
}

export default App;
