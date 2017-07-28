import React, { Component } from 'react';
import './GeometryPage.css';

import GeometryItem from './GeometryItem.js';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Page from '../components/Pager.js';
import Toggle from 'material-ui/Toggle';

class GeometryPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            geometries : [{}, {},{},{}],
            open : false,
            code : ""
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

        fetch('https://raw.githubusercontent.com/Roweax/Suidev/master/server/__main__.py'
        ).then((response) => {
            return response.text();
        }).then((text) => {
            console.log(text);
            
            this.setState({
                code : text
            });
        }).catch(err => {
            console.log("fetch error" + err);
        });
    };

    handleClose = () => {
        this.setState({open: false});
    };



  handleExpandChange = (expanded) => {
    this.setState({expanded: expanded});
  };

  handleToggle = (event, toggle) => {
    this.setState({expanded: toggle});
  };

  handleExpand = () => {
    this.setState({expanded: true});
  };

  handleReduce = () => {
    this.setState({expanded: false});
  };



    render() {
        let code = "class OgreSkeletonReader{std::ostream errors;}\nclass OgreSkeletonReader{std::ostream errors;}\nclass OgreSkeletonReader{std::ostream errors;}\nclass OgreSkeletonReader{std::ostream errors;}\n";
        const actions = [
            <FlatButton label="Cancel" primary={true} onTouchTap={this.handleClose}/>,
            <FlatButton label="Submit" primary={true} disabled={true} onTouchTap={this.handleClose}/>,
        ];

        let temp = <div>
                <FlatButton label="Cancel" primary={true} onTouchTap={this.handleOpen}/>
  <script type="text/javascript" src="./syntaxhighlighter.js"></script>

            {this.state.geometries.map(
                function (item) {
                    return (
                        <GeometryItem key={item.id} data={item}></GeometryItem>
                    )
                }
            )}</div>


        return (
            <div style={{ margin:'40px',display:'flex', flexWrap:'wrap', justifyContent:'center'}}>

                <FlatButton label="Cancel" primary={true} onTouchTap={this.handleOpen}/>
            <Dialog modal={false} open={this.state.open} onRequestClose={this.handleClose} >
            <div style={{position:'relative'}}>
            <div style={{position:'absolute'}}>
            <pre className="brush: cpp;">
            {this.state.code}
            </pre>
            {
                this.componentDidMount()
            }
            </div>
            <img src='./1.jpeg' style={{height:'100%', width:'100%'}} ></img>
            </div>
            </Dialog>
            In Develop
            <Page start = {1} size = {9} total = {100} ></Page>

            <Card style={{width : 800}} expanded={this.state.expanded} onExpandChange={this.handleExpandChange}>
        <CardHeader
          title="C++ Source Code"
          subtitle="public files"
          actAsExpander={true}
          showExpandableButton={true}
        />
        <CardTitle title="C++ Source Code" subtitle="library files" expandable={true} />
        <CardText expandable={true}>
          
            <pre className="brush: cpp;">
            {this.state.code}
            </pre>
        </CardText>
      </Card>
            </div>
        );
    }
}

export default GeometryPage;
