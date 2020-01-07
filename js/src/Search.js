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
          <TextInput label='Map' table='matches' name='map_name' />
          <OptionInput label='Diplomacy' table='matches' name='diplomacy_type' data={data.search_options.general.diplomacy_types} />
          <OptionInput label='Type' table='matches' name='type_id' data={data.search_options.general.game_types} />
          <OptionInput label='Mirror' table='matches' name='mirror' data={data.search_options.general.mirror} />
          <OptionInput label='Rated' table='matches' name='rated' data={data.search_options.general.rated} />
          <OptionInput label='ZR' table='matches' name='rms_zr' data={data.search_options.general.rms_zr} />
          <OptionInput label='Event' table='matches' name='event_id' data={data.search_options.general.events} />
          <OptionInput label='Tournament' table='matches' name='tournament_id' data={data.search_options.general.tournaments} />
          <DateInput label='Played' table='matches' name='played' />
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
        <OptionInput label='Dataset' table='matches' name='dataset_id' data={data.search_options.general.datasets} />
        {findKey(values, 'dataset_id') &&
          <DataQuery
            query={GetSearchOptionsDataset}
            variables={{dataset_id: parseInt(values[findKey(values, 'dataset_id')].dataset_id.values[0])}}
          >
          {(data) => (
            <FormGroup>
              <OptionInput label='Civilization' table='players' name='civilization_id' data={data.search_options.civilizations} />
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
          <TextInput label='Name' table='players' name='user_name' />
          <OptionInput label='Winner' table='players' name='winner' data={data.search_options.general.winner} />
          <OptionInput label='MVP' table='players' name='mvp' data={data.search_options.general.mvp} />
          <OptionInput label='Color' table='players' name='color_id' data={data.search_options.general.colors} />
          <NumberInput label='Rate' table='players' name='rate_snapshot' validation={validRate} />
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
        <OptionInput label='Platform' table='matches' name='platform_id' data={data.search_options.general.platforms} />
        {findKey(values, 'platform_id') &&
          <DataQuery
            query={GetSearchOptionsPlatform}
            variables={{platform_id: values[findKey(values, 'platform_id')].platform_id.values[0]}}
          >
          {(data) => (
            <FormGroup>
              <OptionInput label='Ladder' table='matches' name='ladder_id' data={data.search_options.ladders} />
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
