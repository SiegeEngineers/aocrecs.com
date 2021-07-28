import React, {setGlobal} from 'reactn'
import ReactDOM from 'react-dom'
import App from './App'

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';

import '@fontsource/open-sans/300.css';
import '@fontsource/open-sans/400.css';
import '@fontsource/open-sans/600.css';
import '@fontsource/open-sans/700.css';

import '@fontsource/source-code-pro/400.css';
import '@fontsource/source-code-pro/700.css';

import '@fontsource/material-icons';

import './css/material.css'

setGlobal({
  search: {}
})

ReactDOM.render(<App />, document.getElementById('root'))
