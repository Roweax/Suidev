import React from 'react';
import PropTypes from 'prop-types';

import RaisedButton from 'material-ui/RaisedButton';
import './Pager.css';
/**
* 父组件调用时需要传4个props
* start : 查询的起始记录位置
* size  :　每页记录条数
* total : 总记录数
* pageIndexChange : 页码改变的回调，目录回传的是起始记录位置（因为我的业务的关系）
*
* props可以根据具体业务修改，只需要在componentDidMount方法里面构造好pageIndex(当前页，1开始),pageNum（总页数）
* 回调参数也可以根据需要构造
*
* 调用方法：<Pagination key='pagination' pageIndexChange={this.pageChangeHandle} {...this.state} />
*
*/
//分页组件

const style = {
    minWidth:40,
    margin: 10,
};


export default class Page extends React.Component{

      static defaultProps = {

              pageIndexChange:()=>{},
              index:0,
              total:10,
              onChange:()=>{}
      };

    constructor() {
        super();
        this.state = {
            pageIndex : 1,
            showLinkNum : 10 //每次显示的页数
        }
    }
    componentDidMount (){

        const pageIndex = this.props.index + 1;
        const pageTotal = this.props.total;

        this.setState(Object.assign({},
            this.props,
            {pageIndex:pageIndex, pageTotal:pageTotal}));
        }

        //控制页码跳转的函数
        handleChange(index){
            this.setState({pageNum:this.state.pageNum ,pageIndex:index});
            this.props.onChange(index - 1);
        }
        render(){
            var arrFirst = [];//首页和前一页
            var arrLast = [];//尾页和后一页
            var arrLinkShow = []; //每次显示的页码
            var prevDisplay = 1 === this.state.pageIndex ? 'disabled': ''; //当前页为1时，首页和前一页失效
            var lastDisplay = this.state.pageNum === this.state.pageIndex ? 'disabled':'';//当前页为最后一页时，尾页和后一页失效
            //var startIndex = (Math.ceil(this.state.pageIndex/this.state.showLinkNum)-1) * this.state.showLinkNum + 1;//每次显示页数的开始页
            //var endIndex = Math.min(startIndex + this.state.showLinkNum,(this.state.pageNum+1));//每次显示页数的结束页
            var start_page = 1;
            var end_page = 10;
            for ( let i = start_page; i　<= end_page; i++ ) {
                var currentIndexDisplay = i === this.state.pageIndex ? 'active' : '';
                arrLinkShow.push(
                    <li key = {i} className = {currentIndexDisplay}>

                    <RaisedButton label={i} primary={this.state.pageIndex === i} style={style} onClick={() => { this.handleChange(i);}}>
                    </RaisedButton>
                    </li>
                )
            }
            arrFirst.push(
                <li key="first" className = {prevDisplay}>
                <RaisedButton label="首页" style={style}/>
                </li>
            );
            arrFirst.push(
                <li key = "1" className = {prevDisplay}>
                <RaisedButton label="<" style={style}/>
                </li>
            );
            arrLast.push(
                <li key ={this.state.pageNum} className = {lastDisplay} >

                <RaisedButton label=">" style={style}/>
                </li>
            );
            arrLast.push(
                <li key = "last" className = {lastDisplay}>
                <RaisedButton label="尾页" style={style}/>
                </li>
            );
            return (
                <nav className="text-right" key="page">
                <ul key='page-ul' className="pagination">
                {arrFirst}
                {arrLinkShow}
                {arrLast}
                </ul>
                </nav>
            )
        }
    }

    Page.propTypes = {
        pageIndexChange:PropTypes.func.isRequired,
        index:PropTypes.number.isRequired,
        total:PropTypes.number.isRequired,
        onChange:PropTypes.func.isRequired
    }
