import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'

import Card from '@material-ui/core/Card'
import Grid from '@material-ui/core/Grid'
import FormControl from '@material-ui/core/FormControl'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import Select from '@material-ui/core/Select'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import CivIcon from 'mdi-react/ChessRookIcon'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import DataQuery from './util/DataQuery.js'
import RelatedMatches from './util/RelatedMatches'

import GetCivs from './graphql/Civilizations.js'
import GetDatasets from './graphql/Datasets.js'
import GetCivilization from './graphql/Civilization.js'


const useStyles = makeStyles({
  card: {
    marginBottom: '10px'
  }
})

const CivTable = ({civilizations, selected}) => {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Civilization</TableCell>
          <TableCell>Matches</TableCell>
          <TableCell>Percent</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {civilizations.map((civilization, index) =>
          <TableRow key={index} selected={selected === civilization.id}>
            <TableCell>
              <AppLink path={['civilizations', civilization.dataset_id, civilization.id]} text={civilization.name} />
            </TableCell>
            <TableCell>{civilization.count.toLocaleString()}</TableCell>
            <TableCell>{Math.round(civilization.percent * 1000)/10}%</TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

const Civilization = ({id, dataset_id}) => {
  const classes = useStyles()
  return (
    <RelatedMatches query={GetCivilization} variables={{id, dataset_id}} field='civilization'>
      {(data) => (
        <Card className={classes.card}>
          <CardIconHeader
            icon={<CivIcon />}
            title={data.name}
          />
          <Typography component='span'>
            <ul>
              {data.bonuses.map((bonus, index) =>
                <li key={index}>{bonus.description}</li>
              )}
            </ul>
          </Typography>
        </Card>
      )}
    </RelatedMatches>
  )
}

const CivilizationsView = ({match}) => {
  const [dataset_id, setDataset] = useState(match.params.did ? parseInt(match.params.did) : 1)
  return (
    <Grid container spacing={24}>
      <Grid item xs={6}>
        <FormControl>
          <InputLabel htmlFor='dataset'>Dataset</InputLabel>
          <DataQuery query={GetDatasets}>
            {(data) => (
              <Select value={dataset_id} onChange={(e, v) => setDataset(e.target.value)}>
                {data.search_options.general.datasets.map((dataset) =>
                  <MenuItem key={dataset.value} value={dataset.value}>{dataset.label}</MenuItem>
                )}
              </Select>
            )}
          </DataQuery>
        </FormControl>
        <br />
        <br />
        <DataQuery query={GetCivs} variables={{dataset_id: parseInt(dataset_id)}}>
          {(data) => (
            <CivTable civilizations={data.civilizations} selected={parseInt(match.params.id)} />
          )}
        </DataQuery>
      </Grid>
      {match.params.id && <Grid item xs={6}>
        <Civilization id={parseInt(match.params.id)} dataset_id={parseInt(dataset_id)} />
      </Grid>}
    </Grid>
  )
}

export default CivilizationsView
