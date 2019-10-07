import React from 'react'
import CircularProgress from '@material-ui/core/CircularProgress'
import {Query} from 'react-apollo'

export default ({query, variables, children}) => {
  return (
    <Query query={query} variables={variables}>
      {({ loading, error, data }) => {
        if (loading) return <CircularProgress />
        if (error) return error.message
        return children(data)
      }}
    </Query>
  )
}
