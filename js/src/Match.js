import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'

import AppBar from '@material-ui/core/AppBar'
import Button from '@material-ui/core/Button'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'


import MatchIcon from 'mdi-react/SwordCrossIcon'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import {getMatchTitle} from './util/Shared'

import Chat from './match/Chat'
import Information from './match/Information'
import Achievements from './match/Achievements'
import Files from './match/Files'
import Map from './match/Map'
import {Teams} from './match/Teams'


const useStyles = makeStyles(theme => ({
  tabContent: {
    padding: '10px'
  }
}))


const Match = ({match}) => {
  const [tab, setTab] = useState(0)
  const classes = useStyles()
  const title = getMatchTitle(match, true)
  return (
    <Card>
      <CardIconHeader icon={<AppLink path={['match', match.id]} text={<MatchIcon />} />} title={title}/>
      <CardContent>
        <AppBar position='static'>
          <Tabs value={tab} onChange={(e, value) => setTab(value)}>
            <Tab label='Players' />
            <Tab label='Information' />
            <Tab label='Map' />
            <Tab label='Files' />
            <Tab label='Chat' />
            {match.postgame && <Tab label='Achievements' />}}
          </Tabs>
        </AppBar>
        <Typography component='div' className={classes.tabContent}>
          {tab === 0 && <Teams size={match.team_size} teams={match.teams} rated={match.rated} postgame={match.postgame} />}
          {tab === 1 && <Information match={match} />}
          {tab === 2 && <Map match={match} />}
          {tab === 3 && <Files files={match.files} />}
          {tab === 4 && <Chat match={match} />}
          {tab === 5 && <Achievements size={match.team_size} teams={match.teams} />}
        </Typography>
        {match.has_playback && <AppLink path={['match', match.id]} text={<Button variant="contained" color="primary">Extended Stats</Button>} />}
      </CardContent>
    </Card>
  )
}

export default Match
