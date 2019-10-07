import React, {setGlobal} from 'reactn'
import ReactDOM from 'react-dom'
import './bootstrap'
import App from './App'

setGlobal({
  search: {}
})

ReactDOM.render(<App />, document.getElementById('root'))
