import React, { Component } from 'react';
import './GeometryPage.css';

import GeometryItem from './GeometryItem.js';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Page from '../components/Pager.js';
import Toggle from 'material-ui/Toggle';
import RaisedButton from 'material-ui/RaisedButton';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/styles';


class GeometryPage extends Component {
    codes = ["UBatch.h", "Color.h", "Math.h"];

    constructor(props) {
        super(props);
        this.state = {
            geometries : [{}, {},{},{}],
            open : false,
            item_code : "",
            code : "",
            show_item_code : false,
            large_img : "",
            code_select : 0
        };
    }

    componentDidMount() {
        
        
    }

    RenderCode()
    {

        var oldjs = document.getElementById('highlightjs'); 
        if(oldjs) oldjs.parentNode.removeChild(oldjs); 
        const script = document.createElement("script");
        script.id = 'highlightjs';
        script.src = "./syntaxhighlighter.js";
        script.async = true;
        document.body.appendChild(script);

        var oldcss = document.getElementById('highlightcss'); 
        if(oldcss == null)
        {
            const link = document.createElement("link");
            link.id = 'highlightcss';
            link.type="text/css";
            link.rel="stylesheet";
            link.href="./theme.css";
            document.body.appendChild(link);
        }
    }



    ShowItemCode(index) {
        fetch('http://suidev.oss-cn-hangzhou.aliyuncs.com/code/2'
        //fetch('https://raw.githubusercontent.com/Roweax/Suidev/master/server/__main__.py'
        ).then((response) => {
            return response.text();
        }).then((text) => {
            this.setState({
                item_code : text
            }, this.RenderCode());
        }).catch(err => {
            console.log("fetch error" + err);
        });
    }


    ShowCode(index) {
        fetch('http://suidev.oss-cn-hangzhou.aliyuncs.com/code/' + this.codes[index]
        //fetch('https://raw.githubusercontent.com/Roweax/Suidev/master/server/__main__.py'
        ).then((response) => {
            return response.text();
        }).then((text) => {
            this.setState({
                code : text,
                code_select : index
            }, this.RenderCode());
        }).catch(err => {
            console.log("fetch error" + err);
        });
    }

    handleOpen = (url) => {
        this.setState({open: true, large_img: url});
        this.ShowItemCode(0);
        
    };

    handleClose = () => {
        this.setState({open: false});
    };

  handleShowItemCode = (event, checked) => {
        this.setState({show_item_code : checked});
  }

  handleExpandChange = (expanded) => {
    this.setState({expanded: expanded}, ()=>{if(expanded) this.ShowCode(0)});
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

  handleShowCode = (index) => {
    this.ShowCode(index);
    console.log("download code")
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

            <Dialog modal={false} open={this.state.open} onRequestClose={this.handleClose} >
            <Toggle label="Show Code" labelPosition="left" style={{width:160, margin:'10px 0'}} onToggle={(event, checked)=>{this.handleShowItemCode(event, checked)}}/>
            <div style={{position:'relative', height:405, width:'720'}}>
            <div style={{position:'absolute', height:405, width:'720', display:this.state.show_item_code ? 'inline' : 'none'}}>
            <pre id="item_code" className="brush: cpp;" style={{maxHeight: 200}}>
            {this.state.item_code}
            </pre>
            </div>
            <img src={this.state.large_img} style={{width:'100%', verticalAlign:'middle'}} ></img>
            </div>
            </Dialog>
            <GeometryItem onShowLarge ={(event) => this.handleOpen(event)}/><GeometryItem/>
            <Card style={{width : 1000}} expanded={this.state.expanded} onExpandChange={this.handleExpandChange}>
        <CardHeader
          title="C++ Source Code"
          subtitle="public files"
          actAsExpander={true}
          showExpandableButton={true}
        />
        <CardText expandable={true}>
        <div style={{display:'flex'}}>
          {this.codes.map(
                function (item, index) {
                    return (
                         <RaisedButton key={index} label={<span style = {{textTransform:'none'}}>{item}</span>} primary={this.state.code_select == index} onTouchTap={(event) => this.handleShowCode(index)} style={{margin:'10px'}}/>
                    )
                },
                this
            )}
          </div>
          <div >
            <pre className="brush: cpp;">
            {this.state.code}
            </pre>
            </div>
        </CardText>
      </Card>
            </div>
        );
    }
}

export default GeometryPage;
