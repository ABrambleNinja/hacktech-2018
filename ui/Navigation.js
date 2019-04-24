import React, { Component } from 'react';
import { Collapse, Navbar, NavbarToggler, NavbarBrand, Nav, NavItem, NavLink } from 'reactstrap';

class Navigation extends Component {

    constructor(props) {
        super(props);

        this.state = {
            isOpen: false
        };

        this.toggle = this.toggle.bind(this);
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {

        return (
            <div>

                {/* KINDA HACKY WAY OF FIXING ANIMATIONS AND PADDING BY HAVING TWO NAVBARS, ONE WHICH IS FIXED AND ONE THAT'S NOT */}
                <Navbar color="info" toggleable>
                    <NavbarToggler right onClick={this.toggle} />
                    <NavLink>About Me</NavLink>
                    <NavLink>Coding Projects</NavLink>
                    <NavLink>Artwork</NavLink>
                    <NavLink>Contact Me</NavLink>
                </Navbar>

                <Navbar color="info" fixed="top" toggleable>
                    <NavbarToggler right onClick={this.toggle} />
                    <NavLink href="#about_me" onClick={this.props.scroll_about_me_header}>About Me</NavLink>
                    <NavLink href="#coding_projects" onClick={this.props.scroll_coding_projects_header}>Coding Projects</NavLink>
                    <NavLink href="#artwork" onClick={this.props.scroll_artwork_header}>Artwork</NavLink>
                    <NavLink href="#contact_me" onClick={this.props.scroll_contact_me_header}>Contact Me</NavLink>
                </Navbar>
                {this.props.children}
            </div>
        );
    }

}

export default Navigation;
