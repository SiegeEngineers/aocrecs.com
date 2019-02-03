import React from 'react'
import ApolloClient from 'apollo-boost'
import {ThemeProvider} from '@material-ui/styles'
import {ApolloProvider} from 'react-apollo'
import {BrowserRouter} from 'react-router-dom'

import theme from './theme.js'
import Layout from './Layout.js'

const client = new ApolloClient({
  uri: process.env.REACT_APP_GRAPHQL
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
