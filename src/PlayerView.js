import React from 'react'

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
        <User user={data} />
      )}
    </RelatedMatches>
  )
}

export default PlayerView
