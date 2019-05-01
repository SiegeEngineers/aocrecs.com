import React from 'react'

import Grid from '@material-ui/core/Grid'

import Match from './Match'
import DataQuery from './util/DataQuery'
import GetMatch from './graphql/Match'


const MatchView = ({match}) => {
  const match_id = parseInt(match.params.id)
  return (
    <DataQuery query={GetMatch} variables={{match_id}}>
      {(data) => (
      <Grid container spacing={24}>
        <Grid item>
          <Match match={data.match} />
        </Grid>
      </Grid>
      )}
    </DataQuery>
  )
}

export default MatchView
