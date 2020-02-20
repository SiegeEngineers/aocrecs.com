import gql from 'graphql-tag';

export default gql`
{
  people {
    id
    name
    country
    match_count
  }
}
`
