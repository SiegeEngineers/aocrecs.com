import React from 'react'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Table from '@material-ui/core/Table'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'

import PaginatedTable from '../util/PaginatedTable'
import DataQuery from '../util/DataQuery'
import GetMarket from '../graphql/Market'
import CommodityChart from './CommodityChart'
import PlayerChart from './PlayerChart'

import {orderBy, flatMapDeep} from 'lodash'

import PlayerName from './PlayerName'
import {getHasTeams} from '../util/Shared'


const Market = ({match, size}) => {
  const hasTeams = getHasTeams(size)
  return (
    <DataQuery query={GetMarket} variables={{match_id: match.id}}>
      {(data) => (
        <>
        <Grid container>
          <Grid item xs={4}><CommodityChart data={data.match.market} fields={['buy_food', 'sell_food']} title='Food Prices' /></Grid>
          <Grid item xs={4}><CommodityChart data={data.match.market} fields={['buy_wood', 'sell_wood']} title='Wood Prices' /></Grid>
          <Grid item xs={4}><CommodityChart data={data.match.market} fields={['buy_stone', 'sell_stone']} title='Stone Prices' /></Grid>
          {hasTeams && <>
            <Grid item xs={6}><PlayerChart players={data.match.players} group='trade_carts' field='count' title='Trade Carts' skipzero={true} /></Grid>
            <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='trade_profit' title='Trade Profit' skipzero={true} /></Grid>
            <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='tribute_sent' title='Tribute Sent'skipzero={true} /></Grid>
              <Grid item xs={6}><PlayerChart players={data.match.players} group='timeseries' field='tribute_received' title='Tribute Received'skipzero={true} /></Grid>
             <Grid item xs={6}>
                <Typography variant='h6'>Tribute</Typography>
                <PaginatedTable limit={10} rows={data.match.tribute}>
                  {(rows) => (
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell></TableCell>
                      <TableCell>From</TableCell>
                      <TableCell>To</TableCell>
                      <TableCell>Resource</TableCell>
                      <TableCell align='right'>Spent</TableCell>
                      <TableCell align='right'>Received</TableCell>
                      <TableCell align='right'>Fee</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {rows.map((tribute, i) => (
                      <TableRow key={i}>
                        <TableCell>{tribute.timestamp}</TableCell>
                        <TableCell><PlayerName player={tribute.from_player} /></TableCell>
                        <TableCell><PlayerName player={tribute.to_player} /></TableCell>
                        <TableCell>{tribute.resource}</TableCell>
                        <TableCell align='right'>{tribute.spent.toLocaleString()}</TableCell>
                        <TableCell align='right'>{tribute.received.toLocaleString()}</TableCell>
                        <TableCell align='right'>{tribute.fee}%</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                  )}
                </PaginatedTable>
              </Grid>
              </>}

              <Grid item xs={6}>
                <Typography variant='h6'>Transactions</Typography>
                <PaginatedTable limit={10} rows={orderBy(flatMapDeep(data.match.players.map(player => player.transactions.map(transaction => ({
                      timestamp: transaction.timestamp_secs,
                      player: player,
                      transaction: transaction
                })))), 'timestamp')}>
              {(rows) => (
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell></TableCell>
                      <TableCell>Player</TableCell>
                      <TableCell>Sold Resource</TableCell>
                      <TableCell>Sold Amount</TableCell>
                      <TableCell>Bought Resource</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {rows.map((row, i) => (
                      <TableRow key={i}>
                        <TableCell>{row.transaction.timestamp}</TableCell>
                        <TableCell><PlayerName player={row.player} /></TableCell>
                        <TableCell>{row.transaction.sold_resource}</TableCell>
                        <TableCell>{row.transaction.sold_amount.toLocaleString()}</TableCell>
                        <TableCell>{row.transaction.bought_resource}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
            )}
              </PaginatedTable>
              </Grid>
        </Grid>
        </>
      )}
    </DataQuery>
  )
}

export default Market
