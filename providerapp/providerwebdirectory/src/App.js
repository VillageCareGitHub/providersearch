import React, { Component } from 'react';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';

import PROVIDERSEARCH from './views/PROVIDERSEARCH'

import './App.css';

class App extends Component {
  

  handleChange = input => e => {
    this.setState({ [input]: e.target.value });
  };

  

  
  render () {
    
    let routeList = []
    
    
    
        routeList=[
          <Route exact path="/" render={(props)=><Redirect to="/views/PROVIDERSEARCH"/>} />,
          <Route exact path="/views/PROVIDERSEARCH" render={(props)=><PROVIDERSEARCH/>} />
          
        ]
    

    return (
      <BrowserRouter>
        <div className="App">
          {routeList}
        </div>
      </BrowserRouter>
    )
    }
}
export default App;
