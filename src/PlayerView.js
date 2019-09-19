import React from 'react'
import Grid from '@material-ui/core/Grid'

import User from './User'
import RelatedMatches from './util/RelatedMatches'

import GetUser from './graphql/User'

const PlayerView = ({match}) => {
  const platform_id = match.params.pid
  return (
    <RelatedMatches
        query={GetUser}
        variables={{user_id: match.params.id, platform_id: platform_id}}
        field='user'
      >
        {(data) => (
        <Grid container spacing={24}>
          <Grid item xs={2}>
            <User user={data} />
          </Grid>
        </Grid>
      )}
    </RelatedMatches>
  )
}

export default PlayerView
