import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'
import useReactRouter from 'use-react-router'

import AppBar from '@material-ui/core/AppBar'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
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

import Timestamp from 'react-timestamp'
import {map, join, sortBy, reverse, groupBy} from 'lodash'

import EventIcon from 'mdi-react/CalendarRangeIcon'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'
import WinnerMark from './util/WinnerMark'

import GetEvents from './graphql/Events'
import GetEvent from './graphql/Event'
import GetSeries from './graphql/Series'

const useStyles = makeStyles({
  card: {
    marginBottom: '10px'
  },
  sideWinner: {
    width: '16px',
    height: '16px'
  },
  tabContent: {
    padding: '0px'
  }
})

const Series = ({id}) => {
  const field = 'series'
  const classes = useStyles()
  return (
    <RelatedMatches query={GetSeries} variables={{id}} field={field}>
      {(data) => (
        <Card className={classes.card}>
          <CardIconHeader
            icon={<EventIcon />}
            title={data.name}
          />
          <CardContent>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell>Event</TableCell>
                  <TableCell>{data.tournament.event.name}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Tournament</TableCell>
                  <TableCell><AppLink path={['events', data.tournament.event.id, data.tournament.id]} text={data.tournament.name} /></TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Played</TableCell>
                  <TableCell><Timestamp time={data.played} format='full' /></TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Matches</TableCell>
                  <TableCell>{data.matches.count}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
            <br />
            <Typography component='span'>
              <Typography variant='h6'>Results</Typography>
              <table>
                <tbody>
                <tr>
                  {data.sides.map((side, index) =>
                    <td key={index} valign='top'>
                      {side.users.length > 1 && <div>
                        <WinnerMark winner={side.winner} className={classes.sideWinner} /> {side.name} ({side.score})
                      <ul>
                        {side.users.filter(user => user.id !== null).map(user =>
                          <li key={user.id}>
                            <AppLink path={['player', user.platform_id, user.id]} text={user.name} />
                          </li>
                        )}
                      </ul>
                    </div>}
                    {side.users.length === 1 && <div>
                      {side.users.map((user, i) =>
                        <span key={i}>
                          <WinnerMark winner={side.winner} className={classes.sideWinner} /> <AppLink path={['player', user.platform_id, user.id]} text={side.name} /> ({side.score})
                        </span>
                      )}
                    </div>}
                    {side.users.length === 0 && <div>
                        <span>
                          <WinnerMark winner={side.winner} className={classes.sideWinner} /> {side.name} ({side.score})
                        </span>
                    </div>}
                    </td>
                  )}
                </tr>
              </tbody>
              </table>
            </Typography>
          </CardContent>
        </Card>
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
       <TableBody>
       {tournament.series.map(series => (
         <TableRow key={series.id}>
            <TableCell>
              <AppLink path={['events', tournament.event_id, tournament.id, series.id]} text={series.name} />
            </TableCell>
            {reverse(sortBy(series.participants, 'score')).map((participant, index) => (
              <TableCell key={series.id + ' ' + index}>{participant.name}</TableCell>
            ))}
            <TableCell>{join(map(reverse(sortBy(series.participants, 'score')), 'score'), '-')}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

const Tournaments = ({tournaments}) => {
  const { history, match } = useReactRouter()
  return (
    <>
      {tournaments.map(tournament => (
        <ExpansionPanel
          key={tournament.id}
          expanded={match.params.tid === tournament.id}
          onChange={(o, e) => history.push(e ? '/events/' + tournament.event_id + '/' + tournament.id : '/events/' + tournament.event_id)}
        >
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              <AppLink path={['events', tournament.event_id, tournament.id]} text={tournament.name} />
            </Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <Tournament tournament={tournament}/>
          </ExpansionPanelDetails>
        </ExpansionPanel>
      ))}
    </>
  )
}

const MapTable = ({rows}) => {
  return (
    rows.length > 0 ? <Table>
      <TableHead>
        <TableRow>
          <TableCell>Map</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.map((row, index) =>
          <TableRow key={index}>
            <TableCell>
              <AppLink path={['maps', row.name]} text={row.name} />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
    : <p>No custom maps for this event</p>
  )
}


const Event = ({id}) => {
  const [tab, setTab] = useState(0)
  const classes = useStyles()
  return (
    <DataQuery query={GetEvent} variables={{id}}>
    {(data) => (
      <>
        <Typography variant='h5'>{data.event.name} ({data.event.year})</Typography>
        <AppBar position='static'>
          <Tabs value={tab} onChange={(e, value) => setTab(value)}>
            <Tab label='Tournaments' />
            <Tab label='Maps' />
          </Tabs>
        </AppBar>
        <Typography component='div' className={classes.tabContent}>
          {tab === 0 && <Tournaments tournaments={data.event.tournaments} />}
          {tab === 1 && <MapTable rows={data.event.maps} />}
        </Typography>
      </>
    )}
    </DataQuery>
  )
}


const EventsView = ({match, history}) => {
  return (
    <DataQuery query={GetEvents}>
      {(data) => (
        <Grid container spacing={24}>
          <Grid item xs={6}>
            {match.params.eid ?
              <>
                <Typography><AppLink path={['events']} text="< Back to Events" /></Typography>
                <Event id={match.params.eid} />
              </> :
              <>
              {reverse(Object.keys(groupBy(data.events, 'year'))).map(year => (
                <div key={year}>
                <Typography variant='h5'>{year}</Typography>
                <div>
                  {groupBy(data.events, 'year')[year].map(event => (
                    <Typography key={event.id}><AppLink path={['events', event.id]} text={event.name} /></Typography>
                  ))}
                </div>
                <br />
              </div>
            ))}
            </>}
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
