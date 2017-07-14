import React, { Component } from 'react';
import {GridList, GridTile} from 'material-ui/GridList';
import PlanetItem from './PlanetItem.js';

import Corner from '../components/Corner.js';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';

const styles = {
    root: {
        width : '100%',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        backgroundColor : '#000'
    },
    content: {
        width :1200,
        margin: '0 auto',
    },
    gridList: {
        width: '100%',
        overflowY: 'auto',
        cellHeight : 200
    },
    dialog: {
        width: '100%',
        maxWidth: 'none'
    }
};

class PlanetPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            planets : [
            ],
            open : false
        };
    }



            componentDidMount() {
                fetch('/api/planets/0', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }).then((response) => {
                return response.json();
            }) .then((json) => {
                var data = JSON.parse(json);
                this.setState({
                    planets: data.data
                });
            }).catch(err => {
                console.log('fetch error' + err);
            });
            }

    handleOpen = () => {
        this.setState({
            open: true
        });
    };


    handleClose = () => {
        this.setState({
            open: false
        });
    };

    render() {
        const actions = [
            <FlatButton label="Close" primary={true} onTouchTap={this.handleClose} />
        ];

        var top_rows = 2;

        var planets = this.state.planets;
        var left_planets = [];
        var right_planets = [];
        var bottom_planets = [];
        if(planets.length > 0) {
            left_planets = planets.slice(0, top_rows);
        }
        if(planets.length > top_rows) {
            right_planets = planets.slice(top_rows, top_rows * 2);
        }
        if(planets.length > top_rows * 2) {
            bottom_planets = planets.slice(top_rows * 2);
        }

        var tile = (
            <GridTile cols={1} rows={1}><div style={{width:'100%', height:'100%'}} onShowLarge ={(event) => this.handleOpen(event)}><img src='./1.jpeg' style={{position:'absolute', width:'100%', height:'100%',
            objecFit:'cover'}}></img><Corner></Corner></div>
            </GridTile>
        );

        return (
            <div style = {styles.root}>
            <Dialog title="Planet" actions={actions} modal={true} open={this.state.open} style = {styles.dialog}>
            <div style={{backgroundColor:'black', width:700, minWidth:700, display:'flex', margin:'0 auto'}}>
            <div style={{width:300, height:300}}>
            <img src="./0000.png" style={{width:300, height:300}}></img>
            </div>
            <div style= {{width:400, height:300, minWidth:400, display:'flex', flexDirection:'row',flexWrap:'wrap'}}>
            <img src="./0000.png" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            <img src="./1.jpeg" style={{width:100, height:100}}></img>
            </div>
            </div>
            </Dialog>
            <div style = {styles.content}>
            <GridList cols = {6} padding = {1} style = {styles.gridList}>
            <GridTile actionPosition = "left" cols = {1} rows = {top_rows}>
            <GridList cols = {1} padding = {1}>
            {left_planets.map(
                function (item) {
                    console.log(item.planet_id);
                    return (
                        <PlanetItem key ={item.id} item = {item}/>
                    )
                }, this
            )}
            </GridList>
            </GridTile>

            <GridTile actionPosition="left" titlePosition="top"
            titleBackground="linear-gradient(to bottom, rgba(1,1,1,0.7) 0%,rgba(1,1,1,0.3) 70%,rgba(1,1,1,1) 100%)"
            cols={4}
            rows={2}>
            <div style={{width:'100%', height:'100%'}}><img src='./1.jpeg' style={{position:'absolute', width:'100%', height:'100%',objecFit:'cover'}}></img><Corner></Corner></div>
            </GridTile>
            <GridTile actionPosition="left" cols={1} rows={2}>
            <GridList cols={1} padding={1}>
            {right_planets.map(
                function (item) {
                    return (
                        <PlanetItem key ={item.planet_id} item = {item}/>
                    )
                }, this
            )}
            </GridList>
            </GridTile>
            {bottom_planets.map(
                function (item) {
                    return (
                        <PlanetItem key ={item.planet_id} item = {item}/>
                    )
                }, this
            )}
            </GridList>
            </div>
            </div>
        );
    }
}

export default PlanetPage;
