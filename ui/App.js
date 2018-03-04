/* first imports should always be libraries */
import React, { Component } from 'react';

/* my css */

/* my components */
import Navigation from './Navigation';

class App extends Component {

    constructor(props) {
        super(props);

    }
    render() {
        return(
            <div>
                <Navigation scroll_about_me_header={this.scroll_about_me_header}
                            scroll_coding_projects_header={this.scroll_coding_projects_header}
                            scroll_artwork_header={this.scroll_artwork_header}
                            scroll_contact_me_header={this.scroll_contact_me_header} /> 
            </div>
        );
    }
}

export default App;