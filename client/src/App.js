import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Tabs, Tab } from 'material-ui/Tabs';
import StartMap from './components/StartMap.js';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { indigo100, indigo600, indigo800 } from 'material-ui/styles/colors';

import { GridList, GridTile } from 'material-ui/GridList';
import IconButton from 'material-ui/IconButton';
import StarBorder from 'material-ui/svg-icons/toggle/star-border';


import PlanetPage from './pages/PlanetPage.js';
import InfoPage from './pages/InfoPage.js';
import MaterialPage from './pages/MaterialPage.js';
import GeometryPage from './pages/GeometryPage.js';
import DevelopPage from './pages/DevelopPage.js';

const styles = {
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
    },
    gridList: {
        width: 500,
        height: 500,
        overflowY: 'auto',
    },
};


const muiTheme = getMuiTheme({
    palette: {
        primary1Color: indigo600,
        primary2Color: indigo800,
        primary3Color: indigo100,
    },
}, {
    avatar: {
        borderColor: null,
    },
});



class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pictures: []
        };
    }

    componentDidMount() {}

    render() {
        const styles = {
            headline: {
                fontSize: 24,
                paddingTop: 16,
                marginBottom: 12,
                fontWeight: 400,
            },
        };

        return (
            <MuiThemeProvider muiTheme={muiTheme}>
            <div className="App" >
            <Tabs >
            <Tab label="GALAXY">
            <PlanetPage></PlanetPage>
            </Tab>
            <Tab label="MATERIAL" >
            <MaterialPage/>
            </Tab>
            <Tab label="FIGURE" data-route="/home">
            <GeometryPage/>
            </Tab>
            <Tab label="INFO" data-route="/home">
            <div>
            <InfoPage/>
            </div>
            </Tab>
            <Tab label="DEVELOP" data-route="/home">
            <div>
            <DevelopPage/>
            </div>
            </Tab>
            </Tabs>
            <div className="App-header">
            <IconButton  tooltip="Roweax's Github" style={{
                fill: 'white',
                height: '64px',
                width: '64px'
            }} href="https://github.com/Roweax" tooltipPosition="bottom-center">
            <svg aria-hidden="true" height="40" version="1.1" viewBox="0 0 16 16" width="40"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg></IconButton>
            </div>
            </div>
            </MuiThemeProvider>
        );
    }
}

export default App;