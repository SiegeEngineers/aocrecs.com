import React from 'react'
import {makeStyles} from '@material-ui/styles'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Table from '@material-ui/core/Table'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'

import {TeamBody} from './Teams'
import {getHasTeams} from '../util/Shared'
import PlayerChart from './PlayerChart'
import BarChart from './BarChart'
import DataQuery from '../util/DataQuery'
import Help from '../util/Help'
import GetEconomy from '../graphql/Economy'


const useStyles = makeStyles(theme => ({
  narrowTable: {
    width: 'unset'
  }
}))


const Economy = ({match, size}) => {
  const classes = useStyles()
  const hasTeams = getHasTeams(size)
  return (
    <DataQuery query={GetEconomy} variables={{match_id: match.id}}>
      {(data) => (
      <>
        <Typography variant='h6'>Economy</Typography>
        <Table className={classes.narrowTable}>
          <TableHead>
            <TableRow>
              <TableCell>Player</TableCell>
              <TableCell align='right'>Town Centers</TableCell>
              <TableCell align='right'>Float <Help text={'Average amount of floating resources (aka current stockpile)'} small={true} /></TableCell>
              <TableCell align='right'>Dark Idle <Help text={'Length of time Town Center was idle in Dark Age'} small={true} /></TableCell>
              <TableCell align='right'>Housed <Help text={'Total time that production buildings could not train units due to lack of population space (not including reaching maximum population limit)'} small={true} /></TableCell>
              <TableCell align='right'>Pop Capped <Help text={'Time spent at maximum population'} small={true} /></TableCell>
              <TableCell align='right'>Villager Idle <Help text={'Cumulative villager idle time'} small={true} /></TableCell>
            </TableRow>
          </TableHead>
          <TeamBody teams={data.match.teams} hasTeams={hasTeams} span={7}>
            {(player) => (
              <>
                <TableCell align='right'>{player.metrics.total_tcs}</TableCell>
                <TableCell align='right'>{player.metrics.average_floating_resources.toLocaleString()}</TableCell>
                <TableCell align='right'>{player.metrics.dark_age_tc_idle}</TableCell>
                <TableCell align='right'>{player.metrics.seconds_housed}</TableCell>
                <TableCell align='right'>{player.metrics.seconds_popcapped}</TableCell>
                <TableCell align='right'>{player.metrics.seconds_villagers_idle}</TableCell>
              </>
            )}
          </TeamBody>
        </Table>
        <br />
        <Typography variant='h6'>Villager Allocation <Help text='Number of villagers tasked per resource in selected interval. Only the most recent job is counted if the villager switches resource mid-interval.' /></Typography>
        <BarChart match={data.match} dataKey='villager_allocation' customFilter={(u) => true} lockSelection={true} defaultInterval={5} />
        <Grid container>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='villagers' field='count' title='Villagers' /></Grid>
        <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='relic_gold' title='Relic Profit'skipzero={true} /></Grid>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='total_food' title='Food' /></Grid>
        <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='total_wood' title='Wood' /></Grid>
        <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='total_stone' title='Stone' /></Grid>
          <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='total_gold' title='Gold' /></Grid>
        </Grid>
      </>
      )}
    </DataQuery>
  )
}

export default Economy
