import React, { Component } from 'react';
import './MaterialItem.css';

import Paper from 'material-ui/Paper';


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
            <Paper style = {{boxSizing: 'border-box',width:250, height:250, padding:10, margin:10}} onClick = {() => {this.props.onShowLarge("http://suidev.oss-cn-hangzhou.aliyuncs.com/render/material/original/"  + "00000001.png")}}>
                <img src='./1.jpeg' style={{height:'100%', width:'100%'}} ></img>
            </Paper>
        );
    }
}

export default GeometryItem;
