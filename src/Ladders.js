import React from 'react'

import ExpansionPanel from '@material-ui/core/ExpansionPanel'
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary'
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails'
import ExpandMoreIcon from '@material-ui/icons/ExpandMore'
import Grid from '@material-ui/core/Grid'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import AppLink from './util/AppLink'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'

import VooblyUser from './VooblyUser.js'

import GetLadders from './graphql/Ladders.js'
import GetVooblyUser from './graphql/VooblyUser.js'

const VooblyUserWrapper = ({user_id}) => {
  const field = 'voobly_user'
  return (
    <RelatedMatches query={GetVooblyUser} variables={{user_id}} field={field}>
      {(data) => (
        <VooblyUser voobly_user={data} />
      )}
  </RelatedMatches>
  )
}

const RankTable = ({ladder_id, ranks, selected}) => {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Rank</TableCell>
          <TableCell>Name</TableCell>
          <TableCell align='right'>Rating</TableCell>
          <TableCell align='right'>Wins</TableCell>
          <TableCell align='right'>Losses</TableCell>
          <TableCell align='right'>Streak</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {ranks.map(rank => (
          <TableRow key={rank.rank} selected={selected === rank.user.id}>
            <TableCell>{rank.rank}</TableCell>
            <TableCell>
              <AppLink path={['ladders', ladder_id, rank.user.id]} text={rank.user.name} />
            </TableCell>
            <TableCell align='right'>{rank.rating}</TableCell>
            <TableCell align='right'>{rank.wins}</TableCell>
            <TableCell align='right'>{rank.losses}</TableCell>
            <TableCell align='right'>{rank.streak}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

const LaddersView = ({match, history}) => {
  const ladder_id = parseInt(match.params.id)
  return (
    <DataQuery query={GetLadders}>
      {(data) => (
          <Grid container spacing={24}>
            <Grid item xs={6}>
            {data.meta_ladders.map(ladder => (
              <ExpansionPanel
                key={ladder.id}
                expanded={ladder_id === ladder.id}
                onChange={(o, e) => history.push(e ? '/ladders/' + ladder.id : '/ladders')}
              >
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><AppLink path={['ladders', ladder.id]} text={ladder.name} /></Typography>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                  <RankTable ladder_id={ladder.id} ranks={ladder.ranks} selected={ladder_id} />
                </ExpansionPanelDetails>
              </ExpansionPanel>
            ))}
          </Grid>
          {match.params.vid && <Grid item xs={6}>
            <VooblyUserWrapper user_id={match.params.vid} />
            </Grid>}
          </Grid>
      )}
    </DataQuery>
  )
}

export default LaddersView
