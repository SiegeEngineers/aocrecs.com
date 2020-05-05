import React, {useState} from 'react'
import Pagination from 'material-ui-flat-pagination'

const PaginatedTable = ({rows, children, limit}) => {
  const [offset, setOffset] = useState(0)
  const total = rows.length
  if(offset >= total) {
    setOffset(0)
  }
  return (
    <>
      {children(rows.slice(offset, offset + limit))}
      {total > limit && <Pagination
        limit={limit}
        offset={offset}
        total={total}
        onClick={(e, offset) => setOffset(offset)}
      />}
    </>
  )
}

export default PaginatedTable
