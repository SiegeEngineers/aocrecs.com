import React from 'react'

import Typography from '@material-ui/core/Typography'

import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'

import GetLatest from './graphql/Latest'


const Latest = ({match}) => {
  return (
    <RelatedMatches query={GetLatest} variables={{dataset_id: parseInt(match.params.id)}} field='latest'>
      {(data) => (
        <Typography variant='h3'>{data.matches.count.toLocaleString()} matches</Typography>
      )}
    </RelatedMatches>
  )
}

export default Latest
