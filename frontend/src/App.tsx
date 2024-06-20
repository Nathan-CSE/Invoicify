import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import PageList from './PageList';

function App() {
  return (
    <>
      <Router>
        <PageList></PageList>
      </Router>
    </>
  );
}

export default App;
