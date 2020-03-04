import React from 'react'

import Grid from '@material-ui/core/Grid'

import PlayerChart from './PlayerChart'
import {getHasTeams, getIsNomad} from '../util/Shared'
import DataQuery from '../util/DataQuery'
import GetCharts from '../graphql/Charts'
import GetChartsTG from '../graphql/ChartsTG'


const Charts = ({match}) => {
  const hasTeams = getHasTeams(match.team_size)
  const isNomad = getIsNomad(match.map_name)
  return (
    <DataQuery query={hasTeams ? GetChartsTG : GetCharts} variables={{match_id: match.id}}>
      {(data) => (
        <Grid container>
          {!hasTeams && <>
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='apm' field='actions' title='Effective APM' help='Instantaneous effective APM measured at 30 second sample rate. Each point represents the number of actions in the preceding minute. Effective APM only counts actions that change the game state. For example, building or moving a unit count, but activating a control group does not.'/>
          </Grid>
          <Grid item xs={6}>
            {!isNomad && <PlayerChart players={data.match.players} group='map_control' field='control_percent' title='Map Control' help='Map control as represented by action proximity to enemy, capturing both presence and attention of the player.' custom={{yaxis: {min: 0, max: 100, forceNiceScale: false, labels: {formatter: (v, i) => `${Math.round(v)}%`}}}}/>}
          </Grid>
          </>}
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='timeseries' field='population' title='Total Population' />
          </Grid>
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='timeseries' field='military' title='Military Population' />
          </Grid>
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='timeseries' field='value_objects_destroyed' title='Total Value Destroyed' help='Cumulative sum of resources spent by enemy on units and buildings destroyed by the player.' />
          </Grid>
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='timeseries' field='value_current_units' title='Unit Value' help='Sum of resources spent by player on units and buildings currently in play.' />
          </Grid>
        </Grid>
      )}
    </DataQuery>
  )
}

export default Charts
