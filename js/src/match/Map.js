import React from 'react'
import Typography from '@material-ui/core/Typography'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'

import YesIcon from 'mdi-react/CheckIcon'
import NoIcon from 'mdi-react/CloseIcon'

import AppLink from '../util/AppLink'

const BoolIcon = ({value}) => {
  return value ? <YesIcon /> : <NoIcon />
}


const Map = ({match}) => {
  return (
    <div>
      <Typography variant='h6'>{match.map_name}</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Size</TableCell>
            {match.map_events && <TableCell>Events</TableCell>}
            <TableCell>Seed</TableCell>
            <TableCell align='center'>Custom</TableCell>
            <TableCell align='center'>Fixed Positions</TableCell>
            <TableCell align='center'>Tech Effects</TableCell>
            <TableCell align='center'>Guard Object</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
            <TableCell>{match.map_size}</TableCell>
            {match.map_events && <TableCell>{match.map_events.map((event, i) => [
            i > 0 && ', ',
            <AppLink key={event.id} path={['events', event.id]} text={event.name} />
          ])}
            </TableCell>}
            <TableCell><code>{match.rms_seed}</code></TableCell>
            <TableCell align='center'><BoolIcon value={match.rms_custom} /></TableCell>
            <TableCell align='center'><BoolIcon value={match.direct_placement} /></TableCell>
            <TableCell align='center'><BoolIcon value={match.effect_quantity} /></TableCell>
            <TableCell align='center'><BoolIcon value={match.guard_state} /></TableCell>
        </TableBody>
      </Table>
      <img src={match.minimap_link} width='100%' alt={match.map_name} />
    </div>
  )
}

export default Map
