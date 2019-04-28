import React from 'react'
import ApolloClient from 'apollo-boost'
import {InMemoryCache, defaultDataIdFromObject} from 'apollo-cache-inmemory'
import {ThemeProvider} from '@material-ui/styles'
import {ApolloProvider} from 'react-apollo'
import {BrowserRouter} from 'react-router-dom'

import theme from './theme.js'
import Layout from './Layout.js'

const cache = new InMemoryCache({
  dataIdFromObject: object => {
    switch (object.__typename) {
      case 'StatItem': return object.id + Math.floor((Math.random() * 100000) + 1).toString()
      default: return defaultDataIdFromObject(object)
    }
  }
})

const client = new ApolloClient({
  uri: process.env.REACT_APP_GRAPHQL,
  cache: cache
})

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <ApolloProvider client={client}>
          <Layout />
        </ApolloProvider>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
