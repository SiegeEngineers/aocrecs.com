import gql from 'graphql-tag';

export default gql`
{
  search_options {
    general {
      datasets {
        value
        label
      }
    }
  }
}
`
