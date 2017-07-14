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


class MaterialItem extends Component {
    HexToStr(value, size) {
        var str = "00000000" + value.toString(16).toUpperCase();
        return str.substring(str.length - size);
    }

    onShow() {
        alert('aa');
    }

    render() {
        return (
            <div style = {{boxSizing: 'border-box',width:'33%', padding:'10px'}} onClick = {this.props.onShowLarge}>
            <Card>
            <CardHeader
            title={this.props.data.kind}
            titleStyle = {{textTransform:'uppercase'}}
            subtitle= {this.props.data.create_time}
            avatar= {
                <Paper style={{height: 40, width: 40, margin: "0 10", textAlign: 'center',
                display: 'inline-block', backgroundColor:"#" + this.HexToStr((this.props.data.color >>> 8), 6)}} zDepth={1} />
            }/>


            <CardMedia overlay={<CardTitle title={this.props.data.scene} subtitle={this.props.data.model} />}>
            <img src={"http://suidev.oss-cn-hangzhou.aliyuncs.com/render/material/middle/" + this.HexToStr(this.props.data.id, 8) + ".png"} alt="" />
            </CardMedia>
            </Card>
            </div>
        );
    }
}

export default MaterialItem;
