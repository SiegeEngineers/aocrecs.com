import React, {useState} from 'react'

import {useMutation} from '@apollo/react-hooks'

import {makeStyles} from '@material-ui/styles'
import Button from '@material-ui/core/Button'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Link from '@material-ui/core/Link'
import Typography from '@material-ui/core/Typography'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'
import DialogTitle from '@material-ui/core/DialogTitle'

import UploadIcon from 'mdi-react/FileUploadIcon'

import CardIconHeader from './util/CardIconHeader'
import CircularProgress from '@material-ui/core/CircularProgress'


import DoUpload from './graphql/Upload'

const useStyles = makeStyles({
  input: {
    display: 'none'
  }
})


const UploadAlert = ({message}) => {
  const [open, setOpen] = useState(true)
  return (
    <Dialog open={open} onClose={() => setOpen(false)}>
      <DialogTitle>Upload Failed</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Sorry, your upload failed for the following reason: {message}. If you have questions or believe this to be incorrect,
          please contact <code>happyleaves#4133</code> on <Link target="_blank" href="https://discordapp.com/invite/njAsNuD">Discord</Link>.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setOpen(false)} color='primary' autoFocus>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  )
}

const Upload = ({history}) => {
  const classes = useStyles()
  const [mutate, {loading, error, data}] = useMutation(DoUpload, {
    onCompleted({upload}) {
      if(upload.success) {
        history.push(`/match/${upload.match_id.toString()}`)
      }
    }
  })
  const onChange = ({
    target: {validity, files: [rec_file]}
  }) => validity.valid && mutate({variables: {rec_file}})
  return (
    <Card>
      <CardIconHeader icon={<UploadIcon />} title='Upload' />
      <CardContent>
        <Typography>
          Select a file to upload. Supported types:
          <ul>
            <li>Userpatch 1.4 and up (<code>.mgz</code>)</li>
            <li>Definitive Edition (<code>.aoe2record</code>)</li>
            <li>The Conquerors (<code>.mgx</code>)</li>
            <li>Age of Kings (<code>.mgl</code>)</li>
          </ul>
          If your file is part of an event, please don't use this form. Instead, contact <code>happyleaves#4133</code> on <Link target="_blank" href="https://discordapp.com/invite/njAsNuD">Discord</Link> to have it appropriately catalogued.
        </Typography>
        <input className={classes.input} id='rec_file' type='file' onChange={onChange} />
        {loading
          ? <CircularProgress />
          : <label htmlFor='rec_file'>
              <Button variant='contained' color='primary' component='span'>Upload</Button>
            </label>
        }
        {error && <UploadAlert message={error.message} />}
        {data && !data.upload.success && <UploadAlert message={data.upload.message} />}
      </CardContent>
    </Card>
  )
}

export default Upload
