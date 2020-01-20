import gql from 'graphql-tag';

export default gql`
query Event($id: String!) {
  event(id: $id) {
    id
    year
    name
    tournaments {
      id
      event_id
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
