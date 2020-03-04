import React from 'react'
import {makeStyles} from '@material-ui/styles'

import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import MVPIcon from 'mdi-react/StarIcon'

import AppLink from '../util/AppLink'
import WinnerMark from '../util/WinnerMark'
import {getHasTeams, ChangeIndicator} from '../util/Shared'
import PlayerName from './PlayerName'

const useStyles = makeStyles(theme => ({
  mvpIcon: {
    width: '12px',
    height: '12px'
  },
  teamWinner: {
    width: '16px',
    height: '16px'
  },
  winner: {
    width: '12px',
    height: '12px'
  }
}))


export const TeamRow = ({number, winner, span}) => {
  const classes = useStyles()
  return (
    <TableRow>
      <TableCell colSpan={span}>
        <Typography variant='h6'>
          Team {number} <WinnerMark winner={winner} className={classes.teamWinner} />
        </Typography>
      </TableCell>
    </TableRow>
  )
}

export const TeamBody = ({teams, hasTeams, children, span}) => {
  const classes = useStyles()
  return (
    <>
      {teams.map((team, index) => (
        <TableBody key={index}>
          {hasTeams && <TeamRow number={index + 1} winner={team.winner} span={span} />}
          {team.players.map((player, mindex) => (
            <TableRow key={mindex}>
              <TableCell>
                <WinnerMark winner={!hasTeams && player.winner} className={classes.winner} /> <PlayerName player={player} />
              </TableCell>
              {children(player)}
            </TableRow>
          ))}
        </TableBody>
      ))}
    </>
  )
}

const rateString = (player) => {
  const diff = player.rate_after - player.rate_before
  return <>{player.rate_snapshot} <ChangeIndicator change={diff} /></>
}

export const Teams = ({size, teams, rated, postgame}) => {
  const hasTeams = getHasTeams(size)
  const classes = useStyles()
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Player</TableCell>
          <TableCell>Civilization</TableCell>
          {hasTeams && <TableCell>MVP</TableCell>}
          {rated && <TableCell align='right'>Rating</TableCell>}
          {postgame && <TableCell align='right'>Score</TableCell>}
        </TableRow>
      </TableHead>
      <TeamBody teams={teams} hasTeams={hasTeams} span={5}>
        {(player) => (
          <>
            <TableCell>
              <AppLink path={['civilizations', player.civilization.dataset_id, player.civilization.id]} text={player.civilization.name} />
            </TableCell>
            {hasTeams && <TableCell>
              {player.mvp && <MVPIcon className={classes.mvpIcon} />}
            </TableCell>}
            {rated && <TableCell align='right'>{rateString(player)}</TableCell>}
            {postgame && <TableCell align='right'>{player.score && player.score.toLocaleString()}</TableCell>}
          </>
        )}
      </TeamBody>
    </Table>
  )
}
