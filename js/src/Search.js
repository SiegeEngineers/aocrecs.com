import React, {useGlobal} from 'reactn'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import FormGroup from '@material-ui/core/FormGroup'

import {findKey} from 'lodash'

import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'
import {OptionInput, DateInput, TextInput, NumberInput, BoolInput} from './util/Input'

import GetSearchOptions from './graphql/SearchOptions'
import GetSearchOptionsDataset from './graphql/SearchOptionsDataset'
import GetSearchOptionsPlatform from './graphql/SearchOptionsPlatform'
import GetSearchResults from './graphql/SearchResults'

import FormControl from '@material-ui/core/FormControl'

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
          <OptionInput label='Extended Stats' table='matches' name='has_playback' data={data.search_options.general.playback} />
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
        <FormGroup>
          <OptionInput label='Dataset' table='matches' name='dataset_id' data={data.search_options.general.datasets} />
          </FormGroup>
        {findKey(values, 'dataset_id') &&
          <DataQuery
            query={GetSearchOptionsDataset}
            variables={{dataset_id: parseInt(values[findKey(values, 'dataset_id')].dataset_id.values[0])}}
          >
          {(data) => (
            <FormGroup>
              <OptionInput label='Civilization' table='players' name='civilization_id' data={data.search_options.civilizations} />
              <OptionInput label='Version' table='matches' name='dataset_version' data={data.search_options.versions} />
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
          <TextInput label='Name' table='players' name='name' />
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
        <FormGroup>
        <OptionInput label='Platform' table='matches' name='platform_id' data={data.search_options.general.platforms} />
        </FormGroup>
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

const PlaybackSection = ({data, values}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Events</Typography>
        <Grid container>
          <Grid xs={6}>
        <FormControl component='fieldset'>
          <BoolInput label='Feudal Archers' table='flags' name='archers' />
          <BoolInput label='Feudal Trush' table='flags' name='trushes' />
          <BoolInput label='Feudal Skirmishers' table='flags' name='skirmishers' />
          <BoolInput label='Feudal Scouts' table='flags' name='scouts' />
          <BoolInput label='Feudal Men-at-arms' table='flags' name='maa' />
          <BoolInput label='Drush' table='flags' name='drush' />
          <BoolInput label='Fast Castle' table='flags' name='fast_castle' />
          <BoolInput label='Deer Push' table='flags' name='deer_pushes' />
          <BoolInput label='Daut Castle' table='flags' name='daut_castles' />
          <BoolInput label='Scout Lost to TC' table='flags' name='scout_lost_to_tc' />
        </FormControl>
      </Grid>
      <Grid xs={6}>
        <FormControl component='fieldset'>
        <BoolInput label='Castle Drop' table='flags' name='castle_drops' />
          <BoolInput label='Boar Steal' table='flags' name='boar_steals' />
          <BoolInput label='Sheep Steal' table='flags' name='sheep_steals' />
          <BoolInput label='Boar Kills Villager' table='flags' name='lost_to_boar' />
          <BoolInput label='Wolf Kills Villager' table='flags' name='lost_to_predator' />
          <BoolInput label='TC Kills Boar' table='flags' name='tc_killed_boar' />
          <BoolInput label='TC Kills Sheep' table='flags' name='tc_killed_sheep' />
          <BoolInput label='Castle Race' table='flags' name='castle_race' />
          <BoolInput label='Splash Damage Kills' table='flags' name='badaboom' />
          <BoolInput label='Lost Research' table='flags' name='lost_research' />
</FormControl>
      </Grid>
    </Grid>

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
            <PlaybackSection data={data} />
          </Grid>
          <Grid item xs={3}>
            <PlayerSection data={data} />
          </Grid>
          <Grid item xs={3}>
            <DatasetSection data={data} values={values} />
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
      <Results params={values} />
    </div>
  )
}

export default Search
