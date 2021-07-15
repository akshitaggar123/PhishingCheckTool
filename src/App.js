import React from "react";
import { Container } from "react-bootstrap";
import { Route } from "react-router-dom";
import Header from "./Components/Header";
import Home from "./Screens/Home";
import HomeScreen from "./Screens/HomeScreen";
import Phising from "./Screens/Phising";
import Report from "./Screens/Report";

const App = () => {
  return (
    <>
       <Header/>
      <main className="py-3">
  
          <Route path="/" exact>
            <HomeScreen/>
          </Route>

          <Route path="/phising" exact>
            <Phising/>
          </Route>

          <Route path="/similarity" exact>
            <Home/>
          </Route>

          <Route path="/report" exact>
            <Report/>
          </Route>
         
          </main>

    </>
  );
};

export default App;
