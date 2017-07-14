import React, {Component} from 'react';
import './MaterialPage.css';

import MaterialItem from './MaterialItem.js';
import FlatButton from 'material-ui/FlatButton';
import Toggle from 'material-ui/Toggle';

import Dialog from 'material-ui/Dialog';
import Page from '../components/Pager.js';

var testData = {
    id: 1
};

class MaterialPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            materials: [],
            open: false,
            pageIndex: 0
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

    handleOpen = () => {
        this.setState({
            open: true
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
            <Dialog title="Material" actions={actions} modal={true} open={this.state.open}>
            Only actions can close this dialog.
            </Dialog>
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
