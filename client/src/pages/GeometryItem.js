import React, { Component } from 'react';
import './MaterialItem.css';

import Paper from 'material-ui/Paper';


class GeometryItem extends Component {
    HexToStr(value, size) {
        var str = "00000000" + value.toString(16).toUpperCase();
        return str.substring(str.length - size);
    }


    render() {
        return (
            <Paper style = {{boxSizing: 'border-box',width:350, padding:10, margin:10}} onClick = {() => {this.props.onShowLarge(this.props.item.id)}}>
                <img src={'http://suidev.oss-cn-hangzhou.aliyuncs.com/render/geomtery/s' + this.props.item.id + '.png'} style={{height:'100%', width:'100%'}} ></img>
            </Paper>
        );
    }
}

export default GeometryItem;
