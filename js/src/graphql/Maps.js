import gql from 'graphql-tag';

export default gql`
{
  maps {
    name
    builtin
    events {
      id
      name
    }
    count
    percent
  }
}
`
