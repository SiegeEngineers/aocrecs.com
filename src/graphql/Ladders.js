import gql from 'graphql-tag';

export default gql`
{
  meta_ladders {
    id
    name
    ranks {
      rank
      rating
      user {
        id
        name
      }
    }
  }
}
`;
