import React, { Component } from 'react';
import './Task.css';
import Slider from 'material-ui/Slider';
import RaisedButton from 'material-ui/RaisedButton';

import Snackbar from 'material-ui/Snackbar';

class Task extends Component {
	constructor(props) {
		super(props);
		this.state = {
			prioritys : [],
			open: false,
			click_enable : true
		};
	}

	componentDidMount() {
		fetch('/api/tasks' , {
			method: 'GET',
			headers: {
				"Accept": "application/json",
				'Content-Type': 'application/json'
			}
		}).then((response) => {
			return response.json();
		}).then((json) => {
			this.setState({
				prioritys : JSON.parse(json)
			});
		}).catch(err => {
			console.log("fetch error" + err);
		});

	}

	componentWillMount() {

	}

	valueChange(index, event, newValue) {
		let p = this.state.prioritys;
		p[index].priority = parseInt(newValue, 10);
		this.setState(p);
	}

	save(e) {
		this.setState({
			click_enable: false,
		});
		fetch('/api/settasks' , {
			method: 'PUT',
			headers: {
				//"Accept": "application/json",
				'Content-Type': 'application/json'
			},
			body : JSON.stringify(this.state.prioritys)
		})
		.then((response) => {
			this.setState({
				open: true,
			});
			return response.json();
		})
		.then((json) => {
		})
		.catch(err => {
			this.setState({
				open: true,
			});
			console.log("fetch error" + err);
		});
	}


	handleTouchTap = () => {
		this.setState({
			open: true,
		});
	};

	handleRequestClose = () => {
		this.setState({
			open: false,
			click_enable :true
		});
	};

	componentDidUpdate() {
	}




	render() {
		return (
			<div style={{height:'100%', width:'100%'}}>
			<h2>Priority</h2>


			{
				this.state.prioritys.map(
					(item, index) => (<div key = {item.id}>
						<div>
						<p style={{textAlign:'left', float:'left'}}>{item.name}</p>
						<p style={{textAlign:'left', float:'right'}}>{item.priority}</p>
						</div>
						<Slider min={0} max={100} key={item.id} defaultValue = {item.priority}  onChange={(event, value) => this.valueChange(index, event, value)}/>
						</div>)
					)
				}
				<RaisedButton label="Save" primary={true} disabled = {!this.state.click_enable} style={{margin:'10px', float:'right'}} onTouchTap={() => this.save()} />
				<Snackbar
				open={this.state.open}
				message="Priority Saved"
				autoHideDuration={4000}
				onRequestClose={this.handleRequestClose}
				/>
				</div>
			);
		}
	}
	export default Task;
