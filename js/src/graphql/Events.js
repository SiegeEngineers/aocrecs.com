import gql from 'graphql-tag';

export default gql`
{
  events {
    id
    name
    tournaments {
      id
      name
    }
    maps {
      id
      name
    }
  }
}
`;
