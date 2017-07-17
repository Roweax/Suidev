import React, { Component } from 'react';
import './DevelopPage.css';

import Chip from 'material-ui/Chip';

import Paper from 'material-ui/Paper';
import Divider from 'material-ui/Divider'



const paper_style = {
    padding : '15px',
    width:'100%',
    height :'100%',
    textAlign: 'center',
    display: 'inline-block',
};

const styles = {
    chip: {
        margin: 4,
    },
    wrapper: {
        display: 'flex',
        flexWrap: 'wrap',
    },
};

class DevelopPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            logs : [],
            open : false
        };
    }


    render() {
        return (
            <div style = {{width:'800px', margin:'20px auto'}}>
            <Paper style = {{padding:'40px'}}>
            <h1 style={{textAlign:'center'}} >关于</h1>
            <div style={styles.wrapper}>
            <Chip style={styles.chip}>Html5</Chip>
            <Chip style={styles.chip}>JavaScript</Chip>
            <Chip style={styles.chip}>C++</Chip>
            <Chip style={styles.chip}>Python</Chip>
            <Chip style={styles.chip}>React</Chip>
            <Chip style={styles.chip}>Material-UI</Chip>
            <Chip style={styles.chip}>ECharts</Chip>
            <Chip style={styles.chip}>SyntaxHighlighter</Chip>
            <Chip style={styles.chip}>flask</Chip>
            <Chip style={styles.chip}>flask-restful</Chip>
            <Chip style={styles.chip}>blender</Chip>
            <Chip style={styles.chip}>Aliyun</Chip>
            <Chip style={styles.chip}>AWS</Chip>
            </div>
            <h3>概述</h3>
            <p>这是一个通过脚本随机生成并渲染3D场景的演示网站。Planet（星球）页面展示的是随机生成的星球，Material（材质）页面展示的是随机材质在环境光照下效果，Geometry（几何体）页面展示的是随机几何体组合。Info（信息）页面可以查看记录以及调整生成任务的优先级。</p>

            <Divider />
            <h3>系统</h3>
            <p>本站使用阿里云和AWS的系列产品</p>
            <p>服务器：</p>
            <ul>
            <li>1核CPU，4GB内存，Debian 8.6 64位操作系统（阿里云华东 ESC ecs.mn4.small）</li>
            <li>1核CPU，1GB内存，Ubuntu 16.04 64位操作系统（阿里云美国西部 ESC ecs.xn4.small）</li>
            <li>1核CPU，2GB内存，Ubuntu 16.04 64位操作系统（AWS美国西部 EC2 t2.micro）</li>
            </ul>
            <p>数据库：</p>
            <ul>
            <li>阿里云RDS版 MySQL 5.5</li>
            </ul>
            <p>对象存储：</p>
            <ul>
            <li>阿里云OSS</li>
            </ul>

            <Divider />
            <h3>应用</h3>
            <p>前端开发使用React。React是始于Facebook的一套JS框架，基于组件和状态的模式适合快速构建Web应用。React的Material-UI库有较好的交互和视觉效果。Info页面使用EChart显示图表。</p>
            <p>后端使用Python语言开发，采用flask作为Web应用框架，并使用使用Flask-RESTful扩展为前端提供RESTful API。使用Python作为后端语言的原因是Python有大量成熟的扩展库，适合快速开发。并且本站所依赖的开源渲染引擎Blender也是使用Python作为脚本语言。</p>
            <p>C++。Planet和Material页面的场景都是使用现有的场景文件配合Python脚本修而成的，而Geometry页面的场景完全是使用C++基于算法生成的。</p>
            </Paper>
            </div>
        );
    }
}

export default DevelopPage;
