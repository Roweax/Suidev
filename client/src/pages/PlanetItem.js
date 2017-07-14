import React, { Component } from 'react';
import './MaterialItem.css';

import Corner from '../components/Corner.js';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Toggle from 'material-ui/Toggle';

import Avatar from 'material-ui/Avatar';
import Chip from 'material-ui/Chip';
import Paper from 'material-ui/Paper';
import {GridList, GridTile} from 'material-ui/GridList';
import CircularProgress from 'material-ui/CircularProgress';

const styles = {
    chip: {
        margin: 4
    },


    wrapper: {
        display: 'flex',
        flexWrap: 'wrap',
    },

    paper:{
        height: 40,
        width: 40,
        margin: "0 10",
        textAlign: 'center',
        display: 'inline-block',
    }
};


class PlanetItem extends Component {

    constructor(props) {
        super(props);
        this.state = {
            play: false,
            loading : false
            //src :''
        };

    }

    componentDidMount() {
        this.refs.video.addEventListener("loadeddata", this.handleLoaded.bind(this), false);
    }

    HexToStr(value, size) {
        var str = "00000000" + value.toString(16).toUpperCase();
        return str.substring(str.length - size);
    }

    onShow() {
        alert('aa');
    }

    handlMouseEnter() {
        this.setState({
            play: true,
            src : "http://suidev.oss-cn-hangzhou.aliyuncs.com/render/planet/video/" + this.HexToStr(this.props.item.planet_id, 8) + '.mp4',
            loading : true
        }, this.play());
    }

    handlMouseLeave() {
        this.setState({
            play: false,
            loading : false
        }, this.stop());
    }

    handleLoaded(e) {
        this.setState({
            loading : false
        })
    }

    play() {
        this.refs.video.load();
        this.refs.video.play();
    }

    stop() {
        this.refs.video.pause();
    }

    HexToStr(value, size) {
        var str = "00000000" + value.toString(16).toUpperCase();
        return str.substring(str.length - size);
    }

    render() {
        var loadingbar =
        <CircularProgress style={{display: this.state.loading ? 'inline' : 'none', position:'absolute', left:0, right:0, top:0, bottom:0, margin:'auto', objectFit:'cover'}}/>
        ;
        var show_video = 'hidden';
        return (
            <GridTile cols={1} rows={1}>
            <div style={{width:'100%', height:'100%'}} onMouseEnter = {(event) => this.handlMouseEnter(event)} onMouseLeave = {(event) => this.handlMouseLeave(event)}>
            <img src={"http://suidev.oss-cn-hangzhou.aliyuncs.com/render/planet/original/" + this.HexToStr(this.props.item.planet_id, 8) + '.png'} style={{position:'absolute', width:'100%', height:'100%',objecFit:'cover'}}></img>
            <video preload='none' loop muted ref="video" style={{visibility:this.state.play ? 'visible' : 'hidden', position:'absolute', width:'100%', height:'100%', objectFit:'cover'}}>
                <source src={this.state.src} type="video/mp4" />
            </video><Corner></Corner>
            </div>
            </GridTile>
        );
    }
}

export default PlanetItem;
