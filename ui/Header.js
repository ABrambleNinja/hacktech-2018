import React, { Component } from 'react';
import { Jumbotron, Container, Row, Col } from 'reactstrap';

class Header extends Component {

    render() {

        let style_jumbotron_transparent = {
            background: 'rgba(256, 256, 256, 0.75)'
        }

        return (
            <div>
                <Jumbotron style={style_jumbotron_background_image} fluid>
                    <Container>
                        <Jumbotron className="mx-auto" style={style_jumbotron_transparent}>
                            <Col sm={{ size: 6, push: 2, pull: 2, offset: 1}}>
                                <h1>hi</h1>
                            </Col>
                            <h1 className="display-3">Hello, world!</h1>
                                <p className="lead">This is a simple hero unit, a simple Jumbotron-style component for calling extra attention to featured content or information.</p>
                                <hr className="my-2" />
                                <p>It uses utility classes for typgraphy and spacing to space content out within the larger container.</p>
                        </Jumbotron>
                    </Container>
                </Jumbotron>
            </div>
        );
    }
}

export default Header;
