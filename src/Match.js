import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'

import AppBar from '@material-ui/core/AppBar'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Link from '@material-ui/core/Link'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import Timestamp from 'react-timestamp'
import humanizeDuration from 'humanize-duration'
import {upperFirst} from 'lodash'

import MatchIcon from 'mdi-react/SwordCrossIcon'
import WinnerIcon from 'mdi-react/TrophyVariantIcon'
import MVPIcon from 'mdi-react/StarIcon'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'

const VOOBLY_MATCH_URL = 'https://www.voobly.com/match/view/'
const PLAYER_COLORS = {
  1: '#6599d8',
  2: '#f25f5f',
  3: '#00ee00',
  4: '#ffd700',
  5: '#00eeee',
  6: '#ea69e1',
  7: '#808080',
  8: '#ff8c00'
}

const useStyles = makeStyles({
  playerColor: {
    borderRadius: '4px',
    borderWidth: '1px',
    borderColor: 'white',
    height: '12px',
    width: '12px',
    display: 'inline-block',
    borderStyle: 'solid',
    marginRight: '4px'
  },
  tabContent: {
    padding: '20px'
  },
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
})

const getMatchTitle = (match) => {
  let title = match.type + ' ' + match.diplomacy_type
  if (match.diplomacy_type === 'TG') {
    title += ' ' + match.team_size
  }
  title += ' on ' + match.map.name
  return title
}

const getHasTeams = (size) => {
  return size !== '1v1'
}

const WinnerMark = ({winner, className}) => {
  return (
    <span>{winner
      ? <WinnerIcon className={className} />
      : <svg className={className} />
    }</span>
  )
}

const PlayerName = ({player}) => {
  const classes = useStyles()
  return (
    <span>
      <div style={{backgroundColor: PLAYER_COLORS[player.color_id + 1]}} className={classes.playerColor} />
      {player.voobly_user_id
        ? <AppLink path={['players', player.voobly_user_id]} text={player.voobly_user.name} />
        : player.name
      }
    </span>
  )
}

const PlayerRow = ({player, hasTeams}) => {
  const classes = useStyles()
  return (
    <TableRow>
      <TableCell>
        <WinnerMark winner={!hasTeams && player.winner} className={classes.winner} /> <PlayerName player={player} />
      </TableCell>
      <TableCell>
        <AppLink path={['civilizations', player.civilization.cid]} text={player.civilization.name} />
      </TableCell>
      {hasTeams && <TableCell>
        {player.mvp && <MVPIcon className={classes.mvpIcon} />}
      </TableCell>}
      <TableCell align='right'>{player.score}</TableCell>
    </TableRow>
  )
}

const Teams = ({size, teams}) => {
  const hasTeams = getHasTeams(size)
  const classes = useStyles()
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Player</TableCell>
          <TableCell>Civilization</TableCell>
          {hasTeams && <TableCell>MVP</TableCell>}
          <TableCell align='right'>Score</TableCell>
        </TableRow>
      </TableHead>
      {teams.map((team, index) => (
        <TableBody key={index}>
          {hasTeams && <TableRow>
            <TableCell colSpan={4}>
              <Typography variant='h6'>
                Team {index + 1} <WinnerMark winner={team.winner} className={classes.teamWinner} />
              </Typography>
            </TableCell>
          </TableRow>}
          {team.members.map((member, mindex) => <PlayerRow player={member} hasTeams={hasTeams} key={mindex} />)}
        </TableBody>
      ))}
    </Table>
  )
}

const Information = ({match}) => {
  const hasTeams = getHasTeams(match.team_size)
  return (
    <Table>
      <TableBody>
      <TableRow>
        <TableCell>Duration</TableCell><TableCell>{humanizeDuration(match.duration_secs * 1000)}</TableCell>
      </TableRow>
      {match.played && <TableRow>
        <TableCell>Played</TableCell><TableCell><Timestamp time={match.played} format='full' /></TableCell>
      </TableRow>}
      {match.rated && match.voobly_ladder && <TableRow>
        <TableCell>Ladder</TableCell>
        <TableCell>
          <AppLink path={['ladders', match.voobly_ladder.id]} text={match.voobly_ladder.name} />
        </TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Rated</TableCell><TableCell>{match.rated ? 'Yes' : 'No'}</TableCell>
      </TableRow>
      {match.series && <TableRow>
        <TableCell>Series</TableCell><TableCell>{match.series.name}</TableCell>
      </TableRow>}
      {!hasTeams && <TableRow>
        <TableCell>Mirror</TableCell><TableCell>{match.mirror ? 'Yes' : 'No'}</TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Map</TableCell>
        <TableCell>
          <AppLink path={['maps', match.map.id]} text={match.map.name} /> ({upperFirst(match.map_size)})
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Cheats</TableCell><TableCell>{match.cheats ? 'On' : 'Off'}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Reveal Map</TableCell><TableCell>{upperFirst(match.reveal_map)}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Population Limit</TableCell><TableCell>{match.population_limit}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Speed</TableCell><TableCell>{upperFirst(match.speed)}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Lock Teams</TableCell><TableCell>{match.lock_teams ? 'On' : 'Off'}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Difficulty</TableCell><TableCell>{upperFirst(match.difficulty)}</TableCell>
      </TableRow>
      {match.dataset && <TableRow>
        <TableCell>Dataset</TableCell><TableCell>{match.dataset.name} {match.dataset_version}</TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Version</TableCell><TableCell>{upperFirst(match.version)}</TableCell>
      </TableRow>
      {match.voobly_id && <TableRow>
        <TableCell>Match Link</TableCell>
        <TableCell>
          <Link href={VOOBLY_MATCH_URL + match.voobly_id} underline='always' target='_blank'>{match.voobly_id}</Link>
        </TableCell>
      </TableRow>}
    </TableBody>
    </Table>
  )
}

const Files = ({files}) => {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>File</TableCell>
          <TableCell>Owner</TableCell>
          <TableCell align='right'>Size</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {files.map(file => (
          <TableRow key={file.id}>
            <TableCell>{file.original_filename}</TableCell>
            <TableCell>{file.owner.name}</TableCell>
            <TableCell align='right'>{file.size}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

const Match = ({match}) => {
  const [tab, setTab] = useState(0)
  const classes = useStyles()
  const title = getMatchTitle(match)
  return (
    <Card>
      <CardIconHeader icon={<MatchIcon />} title={title}/>
      <CardContent>
        <AppBar position='static'>
          <Tabs value={tab} onChange={(e, value) => setTab(value)}>
            <Tab label='Players' />
            <Tab label='Information' />
            <Tab label='Files' />
          </Tabs>
        </AppBar>
        <Typography component='div' className={classes.tabContent}>
          {tab === 0 && <Teams size={match.team_size} teams={match.teams} />}
          {tab === 1 && <Information match={match} />}
          {tab === 2 && <Files files={match.files} />}
        </Typography>
      </CardContent>
    </Card>
  )
}

export default Match
