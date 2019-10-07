import gql from 'graphql-tag';

export default gql`
{
  stats {
    by_map {
      name
      builtin
      event_maps {
        event {
          id
          name
        }
      }
      count
      percent
    }
  }
}
`
