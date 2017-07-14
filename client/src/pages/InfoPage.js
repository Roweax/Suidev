import React, { Component } from 'react';
import './InfoPage.css';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Toggle from 'material-ui/Toggle';
import RaisedButton from 'material-ui/RaisedButton';
import Checkbox from 'material-ui/Checkbox';

import Paper from 'material-ui/Paper';
import Chart from '../components/Chart.js'
import Task from '../components/Task.js'
import Page from '../components/Pager.js'

import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn,
} from 'material-ui/Table';


const paper_style = {
    padding : '15px',
    width:'100%',
    height :'100%',
    textAlign: 'center',
    display: 'inline-block',
};


const checkbox_style = {
    width: '80px',
};

class InfoPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            logs : [],
            open : false
        };
    }

    componentDidMount() {
    console.log("123")
        fetch('/api/logs/0' , {
            method: 'GET',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            return response.json();
        }).then((json) => {
            var data = JSON.parse(json);
            console.log(data)
            this.setState({
                logs : data.data
            });
        }).catch(err => {
            console.log("fetch error" + err);
        });
    }



    render() {
        return (
            <div style = {{width:'1000px', margin:'20px auto'}}>
            <div style = {{display: 'flex', minHeight :400}}>
            <div style = {{padding:'10px', width:'50%'}}>
            <Paper style={paper_style}>
            <Chart/>

            </Paper>
            </div>
            <div  style = {{padding:'10px',width:'50%'}}>

            <Paper style={paper_style}>
            <Task/>
            </Paper>
            </div>
            </div>

            <div style = {{padding:'10px'}}>

            <Paper style={paper_style}>
            <h1>Log</h1>
            <div style={{display:'flex'}}>
            <spawn style={{width:80}}></spawn>
            <Checkbox
            label="Galaxy"
            style = {checkbox_style} checked = {true}
            />
            <Checkbox
            label="Material"
            style = {checkbox_style} checked = {true}
            />
            <Checkbox
            label="Figure"
            style = {checkbox_style} checked = {true}
            />
            </div>
            <Table
            fixedHeader={true}>
            <TableHeader>
            <TableRow>
            <TableHeaderColumn>ID</TableHeaderColumn>
            <TableHeaderColumn>Name</TableHeaderColumn>
            <TableHeaderColumn>归类</TableHeaderColumn>
            <TableHeaderColumn width={30}>Images</TableHeaderColumn>
            <TableHeaderColumn width={30}>Video</TableHeaderColumn>
            <TableHeaderColumn>Time</TableHeaderColumn>
            </TableRow>
            </TableHeader>
            <TableBody displayRowCheckbox={true}
            deselectOnClickaway={true}
            showRowHover={true}
            >
            {this.state.logs.map(function (item) {
                return (

                    <TableRow key = {item.id}>
                    <TableRowColumn>{item.id}</TableRowColumn>
                    <TableRowColumn>{item.kind}</TableRowColumn>
                    <TableRowColumn>{item.category}</TableRowColumn>
                    <TableRowColumn width={30}>{item.image}</TableRowColumn>
                    <TableRowColumn width={30}>{item.video}</TableRowColumn>
                    <TableRowColumn>{item.create_time}</TableRowColumn>
                    </TableRow>
                )}
            )}


            </TableBody>
            </Table>
            </Paper>
            </div>
            </div>
        );
    }
}

export default InfoPage;
