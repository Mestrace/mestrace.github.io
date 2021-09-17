import React, { Component } from "react";
import { Input, Menu } from "semantic-ui-react";

export default class HeaderMenu extends Component {
  render() {
    const { activeItem } = this.state;

    return (
      <Menu secondary>
        <Menu.Item name="home" active={activeItem === "home"} />
        <Menu.Item name="messages" active={activeItem === "messages"} />
        <Menu.Item name="friends" active={activeItem === "friends"} />
        <Menu.Menu position="right">
          <Menu.Item>
            <Input icon="search" placeholder="Search..." />
          </Menu.Item>
          <Menu.Item name="logout" active={activeItem === "logout"} />
        </Menu.Menu>
      </Menu>
    );
  }
}
