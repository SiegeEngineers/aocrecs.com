import React from 'react'

import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'

import PaginatedTable from '../util/PaginatedTable'
import DataQuery from '../util/DataQuery'
import PlayerName from './PlayerName'
import GetChat from '../graphql/Chat'


const Chat = ({match}) => {
  return (
    <DataQuery query={GetChat} variables={{match_id: match.id}}>
      {(data) => (
        <PaginatedTable rows={data.match.chat} limit={10}>
        {(rows) => (
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Time</TableCell>
                <TableCell>Audience</TableCell>
                <TableCell>Player</TableCell>
                <TableCell>Message</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((chat, i) => (
                <TableRow key={i}>
                  <TableCell>{chat.origination === 'lobby' ? 'Lobby' : chat.timestamp.split('.')[0]}</TableCell>
                  <TableCell>{chat.audience}</TableCell>
                  <TableCell><PlayerName player={chat.player} /></TableCell>
                  <TableCell>{chat.message}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
        </PaginatedTable>
      )}
    </DataQuery>
  )
}

export default Chat
