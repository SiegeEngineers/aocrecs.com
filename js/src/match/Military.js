import React from 'react'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'

import Help from '../util/Help'
import DataQuery from '../util/DataQuery'
import PlayerChart from './PlayerChart'
import BarChart from './BarChart'
import GetMilitary from '../graphql/Military'


const Military = ({match}) => {
  const customFilter = (u) => !['Villager', 'Fishing Ship', 'Trade Cart'].includes(u.name)
  return (
    <DataQuery query={GetMilitary} variables={{match_id: match.id}}>
      {(data) => (
        <>
        <Typography variant='h6'>Trained Units <Help text='Number of units by type trained in the selected interval' /></Typography>
        <BarChart match={data.match} dataKey='units_trained' customFilter={customFilter} defaultInterval={15} />
        <Grid container>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='kills' title='Kills' skipzero={true} /></Grid>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='deaths' title='Deaths' skipzero={true} /></Grid>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='kd_delta' title='Delta' help="Kills minus deaths" skipzero={true} /></Grid>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='razes' title='Razes' skipzero={true} help="Buildings destroyed" /></Grid>
        </Grid>
        </>
      )}
    </DataQuery>
  )
}


export default Military
