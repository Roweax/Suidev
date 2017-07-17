import React, { Component } from 'react';
import { GridList, GridTile } from 'material-ui/GridList';
import PlanetItem from './PlanetItem.js';

import Corner from '../components/Corner.js';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import Subheader from 'material-ui/Subheader';

const styles = {
    root: {
        width: '100%',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        backgroundColor: '#000'
    },
    content: {
        width: 1200,
        margin: '0 auto',
    },
    gridList: {
        width: '100%',
        overflowY: 'auto',
        cellHeight: 200
    },
    dialog: {
        width: '100%',
        maxWidth: 'none'
    }
};

const planet_null = {
    planet_id: 0,
    create_time: ''
}
class PlanetPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            planets: [],
            open: false,
            planet_id: -1,
            planet_visual: [],
            planet_view: planet_null
        };
    }


    HexToStr(value, size) {
        var str = "00000000" + value.toString(16).toUpperCase();
        return str.substring(str.length - size);
    }

    DecToStr(value, size) {
        var str = "00000000" + value.toString(10).toUpperCase();
        return str.substring(str.length - size);
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
        }).then((json) => {
            var data = JSON.parse(json);
            this.setState({
                planets: data.data
            });
        }).catch(err => {
            console.log('fetch error' + err);
        });
    }

    handleOpen = (planet_id) => {
        if (planet_id != this.state.planet_id) {
            this.setState({
                planet_visual: []
            });
            fetch('/api/planetdetail/' + planet_id, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }).then((response) => {
                return response.json();
            }).then((json) => {
                var planet_select = this.state.planets.find(
                    (e) => e.planet_id === planet_id
                )
                let planet_view = new Object();
                planet_view.kind = planet_select.kind.toUpperCase();
                planet_view.create_time = planet_select.create_time.substr(0, 16)
                let total_sceond = planet_select.render_time;
                let h = parseInt(total_sceond / 3600);
                total_sceond  = total_sceond % 3600;
                let m = parseInt(total_sceond / 60);
                let s = total_sceond % 60;
                planet_view.render_time = h.toString() + "h" + this.DecToStr(m, 2) + "m" + this.DecToStr(s, 2) + "s" 
                var data = JSON.parse(json);
                this.setState({
                    planet_visual: data,
                    planet_id: planet_id,
                    planet_view: planet_view
                });
            }).catch(err => {
                console.log('fetch error' + err);
            });
        }

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
            <FlatButton label="Close" primary={true} keyboardFocused={true} onTouchTap={this.handleClose} />
        ];

        var top_rows = 2;

        var planets = this.state.planets;
        var left_planets = [];
        var right_planets = [];
        var bottom_planets = [];
        if (planets.length > 0) {
            left_planets = planets.slice(0, top_rows);
        }
        if (planets.length > top_rows) {
            right_planets = planets.slice(top_rows, top_rows * 2);
        }
        if (planets.length > top_rows * 2) {
            bottom_planets = planets.slice(top_rows * 2);
        }

        var tile = (
        <GridTile cols={1} rows={1}><div style={{
            width: '100%',
            height: '100%'
        }} onShowLarge ={(event) => this.handleOpen(event)}><img src='./1.jpeg' style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            objecFit: 'cover'
        }}></img><Corner></Corner></div>
            </GridTile>
        );

        return (
            <div style = {styles.root}>
            <Dialog title={"Planet  " + this.state.planet_view.kind} actions={actions} modal={false} open={this.state.open} onRequestClose={this.handleClose}  style = {styles.dialog}>
            
            <div style={{width:700}}>
            <Subheader><span style={{position:'float', float:'left'}}>{"CREATE : " + this.state.planet_view.create_time}</span><span style={{position:'float', float:'right'}}>{"RENDER TIME : " + this.state.planet_view.render_time}</span></Subheader>
            
            <div style={{
                backgroundColor: 'black',
                width: 700,
                minWidth: 700,
                display: 'flex',
                margin: '0 auto'
            }}>
            <div style={{
                width: 300,
                height: 300
            }}>
            <img src={this.state.planet_visual.length > 0 ? "http://suidev.oss-cn-hangzhou.aliyuncs.com/render/planet/original/" + this.HexToStr(this.state.planet_visual[0].visual_id, 8) + '.png' : ""} style={{
                width: 300,
                height: 300
            }}></img>
            </div>
            <div style= {{
                width: 400,
                height: 300,
                minWidth: 400,
                display: 'flex',
                flexDirection: 'row',
                flexWrap: 'wrap'
            }}>
            {this.state.planet_visual.map(function(item) {
                return (
                    <img src={"http://suidev.oss-cn-hangzhou.aliyuncs.com/render/planet/small/" + this.HexToStr(item.visual_id, 8) + '.png'} style={{
                        width: 100,
                        height: 100
                    }}></img>
                )
            }, this
            )}
            </div>
            </div>
            </div>
            </Dialog>
            <div style = {styles.content}>
            <GridList cols = {6} padding = {1} cellHeight="200" style = {styles.gridList}>
            <GridTile actionPosition = "left" cols = {1} rows = {top_rows}>
            <GridList cols = {1} padding = {1} cellHeight="200">
            {left_planets.map(function(item) {
                return (
                    <PlanetItem key ={item.planet_id} item = {item}  onClick={this.handleOpen}/>
                )
            }, this
            )}
            </GridList>
            </GridTile>

            <GridTile actionPosition="left" titlePosition="top"
            titleBackground="linear-gradient(to bottom, rgba(1,1,1,0.7) 0%,rgba(1,1,1,0.3) 70%,rgba(1,1,1,1) 100%)"
            cols={4}
            rows={2}>
            <div style={{
                width: '100%',
                height: '100%'
            }}><img src='./planet_large.jpg' style={{
                position: 'absolute',
                width: '100%',
                height: '100%',
                objecFit: 'cover'
            }}></img><Corner></Corner></div>
            </GridTile>
            <GridTile actionPosition="left" cols={1} rows={2}>
            <GridList cols={1} padding={1} cellHeight="200">
            {right_planets.map(function(item) {
                return (
                    <PlanetItem key ={item.planet_id} item = {item} onClick={this.handleOpen}/>
                )
            }, this
            )}
            </GridList>
            </GridTile>
            {bottom_planets.map(function(item) {
                return (
                    <PlanetItem key ={item.planet_id} item = {item} onClick={this.handleOpen}/>
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
