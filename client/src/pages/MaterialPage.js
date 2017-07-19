import React, {Component} from 'react';
import './MaterialPage.css';

import MaterialItem from './MaterialItem.js';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import CircularProgress from 'material-ui/CircularProgress';
import Page from '../components/Pager.js';

const dialogStyle = {
  maxWidth: 'none',
  width : 1200
};

class MaterialPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            materials: [],
            open: false,
            pageIndex: 0,
            large_img : ''
        };
    }

    componentDidMount() {
        this.loadPage(this.state.pageIndex);
    }

    loadPage(index) {
        fetch('/api/materials/' + index, {
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
                materials: data.data
            });
        }).catch(err => {
            console.log('fetch error' + err);
        });
    }

    handleOpen = (large_img) => {
        this.setState({
            open: true,
            large_img : large_img
        });
    };

    handleClose = () => {
        this.setState({
            open: false
        });
    };

    pageChange = (index) => {
        this.loadPage(index);
        //console.log(index);
    }

    render() {
        const actions = [
            <FlatButton label="Close" primary={true} onTouchTap={this.handleClose} />
        ];

        return (
            <div style={{ margin:40, display:'flex', flexWrap:'wrap'}}>
            <Dialog actions={actions} modal={false} open={this.state.open} style={dialogStyle}  onRequestClose={this.handleClose}  >
            <img src={this.state.large_img} style = {{width:'720', height: '405'}}/>
            </Dialog>
            {this.state.materials.length === 0 ? <div style={{ width:'100%', height:700}}></div>: ''}
            {this.state.materials.map(
                function (item) {
                    return (
                        <MaterialItem data={item} onShowLarge ={(event) => this.handleOpen(event)}></MaterialItem>
                    )
                },
                this
            )}
            <Page index={0} total={20} onChange={this.pageChange}></Page>
            </div>
        );
    }
}

export default MaterialPage;
