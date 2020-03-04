import gql from 'graphql-tag';

export default gql`
query Charts($match_id: Int!) {
  match(id: $match_id) {
    id
    players {
      name
      color_id
      timeseries {
        timestamp_secs
        population
        military
        percent_explored
        value_objects_destroyed
        value_current_units
      }
      apm {
        timestamp_secs
        actions
      }
      map_control {
        timestamp_secs
        control_percent
      }
    }
  }
}
`
