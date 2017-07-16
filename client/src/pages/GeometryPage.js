import React, { Component } from 'react';
import './GeometryPage.css';

import GeometryItem from './GeometryItem.js';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import Page from '../components/Pager.js';

class GeometryPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            geometries : [{}, {},{},{}],
            open : false
        };
    }

    componentDidMount() {
        /*
        fetch('/api/geometries' , {
            method: 'GET',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json'
            }}
        ).then((response) => {
            return response.json();
        }).then((json) => {
            console.log(json);
            this.setState({
                geometries : JSON.parse(json)
            });
        }).catch(err => {
            console.log("fetch error" + err);
        });
        */
        const script = document.createElement("script");
        script.src = "./syntaxhighlighter.js";
        script.async = true;
        document.body.appendChild(script);

        const link = document.createElement("link");
        link.type="text/css";
        link.rel="stylesheet";
        link.href="./theme.css";
        document.body.appendChild(link);
    }

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    render() {
        let code = "class OgreSkeletonReader{std::ostream errors;}\nclass OgreSkeletonReader{std::ostream errors;}\nclass OgreSkeletonReader{std::ostream errors;}\nclass OgreSkeletonReader{std::ostream errors;}\n";
        const actions = [
            <FlatButton label="Cancel" primary={true} onTouchTap={this.handleClose}/>,
            <FlatButton label="Submit" primary={true} disabled={true} onTouchTap={this.handleClose}/>,
        ];

        return (
            <div style={{ margin:'40px',display:'flex', flexWrap:'wrap', justifyContent:'center'}}>

            <Dialog modal={false} open={this.state.open}>
            <div style={{position:'relative'}}>
            <div style={{position:'absolute'}}>
            <pre className="brush: cpp;">
            {code}
            </pre>
            {
                this.componentDidMount()
            }
            </div>
            <img src='./1.jpeg' style={{height:'100%', width:'100%'}} ></img>
            </div>
            </Dialog>

                <FlatButton label="Cancel" primary={true} onTouchTap={this.handleOpen}/>,
  <script type="text/javascript" src="./syntaxhighlighter.js"></script>

            {this.state.geometries.map(
                function (item) {
                    return (
                        <GeometryItem key={item.id} data={item}></GeometryItem>
                    )
                }
            )}

            <Page start = {1} size = {9} total = {100} ></Page>
            </div>
        );
    }
}

export default GeometryPage;
