import React from 'react';
import './style/form.css';
import './style/results.css';
import Header from './components/Header';
import Form from './components/Form';

const App = () => {
  return (
    <div className="app-container">
      <Header />
      <Form />
      <p align="center">
        <a href="https://github.com/fsiino/food-nutrition-express" target="_blank">Github Repo</a>
      </p>
    </div>
  );
}

export default App;
