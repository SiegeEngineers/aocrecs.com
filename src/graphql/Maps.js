import gql from 'graphql-tag';

export default gql`
{
  stats {
    by_map {
      map {
        name
        builtin
        events {
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
