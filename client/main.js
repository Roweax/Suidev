import React from 'react'
import ReactDOM from 'react-dom'

class Hello extends React.Component {
  render(){
    return(
      <h1>Hello333</h1>
    )
  }
}

ReactDOM.render(<Hello />,document.getElementById('app'))