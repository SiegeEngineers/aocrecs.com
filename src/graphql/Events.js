import gql from 'graphql-tag';

export default gql`
{
  events {
    name
    index
    tournaments {
      id
      name
    }
  }
}
`;
