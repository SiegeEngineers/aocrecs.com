import React from 'react'
import ApolloClient from 'apollo-boost'
import Analytics from 'react-router-ga'
import DateFnsUtils from '@date-io/date-fns'
import {InMemoryCache, defaultDataIdFromObject} from 'apollo-cache-inmemory'
import {ThemeProvider} from '@material-ui/styles'
import {ApolloProvider} from 'react-apollo'
import {BrowserRouter} from 'react-router-dom'
import {MuiPickersUtilsProvider} from 'material-ui-pickers'
import theme from './theme.js'
import Layout from './Layout.js'

const cache = new InMemoryCache({
  dataIdFromObject: object => {
    switch (object.__typename) {
      case 'User': return `${object.platform_id}:${object.id}`
      default: return defaultDataIdFromObject(object)
    }
  }
})

const client = new ApolloClient({
  uri: process.env.REACT_APP_API,
  cache: cache
})

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Analytics id={process.env.REACT_APP_GTM}>
          <ApolloProvider client={client}>
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
              <Layout />
            </MuiPickersUtilsProvider>
          </ApolloProvider>
        </Analytics>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
