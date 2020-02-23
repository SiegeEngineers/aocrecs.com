import gql from 'graphql-tag';

export default gql`
{
  people {
    id
    name
    country
    match_count
    first_year
    last_year
  }
}
`
