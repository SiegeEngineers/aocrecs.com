import React, {useEffect, useState} from 'react'

import Pagination from 'material-ui-flat-pagination'
import {merge} from 'lodash'
import Select from '@material-ui/core/Select'
import MenuItem from '@material-ui/core/MenuItem'

import DataQuery from './DataQuery'
import Matches from '../Matches'

const RelatedMatches = ({query, variables, field, children}) => {
  const limit = 8
  const [offset, setOffset] = useState(0)
  const [order, setOrder] = useState('matches.played')
  useEffect(() => setOffset(0), [variables])
  return (
    <DataQuery query={query} variables={merge({offset, limit, order}, variables)}>
      {(data) => (
        <div>
          {children && children(data[field])}
          {data[field].matches.count > limit && <Pagination
            limit={limit}
            offset={offset}
            total={data[field].matches.count}
            onClick={(e, offset) => setOffset(offset)}
            style={{display: 'inline'}}
          />}
          <span style={{margin: '5px'}}>Sort by</span>
          <Select value={order} onChange={(event) => setOrder(event.target.value)}>
            <MenuItem value="matches.played">Played</MenuItem>
            <MenuItem value="matches.added">Added</MenuItem>
          </Select>
          <Matches matches={data[field].matches.hits} />
          {data[field].matches.count > limit && <Pagination
            limit={limit}
            offset={offset}
            total={data[field].matches.count}
            onClick={(e, offset) => setOffset(offset)}
          />}
        </div>
      )}
    </DataQuery>
  )
}

export default RelatedMatches
