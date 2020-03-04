import React from 'react'
import {makeStyles} from '@material-ui/styles'

import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'

const useStyles = makeStyles(theme => ({
  downloadLink: {
    color: theme.palette.primary.main
  }
}))

const Files = ({files}) => {
  const classes = useStyles()
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>File</TableCell>
          <TableCell>Owner</TableCell>
          <TableCell align='right'>Size (bytes)</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {files.map(file => (
          <TableRow key={file.id}>
            <TableCell><a className={classes.downloadLink} href={file.download_link}>{file.original_filename}</a></TableCell>
            <TableCell>{file.owner.name}</TableCell>
            <TableCell align='right'>{file.size.toLocaleString()}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default Files
