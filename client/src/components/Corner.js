import React, { Component } from 'react';
require('./Corner.css');

class Corner extends Component {
    render() {
        return (
            <div className = 'Item'>
            <div className = 'filter'></div>
            <div className = 'top'></div>
            <div className = 'bottom'></div>
            </div>
        );
    }
}
export default Corner;
