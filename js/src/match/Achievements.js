import React from 'react'

import Table from '@material-ui/core/Table'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import {TeamBody} from './Teams'
import {getHasTeams} from '../util/Shared'


const Achievements = ({size, teams}) => {
  const hasTeams = getHasTeams(size)
  return (
    <div>
      <Typography variant='h6'>Score</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Military</TableCell>
            <TableCell align='right'>Economy</TableCell>
            <TableCell align='right'>Technology</TableCell>
            <TableCell align='right'>Society</TableCell>
            <TableCell align='right'>Total</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={6}>
          {(player) => (
            <>
              <TableCell align='right'>{player.military_score.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.economy_score.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.technology_score.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.society_score.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.score.toLocaleString()}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Military</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Units Killed</TableCell>
            <TableCell align='right'>Buildings Razed</TableCell>
            <TableCell align='right'>Units Lost</TableCell>
            <TableCell align='right'>Buildings Lost</TableCell>
            <TableCell align='right'>Units Converted</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={6}>
          {(player) => (
            <>
              <TableCell align='right'>{player.units_killed.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.buildings_razed.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.units_lost.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.buildings_lost.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.units_converted.toLocaleString()}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Economy</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Food</TableCell>
            <TableCell align='right'>Wood</TableCell>
            <TableCell align='right'>Stone</TableCell>
            <TableCell align='right'>Gold</TableCell>
            <TableCell align='right'>Sent</TableCell>
            <TableCell align='right'>Received</TableCell>
            <TableCell align='right'>Trade</TableCell>
            <TableCell align='right'>Relic</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={9}>
          {(player) => (
            <>
              <TableCell align='right'>{player.food_collected.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.wood_collected.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.stone_collected.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.gold_collected.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.tribute_sent.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.tribute_received.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.trade_gold.toLocaleString()}</TableCell>
              <TableCell align='right'>{player.relic_gold.toLocaleString()}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Technology</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Feudal</TableCell>
            <TableCell align='right'>Castle</TableCell>
            <TableCell align='right'>Imperial</TableCell>
            <TableCell align='right'>Explored</TableCell>
            <TableCell align='right'>Researches</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={6}>
          {(player) => (
            <>
              <TableCell align='right'>{player.feudal_time}</TableCell>
              <TableCell align='right'>{player.castle_time}</TableCell>
              <TableCell align='right'>{player.imperial_time}</TableCell>
              <TableCell align='right'>{player.explored_percent}%</TableCell>
              <TableCell align='right'>{player.research_count}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Society</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Wonders</TableCell>
            <TableCell align='right'>Castles</TableCell>
            <TableCell align='right'>Relics</TableCell>
            <TableCell align='right'>Villager High</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={5}>
          {(player) => (
            <>
              <TableCell align='right'>{player.total_wonders}</TableCell>
              <TableCell align='right'>{player.total_castles}</TableCell>
              <TableCell align='right'>{player.total_relics}</TableCell>
              <TableCell align='right'>{player.villager_high}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>

    </div>
  )
}

export default Achievements
