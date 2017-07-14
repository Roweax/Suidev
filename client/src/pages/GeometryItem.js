import React, { Component } from 'react';
import './MaterialItem.css';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Toggle from 'material-ui/Toggle';

import Avatar from 'material-ui/Avatar';
import Chip from 'material-ui/Chip';
import Paper from 'material-ui/Paper';

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


class GeometryItem extends Component {
    HexToStr(value, size) {
        var str = "00000000" + value.toString(16).toUpperCase();
        return str.substring(str.length - size);
    }

    onShow() {
        alert('aa');
    }

    render() {
        return (
            <Paper style = {{boxSizing: 'border-box',width:250, height:250, padding:10, margin:10}} onClick = {this.props.onShowLarge}>
                <img src='./1.jpeg' style={{height:'100%', width:'100%'}} ></img>
            </Paper>
        );
    }
}

export default GeometryItem;
