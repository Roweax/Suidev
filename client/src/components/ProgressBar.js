import React, { Component } from 'react';
//import './StartMap.css';

class ProgressBar extends Component {
    render() {
        return (
            <div style="height:10px; width:100%; position:relative; float:left; background-color:rgba(255, 255, 255, 0.5)">
            <div style="width:100%; height:100%; padding:3px; position:absolute; box-sizing:border-box;">
            <div :style="{width:value + '%', height:'100%', backgroundColor:'rgba(255, 255, 255, 1.0)'}">
            </div>
            </div>
            </div>
        );
    }
}

export default ProgressBar;
