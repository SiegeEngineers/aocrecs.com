import React from 'react'
import { split } from 'apollo-link'
import { ApolloClient } from 'apollo-client';
import Analytics from 'react-router-ga'
import DateFnsUtils from '@date-io/date-fns'
import {InMemoryCache, defaultDataIdFromObject} from 'apollo-cache-inmemory'
import { WebSocketLink } from 'apollo-link-ws'
import { getMainDefinition } from 'apollo-utilities'

import {ThemeProvider} from '@material-ui/styles'
import {ApolloProvider} from 'react-apollo'
import {BrowserRouter} from 'react-router-dom'
import {MuiPickersUtilsProvider} from 'material-ui-pickers'
import theme from './theme.js'
import Layout from './Layout.js'

const { createUploadLink } = require('apollo-upload-client')

const cache = new InMemoryCache({
  dataIdFromObject: object => {
    switch (object.__typename) {
      case 'User': return `${object.platform_id}:${object.id}`
      default: return defaultDataIdFromObject(object)
    }
  }
})

const wsLink = new WebSocketLink({
  uri: process.env.REACT_APP_API.replace('http', 'ws'),
  options: {
    reconnect: true
  }
})

const link = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  createUploadLink({uri: process.env.REACT_APP_API})
)

const client = new ApolloClient({cache, link})

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
