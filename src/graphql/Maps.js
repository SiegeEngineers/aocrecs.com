import gql from 'graphql-tag';

export default gql`
{
  stats {
    by_map {
      map {
        id
        name
      }
      num_matches
      percent_matches
    }
  }
}
`
