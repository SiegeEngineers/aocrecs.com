import React, {useGlobal} from 'reactn'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import FormControl from '@material-ui/core/FormControl'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import Select from '@material-ui/core/Select'
import Typography from '@material-ui/core/Typography'
import FormGroup from '@material-ui/core/FormGroup'

import DataQuery from './util/DataQuery.js'
import RelatedMatches from './util/RelatedMatches'

import GetSearchOptions from './graphql/SearchOptions'
import GetSearchOptionsDataset from './graphql/SearchOptionsDataset'
import GetSearchOptionsPlatform from './graphql/SearchOptionsPlatform'
import GetSearchResults from './graphql/SearchResults'
import {findKey, merge} from 'lodash';

const update = (params, table, name, value) => {
  if (value === '') {
    delete params[table][name]
  } else {
    params = merge(params, {[table]: {[name]: {values: [value]}}})
  }
  return params
}

const Options = ({label, table, name, data}) => {
  const [values, setter] = useGlobal('search')
  const tbl = values[table] || {}
  const val2 = tbl[name] || {}
  const val = val2['values'] || ''
  return (
    <FormControl style={{minWidth: 120}}>
      <InputLabel htmlFor={name}>{label}</InputLabel>
      <Select inputProps={{name: name, id: name}} value={val} onChange={e => setter(update(values, table, name, e.target.value))}>
        <MenuItem value=""></MenuItem>
        {data.map((item) =>
          <MenuItem key={name+item.id} value={item.id}>{item.label} ({item.count.toLocaleString()})</MenuItem>
        )}
      </Select>
    </FormControl>
  )
}

const Form = () => {
  const [values,] = useGlobal('search')
  return (
    <DataQuery query={GetSearchOptions}>
      {(data) => (
                <Grid container spacing={24}>
          <Grid item xs={3}>

        <Card>
          <CardContent>
            <Typography variant='h5'>General</Typography>
            <FormGroup>
              <Options label="Team Size" table="match" name="team_size" data={data.stats.team_sizes} />
              <Options label="Diplomacy" table="match" name="diplomacy_type" data={data.stats.diplomacy_types} />
              <Options label="Map" table="match" name="map_name" data={data.stats.maps} />
              <Options label="Type" table="match" name="type_id" data={data.stats.game_types} />
              <Options label="Mirror" table="match" name="mirror" data={data.stats.mirror} />
              <Options label="Rated" table="match" name="rated" data={data.stats.rated} />
              <Options label="ZR" table="match" name="rms_zr" data={data.stats.rms_zr} />
              <Options label="Event" table="match" name="event_id" data={data.stats.events} />
              <Options label="Tournament" table="match" name="tournament_id" data={data.stats.tournaments} />
            </FormGroup>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={3}>

        <Card>
          <CardContent>
            <Typography variant='h5'>Dataset</Typography>
            <Options label="Dataset" table="match" name="dataset_id" data={data.stats.datasets} />
            {findKey(values, "dataset_id") &&
              <DataQuery query={GetSearchOptionsDataset} variables={{dataset_id: values[findKey(values, "dataset_id")].dataset_id.values[0]}}>
              {(data) => (
                <FormGroup>
                  <Options label="Civilization" table="player" name="civilization_id" data={data.stats.civilizations} />
                </FormGroup>
              )}
              </DataQuery>
            }
          </CardContent>
        </Card>
      </Grid>
            <Grid item xs={3}>
        <Card>
          <CardContent>
            <Typography variant='h5'>Platform</Typography>
            <Options label="Platform" table="match" name="platform_id" data={data.stats.platforms} />
            {findKey(values, "platform_id") &&
              <DataQuery query={GetSearchOptionsPlatform} variables={{platform_id: values[findKey(values, "platform_id")].platform_id.values[0]}}>
              {(data) => (
                <FormGroup>
                  <Options label="Ladder" table="match" name="ladder_id" data={data.stats.ladders} />
                </FormGroup>
              )}
              </DataQuery>
            }
          </CardContent>
        </Card>
      </Grid>

    </Grid>
      )}
    </DataQuery>
  )
}


const Results = ({params}) => {
  return (
    <RelatedMatches query={GetSearchResults} variables={{params}} field='search'>
      {(data) => (
        <Typography variant='h3'>{data.matches.count.toLocaleString()} matches</Typography>
      )}
    </RelatedMatches>
  )
}

const Search = ({match}) => {
  const [values,] = useGlobal('search')
  return (
    <div>
      <Form />
      <br />
      <Results params={values} />
    </div>
  )
}

export default Search
