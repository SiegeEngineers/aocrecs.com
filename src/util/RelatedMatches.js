import React, {useState} from 'react'

import Pagination from 'material-ui-flat-pagination'
import {assign} from 'lodash'

import DataQuery from './DataQuery'
import Matches from '../Matches'

const RelatedMatches = ({query, variables, field, children}) => {
  const limit = 8
  const [offset, setOffset] = useState(0)
  return (
    <DataQuery query={query} variables={assign({offset, limit}, variables)}>
      {(data) => (
        <div>
          {children && children(data[field])}
          {data[field].match_count > limit && <Pagination
            limit={limit}
            offset={offset}
            total={data[field].match_count}
            onClick={(e, offset) => setOffset(offset)}
          />}
          <Matches matches={data[field].matches} />
          {data[field].match_count > limit && <Pagination
            limit={limit}
            offset={offset}
            total={data[field].match_count}
            onClick={(e, offset) => setOffset(offset)}
          />}
        </div>
      )}
    </DataQuery>
  )
}

export default RelatedMatches
