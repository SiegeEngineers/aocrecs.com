import React from 'react'
import {makeStyles} from '@material-ui/styles'

import Grid from '@material-ui/core/Grid'

import Typography from '@material-ui/core/Typography'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'

import {flatMap, map, find, get, flatMapDeep, orderBy, uniqBy} from 'lodash'

import AppLink from '../util/AppLink'
import WinnerMark from '../util/WinnerMark'
import PlayerName from './PlayerName'
import {getHasTeams} from '../util/Shared'
import DataQuery from '../util/DataQuery'
import PaginatedTable from '../util/PaginatedTable'
import GetFlags from '../graphql/Flags'

const useStyles = makeStyles(theme => ({
  teamWinner: {
    width: '16px',
    height: '16px'
  },
  matrixRight: {
    borderRight: '1px solid rgba(81, 81, 81, 1)'
  },
  matrixLeft: {
    borderRight: '1px solid rgba(81, 81, 81, 1)'
  }
}))


const Flags = ({match, selected}) => {
  const hasTeams = getHasTeams(match.team_size)
  return (
    <DataQuery query={GetFlags} variables={{match_id: match.id}}>
    {(data) => (
      <Grid container spacing={5}>
        <Grid item>
          {hasTeams ? <TeamFlags match={data.match} selected={selected} /> : <SingleFlags match={data.match} selected={selected} />}
        </Grid>
        <Grid item>
          {selected && <Log match={data.match} selected={selected} />}
        </Grid>
      </Grid>
    )}
    </DataQuery>
  )
}


const Log = ({match, selected}) => {
  const flags = orderBy(flatMapDeep(match.teams, team => (
    map(team.players, player => (
      player.flags.filter(flag => flag.type === selected).map(flag => (
        flag.evidence.map(ev => (
          {user: player.user, name: player.name, color_id: player.color_id, ...ev}
        ))
      ))
    ))
  )), 'timestamp')
  return (
    <>
      <Typography variant='h6'>Event Log</Typography>
      <PaginatedTable limit={15} rows={flags}>
      {(rows) => (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Player</TableCell>
              <TableCell></TableCell>
              <TableCell>Timestamp</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
          {rows.map((flag, i) => (
            <TableRow key={i}>
              <TableCell><PlayerName player={flag} /></TableCell>
              <TableCell>{flag.value}</TableCell>
              <TableCell align='right'>{flag.timestamp}</TableCell>
            </TableRow>
          ))}
          </TableBody>
        </Table>
      )}
      </PaginatedTable>
    </>
  )
}


const SingleFlags = ({match, selected}) => {
  const classes = useStyles()
  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell className={classes.matrixRight}></TableCell>
            {flatMap(match.teams, team => (
              map(team.players, player => (
                <TableCell className={classes.matrixLeft}><PlayerName player={player} /></TableCell>
                )
              )
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {orderBy(uniqBy(flatMapDeep(match.teams, team => (
            map(team.players, player => (player.flags.map(flag => ({type: flag.type, name: flag.name})))))), 'type'), 'name').map(flag => (
              <TableRow selected={selected === flag.type}>
                <TableCell className={classes.matrixRight}><AppLink path={['match', match.id, 'events', flag.type]} text={flag.name} /></TableCell>
                  {flatMap(match.teams, team => (
                    map(team.players, player => (
                      <TableCell align='center' className={classes.matrixLeft}>{get(find(player.flags, f => f.type === flag.type), 'count')}</TableCell>
                    ))
                  ))}
                </TableRow>
              )
            )
          }
        </TableBody>
      </Table>
    </>
  )
}


const TeamFlags = ({match, selected}) => {
  const classes = useStyles()
  return (
    <>
      {match.teams.map((team, i) => (
      <>
        <Typography variant='h6'>Team {i+1} <WinnerMark winner={team.winner} className={classes.teamWinner} /></Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell className={classes.matrixRight}></TableCell>
              {team.players.map(player => (<TableCell className={classes.matrixLeft}><PlayerName player={player} /></TableCell>))}
            </TableRow>
          </TableHead>
          <TableBody>
            {orderBy(uniqBy(flatMap(team.players, player => player.flags.map(flag => ({type: flag.type, name: flag.name}))), 'type'), 'name').map(flag => (
              <TableRow selected={selected === flag.type}>
                <TableCell className={classes.matrixRight}><AppLink path={['match', match.id, 'events', flag.type]} text={flag.name} /></TableCell>
                {team.players.map(player => (
                  <TableCell align='center' className={classes.matrixLeft}>{get(find(player.flags, f => f.type === flag.type), 'count')}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <br />
      </>
      ))}
    </>
  )
}

export default Flags
