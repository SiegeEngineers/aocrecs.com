import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableRow from '@material-ui/core/TableRow'

import Timestamp from 'react-timestamp'

import VooblyUserIcon from 'mdi-react/AccountIcon'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'

const VooblyUser = ({voobly_user}) => {
  return (
    <Card>
      <CardIconHeader
        icon={<VooblyUserIcon />}
        title={voobly_user.name}
      />
      <CardContent>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Last Login</TableCell>
              <TableCell>
                <Timestamp time={voobly_user.last_login} format='full' />
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Account Created</TableCell>
              <TableCell>
                <Timestamp time={voobly_user.account_created} format='full' />
              </TableCell>
            </TableRow>
            {voobly_user.meta_ranks.map(rank => (
              <TableRow key={rank.ladder.id}>
                <TableCell>
                  <AppLink path={['ladders', rank.ladder.id]} text={rank.ladder.name} />
                </TableCell>
                <TableCell>#{rank.rank}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

export default VooblyUser
