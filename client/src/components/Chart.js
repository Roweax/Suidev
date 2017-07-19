import React, { Component } from 'react';
import './Chart.css';

var echarts = require('echarts');

class Chart extends Component {
	constructor(props) {
		super(props);
		this.state = {
			data : {}
		};
	}

	componentDidMount() {
		fetch('/api/newest', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            return response.json();
        }).then((json) => {
            var data = JSON.parse(json);
            this.setState( {
            	data : data
            })
			this.showChart(this.state.data)
        }).catch(err => {
            console.log('fetch error' + err);
        });
	}

	componentWillMount() {
		var info = this.props.data;
		//HTML5规定自定义属性要以data-开头，这样的可以如下取
		console.log(this.props['data-info'])
		//Action.getInfo(info);
	}


	componentDidUpdate() {
	}

	toChartItem(item) {
		let date = new Date(item["create_time"]);
		let day = new Date();
		day.setFullYear(date.getFullYear(), date.getMonth(), date.getDate());
		let x = (day - new Date()) / 3600 / 24 / 1000 + 30;
		let y = date.getHours() + date.getMinutes() / 60.0;
		let render_time = item["render_time"];
		let kind = item["name"];
		return [x, y, render_time, item["name"]];
	}

	showChart(dataSet){
		var myChart = echarts.init(document.getElementById('chart'));

/*
		var data = [
			[[1,2,17096869,'Australia',1990],[2,0,27662440,'Canada',1990],[3,1,1154605773,'China',1990]],
			[[9.5,2.5,23968973,'Australia',2015],[10,1,35939927,'Canada',2015],[10,2,1376048943,'China',2015]]
		];
*/		
		var data = [
			[],
			[],
			[]
		];
		for(var index in dataSet){
			let item = dataSet[index];
            let ci = this.toChartItem(item);
            if (item['category'] == 'Planet') {
            	data[0].push(ci);
            } else if (item['category'] == 'Material') {
            	data[1].push(ci);
            } else if (item['category'] == 'Geometry') {
            	data[2].push(ci);
            } 
        } 
		var hours = ['0'];
		for(var i = 1; i <= 24; i++) {
			hours.push(i);
		}
		var days = [];
		for(var i = 0; i <= 30; i++) {
			let day_now = new Date()
			day_now.setDate(day_now.getDate() - 30 + i);
			days.push((day_now.getMonth() + 1) + '/' + day_now.getDate());
		}

		var option = {
			title: {
				text: 'Chart'
			},
			legend: {
				right: 10,
				data: ['Planet', 'Material', 'Figure']
			},
			xAxis: {
        		type: 'category',
        		data: days,
				splitLine: {
            		show: true,
            		lineStyle: {
                		color: '#999',
                		type: 'dashed'
                	}
           		},
        		boundaryGap: false,
           		axisLabel: {
            		interval: 4
        		}
			},
			yAxis: {
        		type: 'category',
        		data: hours,
				splitLine: {
            		show: true,
            		lineStyle: {
                		color: '#999',
                		type: 'dashed'
                	}
           		},
        		boundaryGap: false,
           		axisLabel: {
            		interval: 3
        		},
				scale: false
			},
			series: [{
				name: 'Planet',
				data: data[0],
				type: 'scatter',
				symbolSize: function (data) {
					return Math.sqrt(data[2]) / 10;
				},
				label: {
					emphasis: {
						show: false,
						formatter: function (param) {
							return param.data[3];
						},
						position: 'top'
					}
				},
				itemStyle: {
					normal: {
						shadowBlur: 10,
						shadowColor: 'rgba(120, 36, 50, 0.5)',
						shadowOffsetY: 3,
						color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
							offset: 0,
							color: 'rgb(251, 118, 123)'
						}, {
							offset: 1,
							color: 'rgb(204, 46, 72)'
						}])
					}
				}
			}, {
				name: 'Material',
				data: data[1],
				type: 'scatter',
				symbolSize: function (data) {
					return Math.sqrt(data[2]) / 10;
				},
				label: {
					emphasis: {
						show: false,
						formatter: function (param) {
							return param.data[3];
						},
						position: 'top'
					}
				},
				itemStyle: {
					normal: {
						shadowBlur: 10,
						shadowColor: 'rgba(25, 100, 150, 0.5)',
						shadowOffsetY: 5,
						color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
							offset: 0,
							color: 'rgb(129, 227, 238)'
						}, {
							offset: 1,
							color: 'rgb(25, 183, 207)'
						}])
					}
				}
			} , {
				name: 'Geometry',
				data: data[2],
				type: 'scatter',
				symbolSize: function (data) {
					return Math.sqrt(data[2]) / 10;
				},
				label: {
					emphasis: {
						show: false,
						formatter: function (param) {
							return param.data[3];
						},
						position: 'top'
					}
				},
				itemStyle: {
					normal: {
						shadowBlur: 10,
						shadowColor: 'rgba(25, 100, 150, 0.5)',
						shadowOffsetY: 5,
						color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
							offset: 0,
							color: 'rgb(129, 227, 238)'
						}, {
							offset: 1,
							color: 'rgb(25, 183, 207)'
						}])
					}
				}
			}]};

			myChart.setOption(option);
		}


		render() {
			return (
				<div id="chart" style = {{width:'100%', height:'100%'}}></div>
			);
		}
	}
	export default Chart;
