import gql from 'graphql-tag';

export default gql`
query Tournament($id: String!) {
  tournament(id: $id) {
    rounds {
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
  }
}
`;
