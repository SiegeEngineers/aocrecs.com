import React, {useGlobal, useState} from 'reactn'

import Grid from '@material-ui/core/Grid'
import FormControl from '@material-ui/core/FormControl'
import InputLabel from '@material-ui/core/InputLabel'
import TextField from '@material-ui/core/TextField'
import MenuItem from '@material-ui/core/MenuItem'
import Select from '@material-ui/core/Select'

import {DatePicker} from 'material-ui-pickers'
import {useDebouncedCallback} from 'use-debounce'
import {merge} from 'lodash'

import NumberFormatCustom from './NumberFormatCustom'


const DEBOUNCE_MS = 800
const DATE_FORMAT = 'yyyy-MM-dd'


const updateAll = (params, table, key, value) => {
  if (value === null) {
    delete params[table][key]
  } else {
    params = merge(params, {[table]: {[key]: null}})
    params[table][key] = value
  }
  return params
}

const searchState = (table, name, key) => {
  const [params, setter] = useGlobal('search')
  const tables = params[table] || {}
  const keys = tables[name] || {}
  const value = keys[key] || ''
  return [value, params, setter]
}

export const OptionInput = ({label, table, name, data}) => {
  const key = 'values'
  const [current_value, params, setter] = searchState(table, name, key)
  const setValue = (value) => {
    let val = value
    if (val === 'true') {
      val = true
    } else if (val === 'false') {
      val = false
    } else if (!isNaN(val)) {
      val = parseInt(val)
    }
    setter(updateAll(params, table, name, value !== '' ? {[key]: [val]} : null))
  }
  return (
    <FormControl style={{minWidth: 120}}>
      <InputLabel htmlFor={name}>{label}</InputLabel>
      <Select
        inputProps={{name: name, id: name}}
        value={current_value}
        onChange={e => setValue(e.target.value)}
      >
        <MenuItem value=''></MenuItem>
        {data.map((item) =>
          <MenuItem key={name+item.value} value={item.value}>
            {item.label}
          </MenuItem>
        )}
      </Select>
    </FormControl>
  )
}

export const TextInput = ({label, table, name}) => {
  const key = 'values'
  const [text, setText] = useState('')
  const [, params, setter] = searchState(table, name, key)
  const [setValue] = useDebouncedCallback((val) => {
    setter(updateAll(params, table, name, val !== '' ? {[key]: [val]} : null))
  }, DEBOUNCE_MS)

  return (
    <FormControl style={{minWidth: 120}}>
      <TextField
        label={label}
        value={text}
        onChange={(e) => {
          setText(e.target.value)
          setValue(e.target.value)
        }}
      />
    </FormControl>
  )
}

export const NumberInput = ({label, table, name, validation}) => {
  const [number, setNumber] = useState('')
  const [comparator, setComparator] = useState('gte')
  const [, params, setter] = searchState(table, name, comparator)
  const [debouncedSetter] = useDebouncedCallback((key, value) => {
    setter(updateAll(params, table, name, value !== '' ? {[key]: parseInt(value)} : null))
  }, DEBOUNCE_MS)
  const setValue = (key, value) => {
    setNumber(value)
    setComparator(key)
    debouncedSetter(key, value)
  }
  return (
    <Grid container>
      <Grid item>
        <FormControl style={{minWidth: 120}}>
          <InputLabel htmlFor={'comparator'}>Comparator</InputLabel>
          <Select
            value={comparator}
            inputProps={{id: 'comparator'}}
            onChange={e => setValue(e.target.value, number)}
          >
            <MenuItem key='gte' value='gte'>&gt;=</MenuItem>
            <MenuItem key='lte' value='lte'>&lt;=</MenuItem>
          </Select>
        </FormControl>
      </Grid>
      <Grid item>
        <FormControl>
          <TextField
            label={label}
            value={number}
            onChange={e => setValue(comparator, e.target.value)}
            InputProps={{inputComponent: NumberFormatCustom, inputProps: {isAllowed: validation}}}
          />
        </FormControl>
      </Grid>
    </Grid>
  )
}

export const DateInput = ({label, table, name}) => {
  const key = 'date'
  const [value, params, setter] = searchState(table, name, key)
  const setValue = (value) => {
    setter(updateAll(params, table, name, value !== null ? {[key]: value.toISOString().substring(0, 10)} : null))
  }
  return (
    <DatePicker
      label={label}
      clearable
      value={value !== '' ? value : null}
      onChange={setValue}
      format={DATE_FORMAT}
    />
  )
}
