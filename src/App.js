import "./App.css";

import React, { Component } from "react";
import { Input, Menu, Container, Segment } from "semantic-ui-react";

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  NavLink,
} from "react-router-dom";

class App extends Component {
  render() {
    return (
      <Router>
        <Menu fixed="top" inverted>
          <Container>
            <Menu.Item name="Home" as={NavlinkExact} to="/" />
            <Menu.Item name="About" as={NavLink} to="/about" />
            <Menu.Item name="Dashboard" as={NavLink} to="/dashboard" />
          </Container>
        </Menu>

        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/dashboard">
            <Dashboard />
          </Route>
        </Switch>
      </Router>
    );
  }
}

// NavlinkExact wraps NavLink with the exact is always on, in order to prevent Menu.Item
// with as={NavLink} to always be ON when the path points to the Root.
function NavlinkExact(props) {
  return <NavLink {...props} exact={true} />;
}

function Home() {
  return (
    <Container text style={{ marginTop: "7em" }}>
      <div>
        <h2>Home</h2>
      </div>
    </Container>
  );
}

function About() {
  return (
    <Container text style={{ marginTop: "7em" }}>
      <div>
        <h2>About</h2>
      </div>
    </Container>
  );
}

function Dashboard() {
  return (
    <Container text style={{ marginTop: "7em" }}>
      <div>
        <h2>Dashboard</h2>
      </div>
    </Container>
  );
}

export default App;
