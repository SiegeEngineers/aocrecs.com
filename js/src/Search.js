import React, {useGlobal} from 'reactn'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import FormGroup from '@material-ui/core/FormGroup'

import {findKey} from 'lodash'

import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'
import {OptionInput, DateInput, TextInput, NumberInput} from './util/Input'

import GetSearchOptions from './graphql/SearchOptions'
import GetSearchOptionsDataset from './graphql/SearchOptionsDataset'
import GetSearchOptionsPlatform from './graphql/SearchOptionsPlatform'
import GetSearchResults from './graphql/SearchResults'

const MAX_RATE = 3000
const MIN_RATE = 0

const GeneralSection = ({data}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>General</Typography>
        <FormGroup>
          <OptionInput label='Team Size' table='match' name='team_size' data={data.stats.team_sizes} />
          <OptionInput label='Diplomacy' table='match' name='diplomacy_type' data={data.stats.diplomacy_types} />
          <OptionInput label='Map' table='match' name='map_name' data={data.stats.maps} />
          <OptionInput label='Type' table='match' name='type_id' data={data.stats.game_types} />
          <OptionInput label='Mirror' table='match' name='mirror' data={data.stats.mirror} />
          <OptionInput label='Rated' table='match' name='rated' data={data.stats.rated} />
          <OptionInput label='ZR' table='match' name='rms_zr' data={data.stats.rms_zr} />
          <OptionInput label='Event' table='match' name='event_id' data={data.stats.events} />
          <OptionInput label='Tournament' table='match' name='tournament_id' data={data.stats.tournaments} />
          <DateInput label='Played' table='match' name='played' />
        </FormGroup>
      </CardContent>
    </Card>
  )
}

const DatasetSection = ({data, values}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Dataset</Typography>
        <OptionInput label='Dataset' table='match' name='dataset_id' data={data.stats.datasets} />
        {findKey(values, 'dataset_id') &&
          <DataQuery
            query={GetSearchOptionsDataset}
            variables={{dataset_id: values[findKey(values, 'dataset_id')].dataset_id.values[0]}}
          >
          {(data) => (
            <FormGroup>
              <OptionInput label='Civilization' table='player' name='civilization_id' data={data.stats.civilizations} />
            </FormGroup>
          )}
          </DataQuery>
        }
      </CardContent>
    </Card>
  )
}

const PlayerSection = ({data}) => {
  const validRate = (values) => {
    const {formattedValue, floatValue} = values
    return formattedValue === "" || (floatValue < MAX_RATE && floatValue > MIN_RATE)
  }
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Player</Typography>
        <FormGroup>
          <TextInput label='Name' table='player' name='user_name' />
          <OptionInput label='Winner' table='player' name='winner' data={data.stats.winner} />
          <OptionInput label='MVP' table='player' name='mvp' data={data.stats.mvp} />
          <OptionInput label='Color' table='player' name='color_id' data={data.stats.colors} />
          <NumberInput label='Rate' table='player' name='rate_snapshot' validation={validRate} />
        </FormGroup>
      </CardContent>
    </Card>
  )
}

const PlatformSection = ({data, values}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Platform</Typography>
        <OptionInput label='Platform' table='match' name='platform_id' data={data.stats.platforms} />
        {findKey(values, 'platform_id') &&
          <DataQuery
            query={GetSearchOptionsPlatform}
            variables={{platform_id: values[findKey(values, 'platform_id')].platform_id.values[0]}}
          >
          {(data) => (
            <FormGroup>
              <OptionInput label='Ladder' table='match' name='ladder_id' data={data.stats.ladders} />
            </FormGroup>
          )}
          </DataQuery>
        }
      </CardContent>
    </Card>
  )
}

const Form = () => {
  const [values,] = useGlobal('search')
  return (
    <DataQuery query={GetSearchOptions}>
      {(data) => (
        <Grid container spacing={24}>
          <Grid item xs={3}>
            <GeneralSection data={data} />
          </Grid>
          <Grid item xs={3}>
            <PlayerSection data={data} />
          </Grid>
          <Grid item xs={3}>
            <DatasetSection data={data} values={values} />
          </Grid>
          <Grid item xs={3}>
            <PlatformSection data={data} values={values} />
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
