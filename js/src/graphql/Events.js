import gql from 'graphql-tag';

export default gql`
{
  events {
    id
    name
    tournaments {
      id
      name
      series {
        id
        name
        participants {
          name
          score
          winner
        }
      }
    }
    maps {
      name
    }
  }
}
`;
