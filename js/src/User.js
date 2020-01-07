import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Table from '@material-ui/core/Table'
import TableHead from '@material-ui/core/TableHead'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'
import UserIcon from 'mdi-react/AccountIcon'

import Chart from './util/Chart'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'

const RateChart = ({id, data, label}) => {
  return (
    <>
    {data.length > 0 && <>
      <Typography variant='h5'>{label}</Typography>
      <Chart id={id} width='400' height='150' timeseries={true} series={[{data: data.map(d => [d.date, d.count])}]} />
      </>}
    </>
  )
}

const Information = ({user}) => {
  return (
    <>
      <Typography variant='h5'>Information</Typography>
      <Table>
        <TableBody>
          {user.person && user.person.aliases.length > 0 && <TableRow><TableCell>Aliases</TableCell><TableCell>{user.person.aliases.join(', ')}</TableCell></TableRow>}
          <TableRow><TableCell>Most Wins: Map</TableCell><TableCell>
              <AppLink path={['maps', user.top_map.name]} text={user.top_map.name} />
          </TableCell></TableRow>
          <TableRow><TableCell>Most Wins: Civilization</TableCell><TableCell>
              <AppLink path={['civilizations', user.top_civilization.dataset_id, user.top_civilization.id]} text={user.top_civilization.name} />
          </TableCell></TableRow>
          <TableRow><TableCell>Most Matches: Dataset</TableCell><TableCell>{user.top_dataset.name}</TableCell></TableRow>
        </TableBody>
      </Table>
    </>
  )
}

const Rankings = ({user}) => {
  return (
    <>
      <Typography variant='h5'>Rankings</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Ladder</TableCell>
            <TableCell align='right'>Rank</TableCell>
            <TableCell align='right'>Rate</TableCell>
            <TableCell align='right'>Streak</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {user.meta_ranks.map(rank => (
            <TableRow key={rank.ladder.id}>
              <TableCell>
                <Typography noWrap><AppLink path={['ladders', rank.ladder.id]} text={rank.ladder.name} /></Typography>
              </TableCell>
              <TableCell align='right'>{rank.rank}</TableCell>
              <TableCell align='right'>{rank.rating}</TableCell>
              <TableCell align='right'>{rank.streak > 0 ? '+' + rank.streak : rank.streak}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  )
}

const User = ({user}) => {
  return (
    <Card>
      <CardIconHeader
        icon={<UserIcon />}
        title={user.name + (user.canonical_name && user.canonical_name !== user.name ? ' (aka ' + user.canonical_name + ')': '')}
      />
      <CardContent>
        <Grid container spacing={24}>
          <Grid item>
            <Grid container spacing={24}>
              <Grid item>
                <Information user={user} />
              </Grid>
              <Grid item>
                <Rankings user={user} />
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Grid container spacing={24}>
              {user.meta_ranks.map(rank => (
              <Grid item key={rank.ladder_id}>
                <RateChart id={rank.ladder_id} data={rank.rate_by_day} label={rank.ladder.name} />
              </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  )
}

export default User
