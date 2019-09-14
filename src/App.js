import React from 'react'
import ApolloClient from 'apollo-boost'
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
      case 'StatItem': return object.id.toString() + object.label + object.count.toString()
      default: return defaultDataIdFromObject(object)
    }
  }
})

const client = new ApolloClient({
  uri: process.env.REACT_APP_API + '/graphql',
  cache: cache
})

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <ApolloProvider client={client}>
          <MuiPickersUtilsProvider utils={DateFnsUtils}>
            <Layout />
          </MuiPickersUtilsProvider>
        </ApolloProvider>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
