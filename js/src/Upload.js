import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Typography from '@material-ui/core/Typography'
import UploadIcon from 'mdi-react/FileUploadIcon'

import CardIconHeader from './util/CardIconHeader'


const Upload = () => {
  return (
    <Card>
      <CardIconHeader
        icon={<UploadIcon />}
        title='Upload'
      />
      <CardContent>
        <Typography>Coming soon.</Typography>
      </CardContent>
    </Card>
  )
}

export default Upload
