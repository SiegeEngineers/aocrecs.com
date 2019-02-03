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

import {map, flatten, join} from 'lodash'

import AppLink from './util/AppLink'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'

import GetEvents from './graphql/Events'
import GetSeries from './graphql/Series'
import GetTournament from './graphql/Tournament'

const Series = ({id}) => {
  const field = 'serie'
  return (
    <RelatedMatches query={GetSeries} variables={{id}} field={field}>
      {(data) => (
          <Typography variant='h6'>{data.name}</Typography>
      )}
    </RelatedMatches>
  )
}

const Tournament = ({tournament}) => {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Series</TableCell>
          <TableCell>Winner</TableCell>
          <TableCell>Loser</TableCell>
          <TableCell>Score</TableCell>
        </TableRow>
      </TableHead>
      <DataQuery query={GetTournament} variables={{id: tournament.id}}>
        {(data) => (
           <TableBody>
           {flatten(map(data.tournament.rounds, 'series')).map(series => (
             <TableRow key={series.id}>
                <TableCell>
                  <AppLink path={['events', tournament.id, series.id]} text={series.name} />
                </TableCell>
                {series.participants.map((participant, index) => (
                  <TableCell key={series.id + ' ' + index}>{participant.name}</TableCell>
                ))}
                <TableCell>{join(map(series.participants, 'score'), '-')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        )}
      </DataQuery>
    </Table>
  )
}

const EventsView = ({match, history}) => {
  return (
    <DataQuery query={GetEvents}>
      {(data) => (
        <Grid container spacing={24}>
          <Grid item xs={6}>
            {data.events.map(event => (
              <div key={event.index}>
                <Typography variant='h6'>{event.name}</Typography>
                {event.tournaments.map(tournament => (
                  <ExpansionPanel
                    key={tournament.id}
                    expanded={match.params.id === tournament.id}
                    onChange={(o, e) => history.push(e ? '/events/' + tournament.id : '/events')}
                  >
                    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography>
                        <AppLink path={['events', tournament.id]} text={tournament.name} />
                      </Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                      <Tournament tournament={tournament}/>
                    </ExpansionPanelDetails>
                  </ExpansionPanel>
                ))}
              </div>
            ))}
          </Grid>
          {match.params.sid && <Grid item xs={6}>
            <Series id={match.params.sid} />
          </Grid>}
        </Grid>
      )}
    </DataQuery>
  )
}

export default EventsView
